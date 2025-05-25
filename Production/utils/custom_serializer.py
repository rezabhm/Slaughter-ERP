import mongoengine
from bson import ObjectId


class CustomSerializer:

    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, object_=None, many=False, parse_data=True):

        self.queryset = object_ if many else [object_]
        self.many = many
        self.data = []

        if parse_data:
            self.pars_object()

    def create(self, request):
        model_list = []
        for validated_data in self.queryset:
            data = {}
            meta = getattr(self.__class__, 'Meta', None)
            model = getattr(meta, 'model', None)
            fields = getattr(meta, 'fields', [])

            if model:
                for name, field in model._fields.items():
                    if name == 'id':
                        continue

                    if name in fields or fields == '__all__':
                        value = validated_data.get(name, None)

                        if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                            related_class = field.document_type

                            if isinstance(value, dict):
                                related_instance = related_class.objects(**value).first()
                                if not related_instance:
                                    related_instance = related_class(**value)
                                    if field.__class__.__name__ == 'ReferenceField':
                                        related_instance.save()

                                value = related_instance

                            elif isinstance(value, (str, ObjectId)):
                                try:
                                    value = related_class.objects.get(id=value)
                                except related_class.DoesNotExist:
                                    value = None

                        if value is None and hasattr(field, 'default'):
                            default_value = field.default
                            value = default_value(request) if callable(default_value) else default_value

                        data[name] = value

                    else:
                        default_value = None
                        if hasattr(field, 'default'):
                            default_value = field.default
                            default_value = default_value(request) if callable(default_value) else default_value

                        data[name] = default_value

                instance = model(**data)
                instance.save()
                model_list.append(instance)

        self.data = []
        self.queryset = model_list
        self.pars_object()

    def update(self, validated_data):
        meta = getattr(self.__class__, 'Meta', None)
        serializer_fields = getattr(meta, 'fields', [])

        for instance, validated in zip(self.queryset, validated_data):
            fields_dict = {name: field for name, field in instance._fields.items()}

            for key, value in validated.items():
                if (key in serializer_fields or serializer_fields == '__all__') and key in fields_dict:
                    field = fields_dict[key]

                    if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                        related_class = field.document_type

                        if isinstance(value, dict):
                            related_instance = related_class.objects(**value).first()
                            if not related_instance:
                                related_instance = related_class(**value)
                                if field.__class__.__name__ == 'ReferenceField':
                                    related_instance.save()

                            value = related_instance

                        elif isinstance(value, (str, ObjectId)):
                            try:
                                value = related_class.objects.get(id=value)
                            except related_class.DoesNotExist:
                                value = None

                    setattr(instance, key, value)

            instance.save()

        self.data = []
        self.pars_object()

    def pars_object(self):

        for obj in self.queryset:
            obj_dict = self.obj_to_dict(obj)
            obj_dict = self.to_represent(obj_dict)

            self.data.append(obj_dict)

        if len(self.data) == 1:
            self.data = self.data[0]

    def obj_to_dict(self, obj):

        meta = getattr(self.__class__, 'Meta', None)
        if meta:

            fields = getattr(meta, 'fields', '__all__')

            model = getattr(meta, 'model', None)

            model_fields = model._fields.items() if model else []
            return {

                name: self.get_object_fields_value(obj, name, field) for name, field in model_fields if fields == '__all__' or name in fields

            }

    @staticmethod
    def get_object_fields_value(obj, name, field):

        value = getattr(obj, name, None)

        if value:
            if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                return value.to_mongo().to_dict()

        return value

    def to_represent(self, obj_dict):

        return obj_dict
