from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainUserPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return super().create(validated_data)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = self.user.id
        return data
