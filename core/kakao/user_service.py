import httpx

from config import config
from schemas.user import KakaoUser

def get_user(access_token) -> KakaoUser:
    with httpx.Client() as cli:
        resp = cli.post(
            url=config['auth']['kakao']['user_info_uri'],
            headers={
                'Authorization': 'Bearer {access_token}'.format(access_token=access_token),
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            },
            params={
                'secure_resource': True
            },
        )

        if resp.status_code != 200:
            raise Exception("Failed to fetch user info from Kakao")

        user_info = resp.json()
        profile = user_info.get('kakao_account').get('profile')
        print(user_info)
        kakao_user = KakaoUser(
            id=str(user_info.get('id')),
            email_verified=False,
            email=None,
            uname=profile.get('nickname'),
            picture=profile.get('profile_image_url')
        )

        return kakao_user