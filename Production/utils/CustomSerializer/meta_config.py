from typing import List, Optional, Union, Type
from mongoengine import Document


class MetaConfig:
    """
    Configuration class for defining serializer metadata, specifying the MongoEngine model and fields.
    """

    model: Optional[Type[Document]] = None
    fields: Union[str, List[str]] = '__all__'
