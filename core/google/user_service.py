from googleapiclient.discovery import build

from models.user import GoogleUser


def get_user(credential) -> GoogleUser:
    with build(serviceName='oauth2', version='v2', credentials=credential) as service:
        profile = service.userinfo().get().execute()

        google_user = GoogleUser()
        google_user.uname = profile['name']
        google_user.email = profile['email']
        google_user.email_verified = profile['verified_email']
        google_user.id = profile['id']
        google_user.picture = profile['picture']

        return google_user