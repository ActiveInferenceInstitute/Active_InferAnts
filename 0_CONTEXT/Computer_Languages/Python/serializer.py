#!/usr/bin/env python3
"""
Serialization utilities for Active Inference Python implementation
"""

import json
import pickle
import os
import gzip
import bz2
import lzma
import io
from datetime import datetime
from typing import Any, Dict, Optional, Union
import numpy as np


class RestrictedUnpickler(pickle.Unpickler):
    """Unpickler that refuses to instantiate arbitrary classes.

    Pickle can execute arbitrary code when loading untrusted data, so only a small
    allowlist of plain-data types (which is all the agent checkpoint payloads use,
    since numpy arrays are converted to dicts during serialization) is permitted.
    """

    _SAFE_GLOBALS = {
        "builtins": {"str", "int", "float", "bool", "bytes", "list", "dict", "tuple", "set", "frozenset"},
        "numpy": {"int64", "int32", "float64", "float32", "bool_", "ndarray", "dtype"},
        "numpy.core.multiarray": {"scalar", "_reconstruct"},
        "numpy._core.multiarray": {"scalar", "_reconstruct"},
        "numpy.core.numeric": {"_frombuffer"},
        "numpy._core.numeric": {"_frombuffer"},
    }

    def find_class(self, module: str, name: str):
        if name not in self._SAFE_GLOBALS.get(module, set()):
            raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")
        return super().find_class(module, name)


def restricted_loads(data: bytes) -> Any:
    """pickle.loads() restricted to the safe allowlist (RCE guard)."""
    return RestrictedUnpickler(io.BytesIO(data)).load()


class Serializer:
    """Advanced serialization system for Active Inference agents"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.format = self.config.get('format', 'json')  # 'json', 'pickle', 'compressed'
        self.enable_compression = self.config.get('enable_compression', False)
        self.compression_format = self.config.get('compression_format', 'gzip')  # 'gzip', 'bz2', 'lzma'
        self.checkpoint_path = self.config.get('checkpoint_path', './checkpoints/')
        self.max_checkpoints = self.config.get('max_checkpoints', 10)
        self.enable_versioning = self.config.get('enable_versioning', True)
        self.version = self.config.get('version', '2.0.0')

        # Create checkpoint directory
        os.makedirs(self.checkpoint_path, exist_ok=True)

    def serialize(self, agent, options: Optional[Dict[str, Any]] = None) -> Union[str, bytes]:
        """Serialize agent state"""
        options = options or {}

        # Create comprehensive state representation
        state = {
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'agent_type': agent.__class__.__name__,
            'config': getattr(agent, 'config', {}),
            'beliefs': agent.get_beliefs(),
            'history': getattr(agent, 'history', {}),
            'statistics': getattr(agent, 'get_statistics', lambda: {})(),
            'metadata': {
                'serialized_by': 'ActiveInferencePython',
                'format': self.format,
                'compressed': self.enable_compression,
                'numpy_arrays': True,
                **options.get('metadata', {})
            }
        }

        # Handle numpy arrays
        for key, value in state.items():
            if isinstance(value, np.ndarray):
                state[key] = {
                    '_type': 'numpy_array',
                    'data': value.tolist(),
                    'dtype': str(value.dtype),
                    'shape': value.shape
                }
            elif isinstance(value, dict):
                state[key] = self._serialize_nested_dict(value)

        if self.format == 'json':
            return self._serialize_to_json(state)
        elif self.format == 'pickle':
            return self._serialize_to_pickle(state)
        elif self.format == 'compressed':
            return self._serialize_to_compressed(state)
        else:
            raise ValueError(f"Unsupported serialization format: {self.format}")

    def deserialize(self, data: Union[str, bytes], agent_class=None) -> Union[Dict[str, Any], Any]:
        """Deserialize agent state"""
        if isinstance(data, str):
            # JSON format
            state = json.loads(data)
        elif isinstance(data, bytes):
            if self.format == 'pickle':
                state = restricted_loads(data)
            elif self.format == 'compressed':
                state = self._deserialize_from_compressed(data)
            else:
                # Try to decode as UTF-8 first, then as pickle
                try:
                    state = json.loads(data.decode('utf-8'))
                except UnicodeDecodeError:
                    state = restricted_loads(data)
        else:
            raise ValueError("Unknown serialization format")

        # Version compatibility check
        if self.enable_versioning and state.get('version') != self.version:
            print(f"Warning: Version mismatch. Expected {self.version}, got {state.get('version')}")

        # Reconstruct numpy arrays
        state = self._deserialize_nested_dict(state)

        # Create agent if class provided
        if agent_class:
            agent = agent_class(state.get('config', {}))
            agent.set_beliefs(state['beliefs'])
            if hasattr(agent, 'set_history') and 'history' in state:
                agent.set_history(state['history'])
            return agent

        return state

    def _serialize_nested_dict(self, d: dict) -> dict:
        """Recursively serialize nested dictionaries"""
        result = {}
        for key, value in d.items():
            if isinstance(value, np.ndarray):
                result[key] = {
                    '_type': 'numpy_array',
                    'data': value.tolist(),
                    'dtype': str(value.dtype),
                    'shape': value.shape
                }
            elif isinstance(value, dict):
                result[key] = self._serialize_nested_dict(value)
            elif isinstance(value, list):
                result[key] = [self._serialize_nested_item(item) for item in value]
            else:
                result[key] = value
        return result

    def _serialize_nested_item(self, item):
        """Serialize individual nested items"""
        if isinstance(item, np.ndarray):
            return {
                '_type': 'numpy_array',
                'data': item.tolist(),
                'dtype': str(item.dtype),
                'shape': item.shape
            }
        elif isinstance(item, dict):
            return self._serialize_nested_dict(item)
        else:
            return item

    def _deserialize_nested_dict(self, d: dict) -> dict:
        """Recursively deserialize nested dictionaries"""
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                if value.get('_type') == 'numpy_array':
                    result[key] = np.array(value['data'], dtype=value['dtype']).reshape(value['shape'])
                else:
                    result[key] = self._deserialize_nested_dict(value)
            elif isinstance(value, list):
                result[key] = [self._deserialize_nested_item(item) for item in value]
            else:
                result[key] = value
        return result

    def _deserialize_nested_item(self, item):
        """Deserialize individual nested items"""
        if isinstance(item, dict) and item.get('_type') == 'numpy_array':
            return np.array(item['data'], dtype=item['dtype']).reshape(item['shape'])
        elif isinstance(item, dict):
            return self._deserialize_nested_dict(item)
        else:
            return item

    def _serialize_to_json(self, state: dict) -> str:
        """Serialize to JSON"""
        return json.dumps(state, indent=2, default=str)

    def _serialize_to_pickle(self, state: dict) -> bytes:
        """Serialize to pickle format"""
        import pickle
        return pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL)

    def _serialize_to_compressed(self, state: dict) -> bytes:
        """Serialize to compressed format"""
        json_str = json.dumps(state, indent=2, default=str).encode('utf-8')

        if self.compression_format == 'gzip':
            return gzip.compress(json_str)
        elif self.compression_format == 'bz2':
            return bz2.compress(json_str)
        elif self.compression_format == 'lzma':
            return lzma.compress(json_str)
        else:
            raise ValueError(f"Unsupported compression format: {self.compression_format}")

    def _deserialize_from_compressed(self, data: bytes) -> dict:
        """Deserialize from compressed format"""
        if self.compression_format == 'gzip':
            json_str = gzip.decompress(data).decode('utf-8')
        elif self.compression_format == 'bz2':
            json_str = bz2.decompress(data).decode('utf-8')
        elif self.compression_format == 'lzma':
            json_str = lzma.decompress(data).decode('utf-8')
        else:
            raise ValueError(f"Unsupported compression format: {self.compression_format}")

        return json.loads(json_str)

    def save_to_file(self, agent, filename: Optional[str] = None) -> str:
        """Save agent state to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"checkpoint_{timestamp}.{self._get_file_extension()}"

        file_path = os.path.join(self.checkpoint_path, filename)

        # Serialize agent
        serialized_data = self.serialize(agent)

        # Write to file
        if isinstance(serialized_data, str):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(serialized_data)
        else:
            with open(file_path, 'wb') as f:
                f.write(serialized_data)

        # Manage checkpoint rotation
        self._rotate_checkpoints()

        return file_path

    def load_from_file(self, file_path: str, agent_class=None):
        """Load agent state from file"""
        full_path = os.path.abspath(file_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Checkpoint file not found: {full_path}")

        # Read file
        if full_path.endswith('.json') or self.format == 'json':
            with open(full_path, 'r', encoding='utf-8') as f:
                data = f.read()
        else:
            with open(full_path, 'rb') as f:
                data = f.read()

        return self.deserialize(data, agent_class)

    def list_checkpoints(self) -> list:
        """List available checkpoints"""
        if not os.path.exists(self.checkpoint_path):
            return []

        files = []
        extension = self._get_file_extension()

        for filename in os.listdir(self.checkpoint_path):
            if filename.endswith(f'.{extension}'):
                file_path = os.path.join(self.checkpoint_path, filename)
                stat = os.stat(file_path)
                files.append({
                    'filename': filename,
                    'path': file_path,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })

        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files

    def _rotate_checkpoints(self):
        """Rotate checkpoints (remove old ones)"""
        checkpoints = self.list_checkpoints()

        if len(checkpoints) > self.max_checkpoints:
            to_remove = checkpoints[self.max_checkpoints:]
            for checkpoint in to_remove:
                os.remove(checkpoint['path'])

    def _get_file_extension(self) -> str:
        """Get file extension for current format"""
        if self.format == 'json':
            return 'json'
        elif self.format == 'pickle':
            return 'pkl'
        elif self.format == 'compressed':
            if self.compression_format == 'gzip':
                return 'json.gz'
            elif self.compression_format == 'bz2':
                return 'json.bz2'
            elif self.compression_format == 'lzma':
                return 'json.xz'
        return 'dat'

    def validate_serialized_data(self, data: Union[str, bytes]) -> bool:
        """Validate serialized data"""
        try:
            state = self.deserialize(data)

            # Check required fields
            required_fields = ['version', 'beliefs', 'config']
            for field in required_fields:
                if field not in state:
                    print(f"Missing required field: {field}")
                    return False

            # Validate beliefs
            beliefs = state['beliefs']
            if not isinstance(beliefs, (list, np.ndarray)):
                print("Beliefs must be a list or numpy array")
                return False

            if len(beliefs) == 0:
                print("Beliefs cannot be empty")
                return False

            # Check belief normalization
            beliefs_sum = np.sum(beliefs) if isinstance(beliefs, np.ndarray) else sum(beliefs)
            if abs(beliefs_sum - 1.0) > 1e-6:
                print("Warning: Beliefs are not normalized")

            return True

        except Exception as e:
            print(f"Validation failed: {e}")
            return False

    def create_snapshot(self, agent, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a snapshot with metadata"""
        metadata = metadata or {}
        return self.serialize(agent, {
            'metadata': {
                'snapshot': True,
                'description': metadata.get('description', ''),
                'tags': metadata.get('tags', []),
                'user_defined': metadata.get('user_defined', {}),
                **metadata
            }
        })

    def compare_states(self, state1: Union[str, bytes], state2: Union[str, bytes]) -> Dict[str, Any]:
        """Compare two serialized states"""
        s1 = self.deserialize(state1)
        s2 = self.deserialize(state2)

        # Convert beliefs to numpy arrays for comparison
        b1 = np.array(s1['beliefs'])
        b2 = np.array(s2['beliefs'])

        return {
            'beliefs_difference': {
                'different': not np.allclose(b1, b2, atol=1e-6),
                'max_difference': float(np.max(np.abs(b1 - b2))),
                'mean_difference': float(np.mean(np.abs(b1 - b2))),
                'norm_difference': float(np.linalg.norm(b1 - b2))
            },
            'config_difference': self._compare_dicts(s1.get('config', {}), s2.get('config', {})),
            'timestamp_difference': (
                datetime.fromisoformat(s2['timestamp']) - datetime.fromisoformat(s1['timestamp'])
            ).total_seconds(),
            'version_compatible': s1.get('version') == s2.get('version')
        }

    def _compare_dicts(self, d1: dict, d2: dict) -> dict:
        """Compare two dictionaries"""
        differences = {}
        all_keys = set(d1.keys()) | set(d2.keys())

        for key in all_keys:
            if key not in d1:
                differences[key] = {'type': 'missing_in_first', 'value': d2[key]}
            elif key not in d2:
                differences[key] = {'type': 'missing_in_second', 'value': d1[key]}
            elif d1[key] != d2[key]:
                differences[key] = {'type': 'different', 'value1': d1[key], 'value2': d2[key]}

        return differences

    def export_for_sharing(self, agent, format: str = 'base64') -> str:
        """Export agent state for sharing"""
        serialized = self.serialize(agent)
        json_str = json.dumps({
            'version': self.version,
            'format': self.format,
            'data': serialized.decode('utf-8') if isinstance(serialized, bytes) else serialized,
            'timestamp': datetime.now().isoformat()
        })

        if format == 'base64':
            import base64
            return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        else:
            return json_str

    def import_from_shared(self, shared_data: str, agent_class=None, format: str = 'base64'):
        """Import agent state from shared data"""
        if format == 'base64':
            import base64
            json_str = base64.b64decode(shared_data).decode('utf-8')
        else:
            json_str = shared_data

        data = json.loads(json_str)
        return self.deserialize(data['data'], agent_class)

    def get_statistics(self) -> Dict[str, Any]:
        """Get serialization statistics"""
        checkpoints = self.list_checkpoints()

        total_size = sum(cp['size'] for cp in checkpoints)
        avg_size = total_size / len(checkpoints) if checkpoints else 0

        return {
            'total_checkpoints': len(checkpoints),
            'total_size_bytes': total_size,
            'average_size_bytes': avg_size,
            'oldest_checkpoint': checkpoints[-1]['created'] if checkpoints else None,
            'newest_checkpoint': checkpoints[0]['created'] if checkpoints else None,
            'format': self.format,
            'compression': self.enable_compression,
            'versioning': self.enable_versioning
        }


# Create default serializer instance
serializer = Serializer()
