from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def generate_token(user):
    """
        This function is responsible to generate jwt token for logged in user
    """
    #generating token
    refresh_token = TokenObtainPairSerializer().get_token(user)

    #creating refresh token
    refresh = str(refresh_token)

    #creating access token
    access =  str(refresh_token.access_token)

    tokens = {
        'refresh': refresh,
        'access': access,
    }
    return tokens