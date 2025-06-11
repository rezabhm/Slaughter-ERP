import mongoengine
from bson import ObjectId
from typing import Any, Optional, Type


class FieldValueProcessor:
    """Handles processing and validation of field values."""

    @staticmethod
    def get_field_value(obj: Any, name: str, field: Any) -> Any:
        """Extracts and processes field value from an object."""
        value = getattr(obj, name, None)
        if value and field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
            return value.to_mongo().to_dict()
        return value

    @staticmethod
    def process_related_field(field: Any, value: Any, related_class: Type[mongoengine.Document]) -> Optional[Any]:
        """Processes related fields (EmbeddedDocumentField or ReferenceField)."""
        if isinstance(value, dict):
            related_instance = related_class.objects(**value).first()
            if not related_instance:
                related_instance = related_class(**value)
                if field.__class__.__name__ == 'ReferenceField':
                    related_instance.save()
            return related_instance
        elif isinstance(value, (str, ObjectId)):
            try:
                return related_class.objects.get(id=value)
            except related_class.DoesNotExist:
                return None
        return value

    @staticmethod
    def get_default_value(field: Any, request: Any = None) -> Any:
        """Handles default value resolution for fields."""
        if hasattr(field, 'default'):
            default_value = field.default
            try:
                return default_value(request) if callable(default_value) else default_value
            except:
                return default_value() if callable(default_value) else default_value
        return None
