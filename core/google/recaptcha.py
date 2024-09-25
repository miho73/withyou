from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment, Event, CreateAssessmentRequest

from config import config

parant = "projects/with-430118"


def verify_recaptcha(token: str, client_ip: str, action: str):
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    assessment = Assessment(
        event = Event(
            token = token,
            site_key = config['security']['recaptcha']['site_key'],
            user_ip_address = client_ip,
            expected_action = action
        )
    )

    request = CreateAssessmentRequest(
        assessment = assessment,
        parent = parant
    )

    response = client.create_assessment(request)

    if response.token_properties.valid and response.risk_analysis.score >= 0.7:
        return True
    else:
        return False
