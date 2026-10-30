"""
Question 1: Comprehensive JSON Handler with Custom Type Serialization
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- Standard JSON serialization (dumps, dump) and deserialization (loads, load)
- Robust error handling for json.JSONDecodeError with custom JSONParsingError
- Custom json.JSONEncoder subclassing for datetime, UUID, set, and object instances
- Round-trip deserialization using object_hook for ISO-8601 timestamps
- UTF-8 file I/O operations
"""

import json
import uuid
import datetime
from typing import Any, Dict


class JSONParsingError(Exception):
    """Raised when JSON parsing or decoding fails."""
    pass


class CustomJSONEncoder(json.JSONEncoder):
    """
    Extends json.JSONEncoder to support datetime, UUID, sets, and custom objects.
    """

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, (set, frozenset)):
            return sorted(list(obj))
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)


class JSONHandler:
    """
    High-level JSON utility handling serialization, deserialization,
    file I/O, and custom type conversion.
    """

    @staticmethod
    def serialize_to_string(data: Any, indent: int = 2, sort_keys: bool = True) -> str:
        """Serializes data using CustomJSONEncoder."""
        return json.dumps(data, indent=indent, sort_keys=sort_keys, cls=CustomJSONEncoder)

    @staticmethod
    def deserialize_from_string(json_str: str) -> Any:
        """Parses standard JSON string into Python objects, catching errors."""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as err:
            raise JSONParsingError(f"Failed to parse JSON string: {err.msg} at line {err.lineno} col {err.colno}") from err

    @staticmethod
    def save_to_file(filepath: str, data: Any, indent: int = 2) -> None:
        """Saves data to a JSON file using UTF-8 encoding."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, sort_keys=True, cls=CustomJSONEncoder)

    @staticmethod
    def load_from_file(filepath: str) -> Any:
        """Loads data from a JSON file using UTF-8 encoding."""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def deserialize_with_hook(cls, json_str: str) -> Any:
        """
        Deserializes JSON string using object_hook to restore ISO-8601 strings
        for date/timestamp keys into native datetime instances.
        """
        def datetime_decoder(dct: Dict[str, Any]) -> Dict[str, Any]:
            for key, val in dct.items():
                if isinstance(val, str) and ("time" in key.lower() or "created_at" in key.lower() or "date" in key.lower()):
                    try:
                        dct[key] = datetime.datetime.fromisoformat(val)
                    except (ValueError, TypeError):
                        pass
            return dct

        try:
            return json.loads(json_str, object_hook=datetime_decoder)
        except json.JSONDecodeError as err:
            raise JSONParsingError(f"Failed to decode JSON with hook: {err}") from err


if __name__ == "__main__":
    handler = JSONHandler()

    print("=== 1. Custom Type Serialization ===")
    raw_record = {
        "user_id": uuid.UUID("12345678-1234-5678-1234-567812345678"),
        "username": "alex_dev",
        "created_at": datetime.datetime(2026, 10, 26, 14, 30, 0),
        "roles": {"admin", "developer"},
        "is_active": True,
        "metadata": None,
    }

    json_output = handler.serialize_to_string(raw_record, indent=2)
    print("Serialized JSON String:")
    print(json_output)

    print("\n=== 2. Round-Trip Deserialization with Object Hook ===")
    recovered_obj = handler.deserialize_with_hook(json_output)
    print(f"Recovered created_at Type: {type(recovered_obj['created_at'])}")
    print(f"Recovered created_at Value: {recovered_obj['created_at']}")
    print(f"Recovered user_id: '{recovered_obj['user_id']}'")
    print(f"Recovered roles: {recovered_obj['roles']}")

    print("\n=== 3. Error Handling for Corrupt JSON ===")
    try:
        handler.deserialize_from_string("{corrupted_json: 123")
    except JSONParsingError as err:
        print(f"Caught expected JSONParsingError:\n  {err}")
