import requests
from requests.auth import HTTPBasicAuth



def get_device_list(dnac, user, pwd):
    port_list = []
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token(dnac, user, pwd) # Get Token
    url = dnac + "api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    device_list = resp.json()
    port_list.extend(print_device_list(device_list))
    return port_list

def print_device_list(device_json):
    port_list = []
    # print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
    #       format("hostname", "mgmt IP", "serial","platformId", "SW Version", "role", "Uptime"))
    for device in device_json['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            port_list.append(device['managementIpAddress'])
            # print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
            #       format(device['hostname'],
            #              device['managementIpAddress'],
            #              serialNumber,
            #              platformId,
            #              device['softwareVersion'],
            #              device['role'], uptime))
    # print(port_list)
    return port_list

def get_auth_token(dnac, user, pwd):
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = dnac + 'dna/system/api/v1/auth/token'       # Endpoint URL
    # print(url)
    resp = requests.post(url, auth=HTTPBasicAuth(user, pwd))  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use


if __name__ == "__main__":
    get_device_list('https://sandboxdnac.cisco.com/', 'devnetuser', 'Cisco123!')
