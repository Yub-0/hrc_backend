from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import MyUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role

        return token


class TokenDecoder():
    def token_decode(request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            user, token = response
            return token.payload


