# import os #to get environment variables
# import requests #to make http requests inside python code

from get_token import get_token
from verify_token import verify_token

# AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")


def handler(event, context):
    print(event)
    print(context)
    token = get_token(event)
    id_token = verify_token(token)
    print(id_token)
    # userinfo = requests.get(
    #     'https://' + AUTH0_DOMAIN + '/userinfo', 
    #     headers={"Authorization": "Bearer " + token}
    # ).json()
    if id_token and id_token.get('permissions'):
        scopes = '|'.join(id_token['permissions'])
        policy = generate_policy(
            id_token['sub'], 
            'Allow', 
            event['methodArn'],
            scopes=scopes
        )
        return policy
    else:
        policy = generate_policy(
            id_token['sub'],
            "Deny",
            event['methodArn']
        )
        return policy
#it tells if the prinicpal_id can be the user or manager or anyone
#can invoke the api
def generate_policy(principal_id, effect, resource, scopes=None):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
    if scopes:
        policy['context'] = {'scopes': scopes}
    return policy
