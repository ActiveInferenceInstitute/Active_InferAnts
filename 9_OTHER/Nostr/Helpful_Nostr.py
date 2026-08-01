import json
import time
from typing import List, Dict, Any, Optional, Tuple
from nostr.event import Event
from nostr.key import PrivateKey, PublicKey
from nostr.relay_manager import RelayManager
from nostr.filter import Filter, Filters
from nostr.message_type import ClientMessageType
import asyncio
import aiohttp
import base64
import logging
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NostrHelper:
    def __init__(self):
        self.relay_manager = None

    @staticmethod
    def create_event(private_key: str, kind: int, content: str, tags: List[List[str]] = None, created_at: int = None) -> Event:
        """
        Create a Nostr event according to NIP-01.
        
        :param private_key: The private key as a hex string
        :param kind: The event kind (integer)
        :param content: The event content
        :param tags: Optional list of tags
        :param created_at: Optional timestamp for the event (defaults to current time)
        :return: A signed Nostr event
        """
        pk = PrivateKey(bytes.fromhex(private_key))
        event = Event(
            public_key=pk.public_key.hex(),
            created_at=created_at or int(time.time()),
            kind=kind,
            tags=tags or [],
            content=content
        )
        event.sign(pk.hex())
        return event

    async def publish_event(self, event: Event, timeout: float = 5.0) -> Dict[str, bool]:
        """
        Publish an event to all connected relays and wait for confirmations (NIP-01).
        
        :param event: The Event to publish
        :param timeout: Maximum time to wait for confirmations (in seconds)
        :return: A dictionary of relay URLs and their confirmation status
        """
        if not self.relay_manager:
            raise ValueError("Relay manager not initialized. Call setup_relay_manager first.")

        confirmations = {}
        tasks = []

        for relay in self.relay_manager.relays.values():
            task = asyncio.create_task(relay.publish_event(event))
            tasks.append(task)

        try:
            done, pending = await asyncio.wait(tasks, timeout=timeout)
            for task in done:
                result = task.result()
                if isinstance(result, tuple):
                    relay_url, success = result
                    confirmations[relay_url] = success
            for task in pending:
                task.cancel()
        except asyncio.TimeoutError:
            logger.warning(f"Timeout occurred while publishing event: {event.id}")

        logger.info(f"Published event: {event.id}")
        logger.info(f"Confirmations: {confirmations}")
        return confirmations

    async def subscribe_to_events(self, filters: Filters, timeout: float = 30.0) -> List[Event]:
        """
        Subscribe to events matching the given filters with a timeout (NIP-01).
        
        :param filters: The Filters to apply
        :param timeout: Maximum time to wait for events (in seconds)
        :return: A list of matching events
        """
        if not self.relay_manager:
            raise ValueError("Relay manager not initialized. Call setup_relay_manager first.")

        subscription_id = self.relay_manager.add_subscription(filters)
        events = []
        
        try:
            async with asyncio.timeout(timeout):
                while True:
                    message = await self.relay_manager.receive_message()
                    if message.type == ClientMessageType.EVENT:
                        events.append(message.event)
                    elif message.type == ClientMessageType.EOSE:
                        break
        except asyncio.TimeoutError:
            logger.warning(f"Subscription timed out after {timeout} seconds")
        finally:
            self.relay_manager.close_subscription(subscription_id)
        
        return events

    async def setup_relay_manager(self, relay_urls: List[str], connection_timeout: float = 5.0) -> None:
        """
        Set up a RelayManager with the given relay URLs and attempt connections (NIP-01).
        
        :param relay_urls: List of relay URLs to connect to
        :param connection_timeout: Maximum time to wait for connections (in seconds)
        """
        self.relay_manager = RelayManager()
        for url in relay_urls:
            self.relay_manager.add_relay(url)
        
        connection_tasks = [relay.connect() for relay in self.relay_manager.relays.values()]
        
        try:
            await asyncio.wait_for(asyncio.gather(*connection_tasks), timeout=connection_timeout)
        except asyncio.TimeoutError:
            logger.error(f"Timeout occurred while connecting to relays")
        
        connected_relays = [url for url, relay in self.relay_manager.relays.items() if relay.connected]
        logger.info(f"Connected to relays: {connected_relays}")

    @staticmethod
    def create_filter(authors: List[str] = None, kinds: List[int] = None, since: int = None, until: int = None, 
                      limit: int = None, ids: List[str] = None, tags: Dict[str, List[str]] = None) -> Filter:
        """
        Create a comprehensive Filter object for querying events (NIP-01).
        
        :param authors: List of public keys to filter by
        :param kinds: List of event kinds to filter by
        :param since: Unix timestamp to filter events after
        :param until: Unix timestamp to filter events before
        :param limit: Maximum number of events to return
        :param ids: List of event IDs to filter by
        :param tags: Dictionary of tag names and lists of values to filter by
        :return: A configured Filter object
        """
        filter_dict = {}
        if authors:
            filter_dict['authors'] = authors
        if kinds:
            filter_dict['kinds'] = kinds
        if since:
            filter_dict['since'] = since
        if until:
            filter_dict['until'] = until
        if limit:
            filter_dict['limit'] = limit
        if ids:
            filter_dict['ids'] = ids
        if tags:
            for tag_name, tag_values in tags.items():
                filter_dict[f'#{tag_name}'] = tag_values
        
        return Filter(**filter_dict)

    @staticmethod
    def parse_event_content(event: Event) -> Dict[str, Any]:
        """
        Parse the content of an event as JSON, with fallback to raw content.
        
        :param event: The Event object to parse
        :return: A dictionary of the parsed content or raw content
        """
        try:
            return json.loads(event.content)
        except json.JSONDecodeError:
            logger.warning(f"Unable to parse event content as JSON. Event ID: {event.id}")
            return {"raw_content": event.content}

    @staticmethod
    def get_event_tags(event: Event, tag_name: str) -> List[str]:
        """
        Get all values for a specific tag from an event (NIP-01).
        
        :param event: The Event object to search
        :param tag_name: The name of the tag to find
        :return: A list of tag values
        """
        return [tag[1] for tag in event.tags if tag[0] == tag_name]

    @staticmethod
    def create_encrypted_dm(sender_private_key: str, recipient_public_key: str, content: str) -> Event:
        """
        Create an encrypted direct message event (NIP-04).
        
        :param sender_private_key: The sender's private key as a hex string
        :param recipient_public_key: The recipient's public key as a hex string
        :param content: The message content to encrypt
        :return: An encrypted direct message Event
        """
        sender_pk = PrivateKey(bytes.fromhex(sender_private_key))
        recipient_pk = PublicKey(bytes.fromhex(recipient_public_key))
        
        shared_secret = sender_pk.compute_shared_secret(recipient_pk)
        
        # Use HKDF to derive a symmetric key
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'nip04',
            backend=default_backend()
        )
        sym_key = hkdf.derive(shared_secret)
        
        # Encrypt the content
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_content = content.encode('utf-8') + b'\0' * (16 - (len(content) % 16))
        encrypted_content = encryptor.update(padded_content) + encryptor.finalize()
        
        # Encode the encrypted content
        encoded_content = base64.b64encode(iv + encrypted_content).decode('utf-8')
        
        return NostrHelper.create_event(
            private_key=sender_private_key,
            kind=4,  # Encrypted Direct Message
            content=encoded_content,
            tags=[['p', recipient_public_key]]
        )

    @staticmethod
    def decrypt_dm(private_key: str, event: Event) -> str:
        """
        Decrypt a direct message event (NIP-04).
        
        :param private_key: The recipient's private key as a hex string
        :param event: The encrypted Event object
        :return: The decrypted message content
        """
        pk = PrivateKey(bytes.fromhex(private_key))
        sender_pubkey = event.public_key
        sender_pk = PublicKey(bytes.fromhex(sender_pubkey))
        
        shared_secret = pk.compute_shared_secret(sender_pk)
        
        # Use HKDF to derive the symmetric key
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'nip04',
            backend=default_backend()
        )
        sym_key = hkdf.derive(shared_secret)
        
        # Decode and decrypt the content
        decoded_content = base64.b64decode(event.content)
        iv = decoded_content[:16]
        encrypted_content = decoded_content[16:]
        
        cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_content = decryptor.update(encrypted_content) + decryptor.finalize()
        
        # Remove padding
        return decrypted_content.rstrip(b'\0').decode('utf-8')

    async def fetch_user_metadata(self, pubkey: str) -> Optional[Dict[str, Any]]:
        """
        Fetch user metadata for a given public key (NIP-01).
        
        :param pubkey: The public key of the user
        :return: A dictionary containing user metadata or None if not found
        """
        filters = Filters([self.create_filter(authors=[pubkey], kinds=[0], limit=1)])
        events = await self.subscribe_to_events(filters)
        
        if events:
            return self.parse_event_content(events[0])
        return None

    async def create_and_publish_reaction(self, private_key: str, event_id: str, reaction: str = "+") -> Event:
        """
        Create and publish a reaction event (NIP-25).
        
        :param private_key: The private key of the user creating the reaction
        :param event_id: The ID of the event being reacted to
        :param reaction: The reaction content (default is "+")
        :return: The published reaction Event
        """
        reaction_event = self.create_event(
            private_key=private_key,
            kind=7,  # Reaction
            content=reaction,
            tags=[['e', event_id]]
        )
        await self.publish_event(reaction_event)
        return reaction_event

    async def create_and_publish_repost(self, private_key: str, event_id: str, relay_url: str) -> Event:
        """
        Create and publish a repost event (NIP-18).
        
        :param private_key: The private key of the user creating the repost
        :param event_id: The ID of the event being reposted
        :param relay_url: The URL of the relay where the original event was found
        :return: The published repost Event
        """
        repost_event = self.create_event(
            private_key=private_key,
            kind=6,  # Repost
            content="",
            tags=[['e', event_id, relay_url, 'mention']]
        )
        await self.publish_event(repost_event)
        return repost_event

    async def fetch_event_replies(self, event_id: str) -> List[Event]:
        """
        Fetch replies to a specific event (NIP-10).
        
        :param event_id: The ID of the event to fetch replies for
        :return: A list of reply Events
        """
        filters = Filters([self.create_filter(kinds=[1], tags={'e': [event_id]})])
        return await self.subscribe_to_events(filters)

    async def create_and_publish_long_form_content(self, private_key: str, title: str, content: str, 
                                                   summary: str = "", image_url: str = "", published_at: int = None) -> Event:
        """
        Create and publish a long-form content event (NIP-23).
        
        :param private_key: The private key of the author
        :param title: The title of the article
        :param content: The main content of the article (in Markdown)
        :param summary: Optional summary of the article
        :param image_url: Optional URL for the article's image
        :param published_at: Optional timestamp for when the article was published
        :return: The published long-form content Event
        """
        article_data = {
            "title": title,
            "content": content,
            "published_at": published_at or int(time.time())
        }
        if summary:
            article_data["summary"] = summary
        if image_url:
            article_data["image"] = image_url
        
        long_form_event = self.create_event(
            private_key=private_key,
            kind=30023,  # Long-form content
            content=json.dumps(article_data),
            tags=[['d', title]]  # Use title as unique identifier
        )
        await self.publish_event(long_form_event)
        return long_form_event

    @staticmethod
    async def upload_file_to_nostr_build(file_path: str) -> Optional[str]:
        """
        Upload a file to nostr.build and return the URL.
        
        :param file_path: Path to the file to upload
        :return: URL of the uploaded file or None if upload failed
        """
        upload_url = "https://nostr.build/upload.php"
        
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as file:
                data = aiohttp.FormData()
                data.add_field('fileToUpload', file)
                async with session.post(upload_url, data=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        return result.strip()  # The URL of the uploaded file
                    else:
                        logger.error(f"Failed to upload file. Status code: {response.status}")
                        return None

    @staticmethod
    def create_nip05_verification_event(private_key: str, username: str, domain: str) -> Event:
        """
        Create a NIP-05 verification event.
        
        :param private_key: The private key of the user
        :param username: The username part of the NIP-05 identifier
        :param domain: The domain part of the NIP-05 identifier
        :return: A NIP-05 verification Event
        """
        nip05_identifier = f"{username}@{domain}"
        return NostrHelper.create_event(
            private_key=private_key,
            kind=0,  # Metadata event
            content=json.dumps({"nip05": nip05_identifier}),
            tags=[]
        )

    @staticmethod
    async def verify_nip05(identifier: str) -> Optional[str]:
        """
        Verify a NIP-05 identifier and return the public key if valid.
        
        :param identifier: The NIP-05 identifier (e.g., "username@example.com")
        :return: The verified public key or None if verification fails
        """
        username, domain = identifier.split('@')
        url = f"https://{domain}/.well-known/nostr.json?name={username}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if "names" in data and username in data["names"]:
                        return data["names"][username]
        return None

    @staticmethod
    def create_zap_request(private_key: str, recipient_pubkey: str, amount_sats: int, content: str = "") -> Event:
        """
        Create a Zap request event (NIP-57).
        
        :param private_key: The private key of the user creating the Zap request
        :param recipient_pubkey: The public key of the recipient
        :param amount_sats: The amount of satoshis to zap
        :param content: Optional content for the Zap request
        :return: A Zap request Event
        """
        zap_request = NostrHelper.create_event(
            private_key=private_key,
            kind=9734,  # Zap request
            content=content,
            tags=[
                ['p', recipient_pubkey],
                ['amount', str(amount_sats)]
            ]
        )
        return zap_request

def create_event(private_key: str, kind: int, content: str, tags: List[List[str]] = None, created_at: int = None) -> Event:
    """
    Create a Nostr event.
    
    :param private_key: The private key as a hex string
    :param kind: The event kind (integer)
    :param content: The event content
    :param tags: Optional list of tags
    :param created_at: Optional timestamp for the event (defaults to current time)
    :return: A signed Nostr event
    """
    pk = PrivateKey(bytes.fromhex(private_key))
    event = Event(
        public_key=pk.public_key.hex(),
        created_at=created_at or int(time.time()),
        kind=kind,
        tags=tags or [],
        content=content
    )
    event.sign(pk.hex())
    return event

async def publish_event(relay_manager: RelayManager, event: Event, timeout: float = 5.0) -> Dict[str, bool]:
    """
    Publish an event to all connected relays and wait for confirmations.
    
    :param relay_manager: The RelayManager instance
    :param event: The Event to publish
    :param timeout: Maximum time to wait for confirmations (in seconds)
    :return: A dictionary of relay URLs and their confirmation status
    """
    confirmations = {}
    tasks = []

    for relay in relay_manager.relays.values():
        task = asyncio.create_task(relay.publish_event(event))
        tasks.append(task)

    try:
        done, pending = await asyncio.wait(tasks, timeout=timeout)
        for task in done:
            result = task.result()
            if isinstance(result, tuple):
                relay_url, success = result
                confirmations[relay_url] = success
        for task in pending:
            task.cancel()
    except asyncio.TimeoutError:
        print(f"Timeout occurred while publishing event: {event.id}")

    print(f"Published event: {event.id}")
    print(f"Confirmations: {confirmations}")
    return confirmations

async def subscribe_to_events(relay_manager: RelayManager, filters: Filters, timeout: float = 30.0) -> List[Event]:
    """
    Subscribe to events matching the given filters with a timeout.
    
    :param relay_manager: The RelayManager instance
    :param filters: The Filters to apply
    :param timeout: Maximum time to wait for events (in seconds)
    :return: A list of matching events
    """
    subscription_id = relay_manager.add_subscription(filters)
    events = []
    
    try:
        async with asyncio.timeout(timeout):
            while True:
                message = await relay_manager.receive_message()
                if message.type == ClientMessageType.EVENT:
                    events.append(message.event)
                elif message.type == ClientMessageType.EOSE:
                    break
    except asyncio.TimeoutError:
        print(f"Subscription timed out after {timeout} seconds")
    finally:
        relay_manager.close_subscription(subscription_id)
    
    return events

async def setup_relay_manager(relay_urls: List[str], connection_timeout: float = 5.0) -> RelayManager:
    """
    Set up a RelayManager with the given relay URLs and attempt connections.
    
    :param relay_urls: List of relay URLs to connect to
    :param connection_timeout: Maximum time to wait for connections (in seconds)
    :return: A configured RelayManager instance
    """
    relay_manager = RelayManager()
    for url in relay_urls:
        relay_manager.add_relay(url)
    
    connection_tasks = [relay.connect() for relay in relay_manager.relays.values()]
    
    try:
        await asyncio.wait_for(asyncio.gather(*connection_tasks), timeout=connection_timeout)
    except asyncio.TimeoutError:
        print(f"Timeout occurred while connecting to relays")
    
    connected_relays = [url for url, relay in relay_manager.relays.items() if relay.connected]
    print(f"Connected to relays: {connected_relays}")
    
    return relay_manager

def create_filter(authors: List[str] = None, kinds: List[int] = None, since: int = None, until: int = None, 
                  limit: int = None, ids: List[str] = None, tags: Dict[str, List[str]] = None) -> Filter:
    """
    Create a comprehensive Filter object for querying events.
    
    :param authors: List of public keys to filter by
    :param kinds: List of event kinds to filter by
    :param since: Unix timestamp to filter events after
    :param until: Unix timestamp to filter events before
    :param limit: Maximum number of events to return
    :param ids: List of event IDs to filter by
    :param tags: Dictionary of tag names and lists of values to filter by
    :return: A configured Filter object
    """
    filter_dict = {}
    if authors:
        filter_dict['authors'] = authors
    if kinds:
        filter_dict['kinds'] = kinds
    if since:
        filter_dict['since'] = since
    if until:
        filter_dict['until'] = until
    if limit:
        filter_dict['limit'] = limit
    if ids:
        filter_dict['ids'] = ids
    if tags:
        for tag_name, tag_values in tags.items():
            filter_dict[f'#{tag_name}'] = tag_values
    
    return Filter(**filter_dict)

def parse_event_content(event: Event) -> Dict[str, Any]:
    """
    Parse the content of an event as JSON, with fallback to raw content.
    
    :param event: The Event object to parse
    :return: A dictionary of the parsed content or raw content
    """
    try:
        return json.loads(event.content)
    except json.JSONDecodeError:
        print(f"Warning: Unable to parse event content as JSON. Event ID: {event.id}")
        return {"raw_content": event.content}

def get_event_tags(event: Event, tag_name: str) -> List[str]:
    """
    Get all values for a specific tag from an event.
    
    :param event: The Event object to search
    :param tag_name: The name of the tag to find
    :return: A list of tag values
    """
    return [tag[1] for tag in event.tags if tag[0] == tag_name]

def create_encrypted_dm(sender_private_key: str, recipient_public_key: str, content: str) -> Event:
    """
    Create an encrypted direct message event.
    
    :param sender_private_key: The sender's private key as a hex string
    :param recipient_public_key: The recipient's public key as a hex string
    :param content: The message content to encrypt
    :return: An encrypted direct message Event
    """
    sender_pk = PrivateKey(bytes.fromhex(sender_private_key))
    recipient_pk = PublicKey(bytes.fromhex(recipient_public_key))
    
    encrypted_content = sender_pk.encrypt_message(content, recipient_pk)
    
    return create_event(
        private_key=sender_private_key,
        kind=4,  # Encrypted Direct Message
        content=encrypted_content,
        tags=[['p', recipient_public_key]]
    )

def decrypt_dm(private_key: str, event: Event) -> str:
    """
    Decrypt a direct message event.
    
    :param private_key: The recipient's private key as a hex string
    :param event: The encrypted Event object
    :return: The decrypted message content
    """
    pk = PrivateKey(bytes.fromhex(private_key))
    sender_pubkey = event.public_key
    
    return pk.decrypt_message(event.content, sender_pubkey)

async def fetch_user_metadata(relay_manager: RelayManager, pubkey: str) -> Optional[Dict[str, Any]]:
    """
    Fetch user metadata for a given public key.
    
    :param relay_manager: The RelayManager instance
    :param pubkey: The public key of the user
    :return: A dictionary containing user metadata or None if not found
    """
    filters = Filters([create_filter(authors=[pubkey], kinds=[0], limit=1)])
    events = await subscribe_to_events(relay_manager, filters)
    
    if events:
        return parse_event_content(events[0])
    return None

async def create_and_publish_reaction(relay_manager: RelayManager, private_key: str, event_id: str, reaction: str = "+") -> Event:
    """
    Create and publish a reaction event.
    
    :param relay_manager: The RelayManager instance
    :param private_key: The private key of the user creating the reaction
    :param event_id: The ID of the event being reacted to
    :param reaction: The reaction content (default is "+")
    :return: The published reaction Event
    """
    reaction_event = create_event(
        private_key=private_key,
        kind=7,  # Reaction
        content=reaction,
        tags=[['e', event_id]]
    )
    await publish_event(relay_manager, reaction_event)
    return reaction_event

async def create_and_publish_repost(relay_manager: RelayManager, private_key: str, event_id: str, relay_url: str) -> Event:
    """
    Create and publish a repost event.
    
    :param relay_manager: The RelayManager instance
    :param private_key: The private key of the user creating the repost
    :param event_id: The ID of the event being reposted
    :param relay_url: The URL of the relay where the original event was found
    :return: The published repost Event
    """
    repost_event = create_event(
        private_key=private_key,
        kind=6,  # Repost
        content="",
        tags=[['e', event_id, relay_url, 'mention']]
    )
    await publish_event(relay_manager, repost_event)
    return repost_event

async def fetch_event_replies(relay_manager: RelayManager, event_id: str) -> List[Event]:
    """
    Fetch replies to a specific event.
    
    :param relay_manager: The RelayManager instance
    :param event_id: The ID of the event to fetch replies for
    :return: A list of reply Events
    """
    filters = Filters([create_filter(kinds=[1], tags={'e': [event_id]})])
    return await subscribe_to_events(relay_manager, filters)

async def create_and_publish_long_form_content(relay_manager: RelayManager, private_key: str, title: str, content: str, 
                                               summary: str = "", image_url: str = "", published_at: int = None) -> Event:
    """
    Create and publish a long-form content event (NIP-23).
    
    :param relay_manager: The RelayManager instance
    :param private_key: The private key of the author
    :param title: The title of the article
    :param content: The main content of the article (in Markdown)
    :param summary: Optional summary of the article
    :param image_url: Optional URL for the article's image
    :param published_at: Optional timestamp for when the article was published
    :return: The published long-form content Event
    """
    article_data = {
        "title": title,
        "content": content,
        "published_at": published_at or int(time.time())
    }
    if summary:
        article_data["summary"] = summary
    if image_url:
        article_data["image"] = image_url
    
    long_form_event = create_event(
        private_key=private_key,
        kind=30023,  # Long-form content
        content=json.dumps(article_data),
        tags=[['d', title]]  # Use title as unique identifier
    )
    await publish_event(relay_manager, long_form_event)
    return long_form_event

async def upload_file_to_nostr_build(file_path: str) -> Optional[str]:
    """
    Upload a file to nostr.build and return the URL.
    
    :param file_path: Path to the file to upload
    :return: URL of the uploaded file or None if upload failed
    """
    upload_url = "https://nostr.build/upload.php"
    
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as file:
            data = aiohttp.FormData()
            data.add_field('fileToUpload', file)
            async with session.post(upload_url, data=data) as response:
                if response.status == 200:
                    result = await response.text()
                    return result.strip()  # The URL of the uploaded file
                else:
                    print(f"Failed to upload file. Status code: {response.status}")
                    return None

def create_nip05_verification_event(private_key: str, username: str, domain: str) -> Event:
    """
    Create a NIP-05 verification event.
    
    :param private_key: The private key of the user
    :param username: The username part of the NIP-05 identifier
    :param domain: The domain part of the NIP-05 identifier
    :return: A NIP-05 verification Event
    """
    nip05_identifier = f"{username}@{domain}"
    return create_event(
        private_key=private_key,
        kind=0,  # Metadata event
        content=json.dumps({"nip05": nip05_identifier}),
        tags=[]
    )

async def verify_nip05(identifier: str) -> Optional[str]:
    """
    Verify a NIP-05 identifier and return the public key if valid.
    
    :param identifier: The NIP-05 identifier (e.g., "username@example.com")
    :return: The verified public key or None if verification fails
    """
    username, domain = identifier.split('@')
    url = f"https://{domain}/.well-known/nostr.json?name={username}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if "names" in data and username in data["names"]:
                    return data["names"][username]
    return None

def create_zap_request(private_key: str, recipient_pubkey: str, amount_sats: int, content: str = "") -> Event:
    """
    Create a Zap request event (NIP-57).
    
    :param private_key: The private key of the user creating the Zap request
    :param recipient_pubkey: The public key of the recipient
    :param amount_sats: The amount of satoshis to zap
    :param content: Optional content for the Zap request
    :return: A Zap request Event
    """
    zap_request = create_event(
        private_key=private_key,
        kind=9734,  # Zap request
        content=content,
        tags=[
            ['p', recipient_pubkey],
            ['amount', str(amount_sats)]
        ]
    )
    return zap_request

def create_badge_definition(private_key: str, name: str, description: str, image_url: str) -> Event:
    """
    Create a badge definition event (NIP-58).
    
    :param private_key: The private key of the badge creator
    :param name: The name of the badge
    :param description: A description of the badge
    :param image_url: URL of the badge image
    """
    pass

# Example usage
async def example_usage():
    relay_urls = ["wss://relay.damus.io", "wss://relay.nostr.info"]
    relay_manager = setup_relay_manager(relay_urls)
    
    # Create and publish an event
    private_key = PrivateKey().hex()
    event = create_event(private_key, kind=1, content="Hello, Nostr!")
    await publish_event(relay_manager, event)
    
    # Subscribe to events
    filters = Filters([create_filter(kinds=[1], limit=10)])
    events = await subscribe_to_events(relay_manager, filters)
    
    for event in events:
        print(f"Received event: {event.id}")
        print(f"Content: {parse_event_content(event)}")
    
    relay_manager.close_connections()

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
