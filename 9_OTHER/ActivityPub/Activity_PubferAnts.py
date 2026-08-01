import random
import math
import json
from typing import List, Dict, Tuple, Any
import requests
from Helpful_ActivityPub import ActivityPubHelper

class AntAgent:
    def __init__(self, actor_id: str, position: Tuple[float, float]):
        self.actor_id = actor_id
        self.position = position
        self.energy = 100.0
        self.pheromone = 0.0
        self.followers: List[str] = []
        self.following: List[str] = []
        self.liked_objects: List[str] = []
        self.blocked_actors: List[str] = []

    def move(self, direction: Tuple[float, float]):
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])
        self.energy -= 1.0
        self.pheromone = max(0, self.pheromone - 0.1)

    def deposit_pheromone(self, amount: float):
        self.pheromone += amount

class Environment:
    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.food_sources: List[Tuple[float, float]] = []
        self.pheromone_map: Dict[Tuple[int, int], float] = {}

    def add_food_source(self, position: Tuple[float, float]):
        self.food_sources.append(position)

    def update_pheromone(self, position: Tuple[float, float], amount: float):
        grid_pos = (int(position[0]), int(position[1]))
        self.pheromone_map[grid_pos] = self.pheromone_map.get(grid_pos, 0) + amount

    def get_pheromone(self, position: Tuple[float, float]) -> float:
        grid_pos = (int(position[0]), int(position[1]))
        return self.pheromone_map.get(grid_pos, 0)

class ActivityPubAntSimulation:
    def __init__(self, num_ants: int, env_size: Tuple[int, int], base_url: str, access_token: str):
        self.environment = Environment(env_size)
        self.ants: List[AntAgent] = []
        self.ap_helper = ActivityPubHelper(base_url, access_token)

        for i in range(num_ants):
            ant_id = f"ant_{i}"
            position = (random.uniform(0, env_size[0]), random.uniform(0, env_size[1]))
            self.ants.append(AntAgent(ant_id, position))
            self.create_ant_actor(ant_id, i, base_url)

        self.environment.add_food_source((env_size[0] * 0.8, env_size[1] * 0.8))
        self.environment.add_food_source((env_size[0] * 0.2, env_size[1] * 0.2))

    def create_ant_actor(self, ant_id: str, index: int, base_url: str):
        actor_data = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
                {"manuallyApprovesFollowers": "as:manuallyApprovesFollowers"}
            ],
            "type": "Person",
            "id": f"{base_url}/actors/{ant_id}",
            "name": f"Ant {index}",
            "preferredUsername": f"ant{index}",
            "summary": f"I'm ant number {index} in the ActivityPub Ant Simulation",
            "inbox": f"{base_url}/actors/{ant_id}/inbox",
            "outbox": f"{base_url}/actors/{ant_id}/outbox",
            "followers": f"{base_url}/actors/{ant_id}/followers",
            "following": f"{base_url}/actors/{ant_id}/following",
            "liked": f"{base_url}/actors/{ant_id}/liked",
            "streams": [
                {
                    "id": f"{base_url}/actors/{ant_id}/main",
                    "type": "OrderedCollection",
                    "name": "Main Stream"
                },
                {
                    "id": f"{base_url}/actors/{ant_id}/pheromones",
                    "type": "OrderedCollection",
                    "name": "Pheromone Trail"
                }
            ],
            "endpoints": {
                "sharedInbox": f"{base_url}/shared_inbox"
            },
            "publicKey": {
                "id": f"{base_url}/actors/{ant_id}#main-key",
                "owner": f"{base_url}/actors/{ant_id}",
                "publicKeyPem": "..."  # Generate and add actual public key here
            },
            "manuallyApprovesFollowers": False,
            "attachment": [
                {
                    "type": "PropertyValue",
                    "name": "Species",
                    "value": "Formicidae"
                },
                {
                    "type": "PropertyValue",
                    "name": "Role",
                    "value": "Forager"
                }
            ],
            "icon": {
                "type": "Image",
                "mediaType": "image/png",
                "url": f"{base_url}/images/ant_avatar.png"
            }
        }
        self.ap_helper.create_actor(ant_id, json.dumps(actor_data))

    def run_simulation(self, num_steps: int):
        for step in range(num_steps):
            for ant in self.ants:
                self.update_ant(ant)

            if step % 10 == 0:
                self.publish_state()

    def update_ant(self, ant: AntAgent):
        possible_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        best_move = max(possible_moves, key=lambda move: self.evaluate_move(ant, move))
        ant.move(best_move)

        for food_source in self.environment.food_sources:
            if math.dist(ant.position, food_source) < 1.0:
                ant.deposit_pheromone(10.0)
                self.environment.update_pheromone(ant.position, 10.0)
                self.publish_ant_action(ant, "found_food")
                break

        self.update_ant_profile(ant)
        self.publish_pheromone_update(ant)
        self.check_ant_interactions(ant)

    def evaluate_move(self, ant: AntAgent, move: Tuple[float, float]) -> float:
        new_position = (ant.position[0] + move[0], ant.position[1] + move[1])
        
        if not (0 <= new_position[0] < self.environment.size[0] and 0 <= new_position[1] < self.environment.size[1]):
            return float('-inf')

        pheromone_level = self.environment.get_pheromone(new_position)
        distance_to_food = min(math.dist(new_position, food) for food in self.environment.food_sources)

        return pheromone_level * 2 - distance_to_food + random.uniform(-0.1, 0.1)

    def publish_state(self):
        state_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Note",
            "attributedTo": f"{self.ap_helper.base_url}/actors/simulation",
            "content": f"Simulation state: {len(self.ants)} ants, {len(self.environment.food_sources)} food sources",
            "ants": [{"id": f"{self.ap_helper.base_url}/actors/{ant.actor_id}", "position": ant.position, "energy": ant.energy} for ant in self.ants],
            "foodSources": self.environment.food_sources,
            "pheromoneMap": {f"{k[0]},{k[1]}": v for k, v in self.environment.pheromone_map.items()}
        }
        self.ap_helper.create_note("simulation", json.dumps(state_data), ["https://www.w3.org/ns/activitystreams#Public"])

    def publish_ant_action(self, ant: AntAgent, action: str):
        action_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Note",
            "attributedTo": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "content": f"Ant {ant.actor_id} {action} at position {ant.position}",
            "to": ["https://www.w3.org/ns/activitystreams#Public"]
        }
        self.ap_helper.create_note(ant.actor_id, json.dumps(action_data), ["https://www.w3.org/ns/activitystreams#Public"])

    def ant_interaction(self, ant1: AntAgent, ant2: AntAgent):
        interaction_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Note",
            "attributedTo": f"{self.ap_helper.base_url}/actors/{ant1.actor_id}",
            "content": f"Ant {ant1.actor_id} interacted with Ant {ant2.actor_id}",
            "to": [f"{self.ap_helper.base_url}/actors/{ant2.actor_id}"]
        }
        self.ap_helper.create_note(ant1.actor_id, json.dumps(interaction_data), [f"{self.ap_helper.base_url}/actors/{ant2.actor_id}"])

    def update_ant_profile(self, ant: AntAgent):
        updates = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Update",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": {
                "id": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
                "type": "Person",
                "summary": f"Energy: {ant.energy:.2f}, Position: ({ant.position[0]:.2f}, {ant.position[1]:.2f})",
                "attachment": [
                    {
                        "type": "PropertyValue",
                        "name": "Energy",
                        "value": f"{ant.energy:.2f}"
                    },
                    {
                        "type": "PropertyValue",
                        "name": "Position",
                        "value": f"({ant.position[0]:.2f}, {ant.position[1]:.2f})"
                    },
                    {
                        "type": "PropertyValue",
                        "name": "Pheromone",
                        "value": f"{ant.pheromone:.2f}"
                    }
                ]
            }
        }
        self.ap_helper.update_actor(ant.actor_id, json.dumps(updates))

    def get_ant_followers(self, ant: AntAgent):
        return self.ap_helper.get_followers(f"{self.ap_helper.base_url}/actors/{ant.actor_id}")

    def get_ant_following(self, ant: AntAgent):
        return self.ap_helper.get_following(f"{self.ap_helper.base_url}/actors/{ant.actor_id}")

    def ant_follow(self, follower: AntAgent, followed: AntAgent):
        follow_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Follow",
            "actor": f"{self.ap_helper.base_url}/actors/{follower.actor_id}",
            "object": f"{self.ap_helper.base_url}/actors/{followed.actor_id}"
        }
        self.ap_helper.follow_actor(follower.actor_id, json.dumps(follow_data))
        follower.following.append(followed.actor_id)
        followed.followers.append(follower.actor_id)

    def ant_unfollow(self, follower: AntAgent, followed: AntAgent):
        unfollow_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Undo",
            "actor": f"{self.ap_helper.base_url}/actors/{follower.actor_id}",
            "object": {
                "type": "Follow",
                "actor": f"{self.ap_helper.base_url}/actors/{follower.actor_id}",
                "object": f"{self.ap_helper.base_url}/actors/{followed.actor_id}"
            }
        }
        self.ap_helper.unfollow_actor(follower.actor_id, json.dumps(unfollow_data))
        follower.following.remove(followed.actor_id)
        followed.followers.remove(follower.actor_id)

    def ant_like_action(self, ant: AntAgent, liked_object_id: str):
        like_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Like",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": liked_object_id
        }
        self.ap_helper.like_object(ant.actor_id, json.dumps(like_data))
        ant.liked_objects.append(liked_object_id)

    def ant_unlike_action(self, ant: AntAgent, unliked_object_id: str):
        unlike_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Undo",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": {
                "type": "Like",
                "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
                "object": unliked_object_id
            }
        }
        self.ap_helper.unlike_object(ant.actor_id, json.dumps(unlike_data))
        ant.liked_objects.remove(unliked_object_id)

    def get_ant_inbox(self, ant: AntAgent):
        return self.ap_helper.get_inbox(f"{self.ap_helper.base_url}/actors/{ant.actor_id}")

    def get_ant_outbox(self, ant: AntAgent):
        return self.ap_helper.get_outbox(f"{self.ap_helper.base_url}/actors/{ant.actor_id}")

    def ant_announce(self, ant: AntAgent, object_id: str):
        announce_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Announce",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": object_id,
            "to": ["https://www.w3.org/ns/activitystreams#Public"]
        }
        self.ap_helper.announce_object(ant.actor_id, json.dumps(announce_data))

    def ant_delete(self, ant: AntAgent, object_id: str):
        delete_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Delete",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": object_id
        }
        self.ap_helper.delete_object(ant.actor_id, json.dumps(delete_data))

    def ant_update(self, ant: AntAgent, object_id: str, updated_data: Dict[str, Any]):
        update_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Update",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": {
                "id": object_id,
                **updated_data
            }
        }
        self.ap_helper.update_object(ant.actor_id, json.dumps(update_data))

    def ant_block(self, ant: AntAgent, blocked_ant: AntAgent):
        block_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Block",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": f"{self.ap_helper.base_url}/actors/{blocked_ant.actor_id}"
        }
        self.ap_helper.block_actor(ant.actor_id, json.dumps(block_data))

    def ant_undo(self, ant: AntAgent, object_id: str):
        undo_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Undo",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": object_id
        }
        self.ap_helper.undo_action(ant.actor_id, json.dumps(undo_data))

    def get_ant_followers_collection(self, ant: AntAgent):
        return self.ap_helper.get_followers_collection(f"{self.ap_helper.base_url}/actors/{ant.actor_id}")

    def get_ant_following_collection(self, ant: AntAgent):
        return self.ap_helper.get_following_collection(f"{self.ap_helper.base_url}/actors/{ant.actor_id}")

    def ant_add(self, ant: AntAgent, object_id: str, target_collection: str):
        add_data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Add",
            "actor": f"{self.ap_helper.base_url}/actors/{ant.actor_id}",
            "object": object_id,
            "target": target_collection
        }
        self.ap_helper.add_to_collection(ant.actor_id, json.dumps(add_data))

    def ant_remove(self, ant: AntAgent, object_id: str, target_collection: str):
        """Remove an object from a collection."""
        self.ap_helper.remove_from_collection(ant.actor_id, object_id, target_collection)

if __name__ == "__main__":
    simulation = ActivityPubAntSimulation(num_ants=10, env_size=(100, 100), base_url="https://example.com/activitypub", access_token="your_access_token_here")
    simulation.run_simulation(num_steps=1000)
