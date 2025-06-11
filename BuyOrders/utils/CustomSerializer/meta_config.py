import mongoengine
from typing import List, Optional, Union, Type


class MetaConfig:
    """Configuration class for serializer metadata."""
    model: Optional[Type[mongoengine.Document]] = None
    fields: Union[str, List[str]] = '__all__'
