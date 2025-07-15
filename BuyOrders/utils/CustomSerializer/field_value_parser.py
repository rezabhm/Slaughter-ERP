from typing import Any, Optional, Type
from bson import ObjectId
from mongoengine import Document
from mongoengine.errors import DoesNotExist


class FieldValueProcessor:
    """
    Handles processing and validation of MongoEngine field values.
    """

    @staticmethod
    def get_field_value(obj: Any, name: str, field: Any) -> Any:
        """
        Extract and process a field value from a MongoEngine object.

        Args:
            obj: The MongoEngine object to extract the field from.
            name: The name of the field.
            field: The MongoEngine field instance.

        Returns:
            Any: The processed field value or None if extraction fails.
        """
        try:
            value = getattr(obj, name, None)
            if value and field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                return value.to_mongo().to_dict()
            return value
        except Exception as e:
            print(f"Error extracting field {name} from object {obj}: {e}")
            return None

    @staticmethod
    def process_related_field(field: Any, value: Any, related_class: Type[Document]) -> Optional[Any]:
        """
        Process related fields (EmbeddedDocumentField or ReferenceField).

        Args:
            field: The MongoEngine field instance.
            value: The value to process.
            related_class: The related MongoEngine document class.

        Returns:
            Optional[Any]: The processed related field value or None if invalid.
        """
        if isinstance(value, dict):
            try:
                if field.__class__.__name__ == 'ReferenceField':
                    related_instance = related_class.objects(**value).first()
                    if not related_instance:
                        related_instance = related_class(**value)
                        related_instance.save()
                    return related_instance
                return related_class(**value)
            except Exception as e:
                print(f"Error processing related field with value {value}: {e}")
                return None
        if isinstance(value, (str, ObjectId)):
            try:
                return related_class.objects.get(id=value)
            except DoesNotExist:
                return None
        return value

    @staticmethod
    def get_default_value(field: Any, request: Any = None) -> Any:
        """
        Resolve the default value for a MongoEngine field.

        Args:
            field: The MongoEngine field instance.
            request: The HTTP request object (optional).

        Returns:
            Any: The default value for the field or None if not applicable.
        """
        if not hasattr(field, 'default'):
            return None

        default_value = field.default
        try:
            return default_value(request) if callable(default_value) and request else default_value() if callable(default_value) else default_value
        except Exception as e:
            print(f"Error resolving default value for field {field}: {e}")
            return default_value() if callable(default_value) else default_value