from rest_framework import serializers

# Mapping MongoDB field types to DRF field types
field_type = {
    'default': serializers.CharField,  # Default serializer for unknown types
    'StringField': serializers.CharField,  # Maps MongoDB StringField to DRF CharField
    'DateTimeField': serializers.DateTimeField,  # Maps MongoDB DateTimeField to DRF DateTimeField
    'FloatField': serializers.FloatField,  # Maps MongoDB FloatField to DRF FloatField
    'IntField': serializers.IntegerField,  # Maps MongoDB IntField to DRF IntegerField
    'ReferenceField': serializers.UUIDField,  # Maps MongoDB ReferenceField to DRF UUIDField
    'BooleanField': serializers.BooleanField,  # Maps MongoDB BooleanField to DRF BooleanField
}


class MongoSerializer(serializers.Serializer):

    # Initialize the serializer with fields dynamically based on the model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get model and fields from Meta class
        model, fields = self.get_model()  # Returns model and fields to include
        model_fields = self.get_model_fields(model, fields)  # Get the field types for the model

        # Loop through fields and dynamically add them to the serializer
        for key, value in model_fields.items():
            field_attr = field_type.get(value, None)  # Get DRF field class based on MongoDB field type
            if field_attr:
                # Set the field as read-only if it's 'id', else make it writable
                self.fields[key] = field_attr(readonly=True if key == 'id' else False)
            else:
                # If the field type is unknown, default to CharField
                self.fields[key] = field_type['default']()

    def create(self, validated_data):
        # Create and save the model instance using the validated data
        return self.Meta.model(**validated_data).save()

    def update(self, instance, validated_data):
        # Update the existing instance with validated data
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    # Get fields for the model based on whether all fields or a subset is specified
    def get_model_fields(self, model, fields):
        model_fields = {}
        for name, field in model._fields.items():
            # If fields is '__all__', include all fields; otherwise, check if the field is in the provided list
            if fields == '__all__' or name in fields:
                model_fields[name] = type(field).__name__  # Store the field type name

        return model_fields

    # Get the model and fields from the Meta class
    def get_model(self):
        # Access Meta from the class
        meta = getattr(self.__class__, 'Meta', None)
        if meta:
            # Return the model and fields defined in Meta
            return meta.get('model', None), meta.get('fields', None)

