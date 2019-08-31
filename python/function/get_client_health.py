import requests
from requests.auth import HTTPBasicAuth
from function.dnac_config import DNAC_USER, DNAC_PASSWORD


def get_client_health():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token() # Get Token
    url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/flow-analysis"
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    print(resp)
    client_health = resp.json()
    print(client_health)


def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD))  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use


if __name__ == "__main__":
    get_client_health()