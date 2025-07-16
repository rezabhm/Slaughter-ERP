from typing import Any, Dict, List
from bson import ObjectId
from utils.CustomSerializer.field_value_parser import FieldValueProcessor
from utils.CustomSerializer.meta_config import MetaConfig


class DataSerializer:
    """
    Handles conversion of MongoEngine objects to dictionary representation.
    """

    def __init__(self, meta: MetaConfig) -> None:
        """
        Initialize the serializer with Meta configuration.

        Args:
            meta: MetaConfig object containing model and field information.
        """
        self.meta = meta

    def to_dict(self, obj: Any) -> Dict[str, Any]:
        """
        Convert an object to a dictionary based on Meta configuration.

        Args:
            obj: The MongoEngine object to serialize.

        Returns:
            Dict[str, Any]: Dictionary representation of the object.
        """
        model = self.meta.model
        fields = self.meta.fields
        if not model:
            return {}

        return {
            name: FieldValueProcessor.get_field_value(obj, name, field)
            for name, field in model._fields.items()
            if fields == '__all__' or name in fields or name == 'id'
        }

    def correct_dict(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively correct dictionary values, handling nested structures and ObjectId.

        Args:
            obj: The dictionary to process.

        Returns:
            Dict[str, Any]: Corrected dictionary with processed values.
        """
        return {key: self._correct_value(value) for key, value in obj.items()}

    def _correct_value(self, value: Any) -> Any:
        """
        Recursively correct values in dictionaries, lists, or ObjectId instances.

        Args:
            value: The value to correct.

        Returns:
            Any: The corrected value.
        """
        if isinstance(value, dict):
            return self.correct_dict(value)
        if isinstance(value, list):
            return [self._correct_value(item) for item in value]
        if isinstance(value, ObjectId):
            return str(value)
        return value