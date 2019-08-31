#! /usr/bin/env python

from path_trace.env_lab import apicem
# from env_lab import apicem
from time import sleep
import json
import requests
import sys
import urllib3
from requests.auth import HTTPBasicAuth

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
              'content-type': "application/json",
              'x-auth-token': ""
          }


def apic_login(host, username, password):
    """
    Use the REST API to Log into an DNA_CENTER and retrieve token
    """
    url = "https://{}/api/system/v1/auth/token".format(host)
    # payload = {"username": username, "password": password}

    # Make Login request and return the response body
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password),
                                headers=headers, verify=False)
    # print response
    return response.json()["Token"]

def interface_details(apic, ticket, id):
    """
    Use the REST API to retrieve details about an interface based on id.
    """
    url = "https://{}/api/v1/interface/{}".format(apic, id)
    headers["x-auth-token"] = ticket

    response = requests.request("GET", url, headers=headers, verify=False)
    return response.json()["response"]

def print_interface_details(interface):
    """
    Print to screen interesting details about an interface.
    Input Paramters are:
      interface: dictionary object of an interface returned from APIC-EM
    Standard Output Details:
      Port Name - (portName)
      Interface Type (interfaceType) - Physical/Virtual
      Admin Status - (adminStatus)
      Operational Status (status)
      Media Type - (mediaType)
      Speed - (speed)
      Duplex Setting (duplex)
      Port Mode (portMode) - access/trunk/routed
      Interface VLAN - (vlanId)
      Voice VLAN - (voiceVlan)
    """

    # Print Standard Details
    print("Port Name: {}".format(interface["portName"]))
    print("Interface Type: {}".format(interface["interfaceType"]))
    print("Admin Status: {}".format(interface["adminStatus"]))
    print("Operational Status: {}".format(interface["status"]))
    print("Media Type: {}".format(interface["mediaType"]))
    print("Speed: {}".format(interface["speed"]))
    print("Duplex Setting: {}".format(interface["duplex"]))
    print("Port Mode: {}".format(interface["portMode"]))
    print("Interface VLAN: {}".format(interface["vlanId"]))
    print("Voice VLAN: {}".format(interface["voiceVlan"]))

    # Blank line at the end
    print("")


def run_flow_analysis(apic, ticket, source_ip, destination_ip):
    """
    Use the REST API to initiate a Flow Analysis (Path Trace) from a given
    source_ip to destination_ip.  Function will wait for analysis to complete,
    and return the results.
    """
    base_url = "https://{}/api/v1/flow-analysis".format(apic)
    headers["x-auth-token"] = ticket

    # initiate flow analysis
    body = {"destIP": destination_ip, "sourceIP": source_ip}
    initiate_response = requests.post(base_url, headers=headers, verify=False,
                                      json=body)

    # Verify successfully initiated.  If not error and exit
    if initiate_response.status_code != 202:
        print("Error: Flow Analysis Initiation Failed")
        print(initiate_response.text)
        sys.exit(1)

    # Check status of analysis and wait until completed
    flowAnalysisId = initiate_response.json()["response"]["flowAnalysisId"]
    detail_url = base_url + "/{}".format(flowAnalysisId)
    detail_response = requests.get(detail_url, headers=headers, verify=False)
    while not detail_response.json()["response"]["request"]["status"] == "COMPLETED":  # noqa: E501
        print("Flow analysis not complete yet, waiting 5 seconds")
        sleep(1)
        detail_response = requests.get(detail_url, headers=headers,
                                       verify=False)

    # Return the flow analysis details
    return detail_response.json()["response"]


def print_flow_analysis_details(flow_analysis):
    str1 = ''
    """
    Print to screen interesting details about the flow analysis.
    Input Parameters are:
      flow_analysis: dictionary object of a flow analysis returned from APIC-EM
    """
    hops = flow_analysis["networkElementsInfo"]

    print("Number of Hops from Source to Destination: {}".format(len(hops)))
    print()

    # Print Details per hop
    print("Flow Details: ")
    # Hop 1 (index 0) and the last hop (index len - 1) represent the endpoints
    for i, hop in enumerate(hops):
        if i == 0 or i == len(hops) - 1:
            continue

        print("*" * 40)
        print("Hop {}: Network Device {}".format(i, hop["name"]))
        str1 = str1 + "Hop: " + i + " Network Device :" + hop["name"]
        # If the hop is "UNKNOWN" continue along
        if hop["name"] == "UNKNOWN":
            print()
            continue

        print("Device IP: {}".format(hop["ip"]))
        print("Device Role: {}".format(hop["role"]))

        # If type is an Access Point, skip interface details
        if hop["type"] == "Unified AP":
            continue
        print()

        # Step 4: Are there any problems along the path?
        # Print details about each interface
        print("Ingress Interface")
        print("-" * 20)
        ingress = interface_details(apicem["host"], login,
                                    hop["ingressInterface"]["physicalInterface"]["id"])  # noqa: E501
        print_interface_details(ingress)
        print("Egress Interface")
        print("-" * 20)
        egress = interface_details(apicem["host"], login,
                                   hop["egressInterface"]["physicalInterface"]["id"])  # noqa: E501
        print_interface_details(egress)

    # Print blank line at end
    print("")
    return str1
# Entry point for program

def path_trace_main(source_port, des_port):
    source_port = '10.10.22.66'
    des_port = '10.10.22.98'
    list1 = []


    source_ip = source_port
    destination_ip = des_port
    # Print Starting message
    print("Running Troubleshooting Script for ")
    print("      Source IP:      {} ".format(source_ip))
    print("      Destination IP: {}".format(destination_ip))
    print("")

    # Log into the APIC-EM Controller to get Ticket
    login = apic_login(apicem["host"], apicem["username"], apicem["password"])

    # Step 3: What path does the traffic take?
    # Step 4: Are there any problems along the path?
    # Run a Flow Analysis for Source/Destionation
    print("Running Flow Analysis from {} to {}".format(source_ip, destination_ip))  # noqa: E501
    print("-" * 55)
    flow_analysis = run_flow_analysis(apicem["host"], login,
                                      source_ip,
                                      destination_ip)

    # Print Out Details
    list1.append(print_flow_analysis_details(flow_analysis))
    return list1

if __name__ == '__main__':
    path_trace_main('', '')
