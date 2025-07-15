from typing import Any, Dict, Type
from drf_yasg import openapi
import mongoengine


class OperationConfig:
    """
    Defines reusable configurations for various API operations
    such as single/bulk POST, PATCH, GET, DELETE.
    """

    CONFIGS = {
        'single_post': {
            'method_type': 'POST',
            'summary': lambda model: f"Create a single {model.__name__}",
            'description': lambda model: f"Creates one {model.__name__} object with provided fields.",
            'status_code': 201,
            'uses_request_body': True
        },
        'bulk_post': {
            'method_type': 'POST',
            'summary': lambda model: f"Create multiple {model.__name__} objects",
            'description': lambda model: f"Creates multiple {model.__name__} objects from a list of data.",
            'status_code': 201,
            'uses_request_body': True
        },
        'single_patch': {
            'method_type': 'PATCH',
            'summary': lambda model: f"Update a single {model.__name__}",
            'description': lambda model: f"Partially updates one {model.__name__} object.",
            'status_code': 200,
            'uses_request_body': True
        },
        'bulk_patch': {
            'method_type': 'PATCH',
            'summary': lambda model: f"Update multiple {model.__name__} objects",
            'description': lambda model: f"Partially updates multiple {model.__name__} objects.",
            'status_code': 200,
            'uses_request_body': True
        },
        'single_delete': {
            'method_type': 'DELETE',
            'summary': lambda model: f"Delete a single {model.__name__}",
            'description': lambda model: f"Deletes one {model.__name__} object by ID.",
            'status_code': 204,
            'uses_request_body': True
        },
        'bulk_delete': {
            'method_type': 'DELETE',
            'summary': lambda model: f"Delete multiple {model.__name__} objects",
            'description': lambda model: f"Deletes multiple {model.__name__} objects by a list of IDs.",
            'status_code': 204,
            'uses_request_body': True
        },
        'single_get': {
            'method_type': 'GET',
            'summary': lambda model: f"Retrieve a single {model.__name__}",
            'description': lambda model: f"Retrieves one {model.__name__} object by ID.",
            'status_code': 200,
            'parameters': [
                openapi.Parameter(
                    'id', openapi.IN_QUERY,
                    description='ID of the object',
                    type=openapi.TYPE_STRING,
                    required=True
                )
            ]
        },
        'bulk_get': {
            'method_type': 'GET',
            'summary': lambda model: f"List multiple {model.__name__} objects",
            'description': lambda model: f"Retrieves a list of {model.__name__} objects with filters.",
            'status_code': 200,
            'parameters': [
                openapi.Parameter(
                    'ids', openapi.IN_QUERY,
                    description='Comma-separated list of IDs',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    required=True,
                    collection_format='csv'
                )
            ]
        }
    }

    @classmethod
    def get_config(cls, method: str, model: Type[mongoengine.Document]) -> Dict[str, Any]:
        """
        Retrieves configuration for a given operation method and model.

        Args:
            method: Operation name (e.g. 'single_post', 'bulk_get').
            model: The MongoEngine model class.

        Returns:
            Dict[str, Any]: Operation metadata including summary, description, method, etc.
        """
        config = cls.CONFIGS.get(method)
        if not config:
            raise ValueError(f"Unsupported method: {method}")
        return {
            'method_type': config['method_type'],
            'summary': config['summary'](model),
            'description': config['description'](model),
            'status_code': config['status_code'],
            'parameters': config.get('parameters', []),
            'uses_request_body': config.get('uses_request_body', False)
        }
