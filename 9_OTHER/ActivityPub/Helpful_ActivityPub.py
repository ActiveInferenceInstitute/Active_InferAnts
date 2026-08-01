import requests
from typing import Dict, List, Union, Optional
import json
from pyld import jsonld
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
import base64
import uuid
from datetime import datetime, timezone
import logging
from urllib.parse import urlparse
from cachetools import TTLCache, cached

class ActivityPubHelper:
    def __init__(self, base_url: str, access_token: str, cache_ttl: int = 300):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/activity+json",
            "Accept": "application/activity+json"
        }
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.cache = TTLCache(maxsize=1000, ttl=cache_ttl)
        self.logger = logging.getLogger(__name__)

    @cached(cache='self.cache')
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise

    def create_actor(self, username: str, display_name: str, summary: str) -> Dict:
        """Create a new actor (user) in the ActivityPub network."""
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        actor_data = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1"
            ],
            "type": "Person",
            "id": f"{self.base_url}/users/{username}",
            "preferredUsername": username,
            "name": display_name,
            "summary": summary,
            "inbox": f"{self.base_url}/users/{username}/inbox",
            "outbox": f"{self.base_url}/users/{username}/outbox",
            "followers": f"{self.base_url}/users/{username}/followers",
            "following": f"{self.base_url}/users/{username}/following",
            "liked": f"{self.base_url}/users/{username}/liked",
            "streams": [
                {
                    "type": "Collection",
                    "id": f"{self.base_url}/users/{username}/streams/main",
                    "name": "Main Stream"
                }
            ],
            "endpoints": {
                "sharedInbox": f"{self.base_url}/shared_inbox"
            },
            "publicKey": {
                "id": f"{self.base_url}/users/{username}#main-key",
                "owner": f"{self.base_url}/users/{username}",
                "publicKeyPem": public_key_pem
            },
            "icon": {
                "type": "Image",
                "mediaType": "image/png",
                "url": f"{self.base_url}/users/{username}/avatar.png"
            },
            "image": {
                "type": "Image",
                "mediaType": "image/jpeg",
                "url": f"{self.base_url}/users/{username}/header.jpg"
            },
            "manuallyApprovesFollowers": False,
            "discoverable": True,
            "published": datetime.now(timezone.utc).isoformat(),
            "updated": datetime.now(timezone.utc).isoformat(),
            "attachment": [
                {
                    "type": "PropertyValue",
                    "name": "Website",
                    "value": "<a href='https://example.com' target='_blank' rel='nofollow noopener noreferrer me'>https://example.com</a>"
                }
            ],
            "tag": [
                {
                    "type": "Hashtag",
                    "href": f"{self.base_url}/tags/activitypub",
                    "name": "#activitypub"
                }
            ]
        }
        response = self._make_request("POST", f"{self.base_url}/users", json=actor_data)
        return response.json()

    def get_actor(self, actor_id: str) -> Dict:
        """Fetch an actor's information."""
        response = self._make_request("GET", actor_id)
        return response.json()

    def update_actor(self, actor_id: str, updates: Dict) -> Dict:
        """Update an actor's information."""
        current_actor = self.get_actor(actor_id)
        updated_actor = {**current_actor, **updates, "updated": datetime.now(timezone.utc).isoformat()}
        response = self._make_request("PATCH", actor_id, json=updated_actor)
        return response.json()

    def create_note(self, actor_id: str, content: str, to: List[str], cc: Optional[List[str]] = None, 
                    in_reply_to: Optional[str] = None, attachments: Optional[List[Dict]] = None) -> Dict:
        """Create a new note (post) in the ActivityPub network."""
        note_id = f"{self.base_url}/notes/{uuid.uuid4()}"
        note_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Create",
            "actor": actor_id,
            "object": {
                "id": note_id,
                "type": "Note",
                "content": content,
                "to": to,
                "cc": cc or [],
                "attributedTo": actor_id,
                "inReplyTo": in_reply_to,
                "published": datetime.now(timezone.utc).isoformat(),
                "attachment": attachments or [],
                "tag": [
                    {
                        "type": "Mention",
                        "href": mention,
                        "name": f"@{urlparse(mention).path.split('/')[-1]}"
                    } for mention in to + (cc or []) if mention.startswith("http")
                ],
                "sensitive": False,
                "summary": None,  # Content warning, if any
                "language": "en"
            }
        }
        response = self._make_request("POST", f"{actor_id}/outbox", json=note_data)
        return response.json()

    def get_note(self, note_id: str) -> Dict:
        """Fetch a note's information."""
        response = self._make_request("GET", note_id)
        return response.json()

    def delete_note(self, actor_id: str, note_id: str) -> Dict:
        """Delete a note from the ActivityPub network."""
        delete_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Delete",
            "actor": actor_id,
            "object": {
                "id": note_id,
                "type": "Tombstone"
            },
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{actor_id}/outbox", json=delete_data)
        return response.json()

    def follow_actor(self, follower_id: str, followed_id: str) -> Dict:
        """Create a follow relationship between two actors."""
        follow_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Follow",
            "actor": follower_id,
            "object": followed_id,
            "id": f"{self.base_url}/activities/{uuid.uuid4()}",
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{follower_id}/outbox", json=follow_data)
        return response.json()

    def unfollow_actor(self, follower_id: str, followed_id: str) -> Dict:
        """Remove a follow relationship between two actors."""
        unfollow_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Undo",
            "actor": follower_id,
            "object": {
                "type": "Follow",
                "actor": follower_id,
                "object": followed_id
            },
            "id": f"{self.base_url}/activities/{uuid.uuid4()}",
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{follower_id}/outbox", json=unfollow_data)
        return response.json()

    def like_object(self, actor_id: str, object_id: str) -> Dict:
        """Like an object (e.g., a note) in the ActivityPub network."""
        like_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Like",
            "actor": actor_id,
            "object": object_id,
            "id": f"{self.base_url}/activities/{uuid.uuid4()}",
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{actor_id}/outbox", json=like_data)
        return response.json()

    def unlike_object(self, actor_id: str, object_id: str) -> Dict:
        """Remove a like from an object in the ActivityPub network."""
        unlike_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Undo",
            "actor": actor_id,
            "object": {
                "type": "Like",
                "actor": actor_id,
                "object": object_id
            },
            "id": f"{self.base_url}/activities/{uuid.uuid4()}",
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{actor_id}/outbox", json=unlike_data)
        return response.json()

    def get_inbox(self, actor_id: str, limit: int = 20, page: int = 1) -> Dict:
        """Fetch the inbox of an actor."""
        params = {"limit": limit, "page": page}
        response = self._make_request("GET", f"{actor_id}/inbox", params=params)
        return response.json()

    def get_outbox(self, actor_id: str, limit: int = 20, page: int = 1) -> Dict:
        """Fetch the outbox of an actor."""
        params = {"limit": limit, "page": page}
        response = self._make_request("GET", f"{actor_id}/outbox", params=params)
        return response.json()

    def get_followers(self, actor_id: str, limit: int = 20, page: int = 1) -> Dict:
        """Fetch the followers of an actor."""
        params = {"limit": limit, "page": page}
        response = self._make_request("GET", f"{actor_id}/followers", params=params)
        return response.json()

    def get_following(self, actor_id: str, limit: int = 20, page: int = 1) -> Dict:
        """Fetch the actors that an actor is following."""
        params = {"limit": limit, "page": page}
        response = self._make_request("GET", f"{actor_id}/following", params=params)
        return response.json()

    def create_collection(self, actor_id: str, name: str, items: List[str]) -> Dict:
        """Create a new collection in the ActivityPub network."""
        collection_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Collection",
            "id": f"{self.base_url}/collections/{uuid.uuid4()}",
            "attributedTo": actor_id,
            "name": name,
            "totalItems": len(items),
            "items": items,
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{actor_id}/collections", json=collection_data)
        return response.json()

    def add_to_collection(self, actor_id: str, collection_id: str, item_id: str) -> Dict:
        """Add an item to a collection."""
        add_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Add",
            "actor": actor_id,
            "object": item_id,
            "target": collection_id,
            "id": f"{self.base_url}/activities/{uuid.uuid4()}",
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{actor_id}/outbox", json=add_data)
        return response.json()

    def remove_from_collection(self, actor_id: str, collection_id: str, item_id: str) -> Dict:
        """Remove an item from a collection."""
        remove_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Remove",
            "actor": actor_id,
            "object": item_id,
            "target": collection_id,
            "id": f"{self.base_url}/activities/{uuid.uuid4()}",
            "published": datetime.now(timezone.utc).isoformat()
        }
        response = self._make_request("POST", f"{actor_id}/outbox", json=remove_data)
        return response.json()

    def search(self, query: str, type: Optional[str] = None, limit: int = 20, page: int = 1) -> Dict:
        """Search for actors, notes, or other objects in the ActivityPub network."""
        params = {"q": query, "type": type, "limit": limit, "page": page}
        response = self._make_request("GET", f"{self.base_url}/search", params=params)
        return response.json()

    def sign_message(self, message: str) -> str:
        """Sign a message using the actor's private key."""
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

    def verify_signature(self, message: str, signature: str, public_key_pem: str) -> bool:
        """Verify a signature using the provided public key."""
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        try:
            public_key.verify(
                base64.b64decode(signature),
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

    def expand_json_ld(self, data: Dict) -> Dict:
        """Expand JSON-LD data."""
        return jsonld.expand(data)

    def compact_json_ld(self, data: Dict, context: Dict) -> Dict:
        """Compact JSON-LD data."""
        return jsonld.compact(data, context)

    def create_image(self, actor_id: str, image_url: str, description: str, to: List[str], cc: Optional[List[str]] = None) -> Dict:
        """Create a new image object in the ActivityPub network."""
        image_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Create",
            "actor": actor_id,
            "object": {
                "type": "Image",
                "id": f"{self.base_url}/images/{uuid.uuid4()}",
                "url": image_url,
                "name": description,
                "to": to,
                "cc": cc or [],
                "attributedTo": actor_id
            }
        }
        response = requests.post(f"{actor_id}/outbox", json=image_data, headers=self.headers)
        return response.json()

    def create_event(self, actor_id: str, name: str, content: str, start_time: str, end_time: str, location: str, to: List[str], cc: Optional[List[str]] = None) -> Dict:
        """Create a new event in the ActivityPub network."""
        event_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Create",
            "actor": actor_id,
            "object": {
                "type": "Event",
                "name": name,
                "content": content,
                "startTime": start_time,
                "endTime": end_time,
                "location": {
                    "type": "Place",
                    "name": location
                },
                "to": to,
                "cc": cc or [],
                "attributedTo": actor_id
            }
        }
        response = requests.post(f"{actor_id}/outbox", json=event_data, headers=self.headers)
        return response.json()

    def create_group(self, actor_id: str, name: str, summary: str) -> Dict:
        """Create a new group in the ActivityPub network."""
        group_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Group",
            "name": name,
            "summary": summary,
            "attributedTo": actor_id
        }
        response = requests.post(f"{self.base_url}/groups", json=group_data, headers=self.headers)
        return response.json()

    def join_group(self, actor_id: str, group_id: str) -> Dict:
        """Join a group in the ActivityPub network."""
        join_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Join",
            "actor": actor_id,
            "object": group_id
        }
        response = requests.post(f"{actor_id}/outbox", json=join_data, headers=self.headers)
        return response.json()

    def leave_group(self, actor_id: str, group_id: str) -> Dict:
        """Leave a group in the ActivityPub network."""
        leave_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Leave",
            "actor": actor_id,
            "object": group_id
        }
        response = requests.post(f"{actor_id}/outbox", json=leave_data, headers=self.headers)
        return response.json()

    def create_question(self, actor_id: str, content: str, options: List[str], to: List[str], cc: Optional[List[str]] = None) -> Dict:
        """Create a new question (poll) in the ActivityPub network."""
        question_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Create",
            "actor": actor_id,
            "object": {
                "type": "Question",
                "content": content,
                "oneOf": [{"type": "Note", "name": option} for option in options],
                "to": to,
                "cc": cc or [],
                "attributedTo": actor_id
            }
        }
        response = requests.post(f"{actor_id}/outbox", json=question_data, headers=self.headers)
        return response.json()

    def answer_question(self, actor_id: str, question_id: str, answer: str) -> Dict:
        pass
