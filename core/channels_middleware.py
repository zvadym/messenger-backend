import jwt
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user(pk):
    return User.objects.get(pk=pk)


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom token auth middleware
    """

    def populate_scope(self, scope):
        # Get the token
        data = parse_qs(scope['query_string'].decode('utf8'))

        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            token = data['token'][0]
            UntypedToken(token)
        except (InvalidToken, TokenError, KeyError) as e:
            # Token is invalid
            # TODO: raise some websocket's extension
            return None

        #  Then token is valid, decode it
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # Will return a dictionary like -
        # {
        #     "token_type": "access",
        #     "exp": 1568770772,
        #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
        #     "user_id": 6
        # }
        scope['user_id'] = decoded_data['user_id']

        # Add it to the scope if it's not there already
        if 'user' not in scope:
            scope['user'] = UserLazyObject()

        # Return the inner application directly and let it run everything else
        # return self.inner(dict(scope, user=user))

    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(pk=scope['user_id'])
