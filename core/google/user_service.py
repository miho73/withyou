import logging

from googleapiclient.discovery import build

from models.user import Role
from schemas.user import GoogleUser

log = logging.getLogger(__name__)

def get_user(credential) -> GoogleUser:
    with build(serviceName='oauth2', version='v2', credentials=credential) as service:
        profile = service.userinfo().get().execute()

        log.debug("Got user profile from Google. profile=\"{profile}\"".format(profile=profile))
        google_user = GoogleUser(
            uname = profile['name'],
            email = profile['email'],
            email_verified = profile['verified_email'],
            id = profile['id'],
            picture = profile['picture']
        )

        return google_user