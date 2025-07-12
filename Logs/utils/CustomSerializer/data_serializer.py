from bson import ObjectId
from typing import Any, Dict

from utils.CustomSerializer.field_value_parser import FieldValueProcessor
from utils.CustomSerializer.meta_config import MetaConfig


class DataSerializer:
    """Handles conversion of objects to dictionary representation."""

    def __init__(self, meta: MetaConfig):
        self.meta = meta

    def to_dict(self, obj: Any) -> Dict[str, Any]:
        """Converts an object to dictionary based on Meta configuration."""
        fields = self.meta.fields
        model = self.meta.model
        model_fields = model._fields.items() if model else []
        return {
            name: FieldValueProcessor.get_field_value(obj, name, field)
            for name, field in model_fields
            if fields == '__all__' or name in fields or 'id' in name
        }

    def correct_value(self, value: Any) -> Any:
        """Recursively corrects values in dictionaries or lists."""
        if isinstance(value, dict):
            return self.correct_dict(value)
        elif isinstance(value, list):
            return [self.correct_value(dt) for dt in value]
        elif isinstance(value, ObjectId):
            return str(value)
        return value

    def correct_dict(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Corrects dictionary values recursively."""
        corrected_data = {key: self.correct_value(value) for key, value in obj.items()}
        return corrected_data
