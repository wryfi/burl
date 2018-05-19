from rest_framework import serializers


class SerializerEnumField(serializers.Field):
    def __init__(self, *args, **kwargs):
        self.enum = kwargs.pop('enum')
        super(SerializerEnumField, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        return instance.label

    def to_internal_value(self, data):
        if not self.enum:
            raise serializers.ValidationError('You must specify an enum in the field\'s kwargs')
        try:
            data = int(data)
            return data
        except ValueError:
            for choice in self.enum.choices():
                if choice[1] == data:
                    return choice[0]