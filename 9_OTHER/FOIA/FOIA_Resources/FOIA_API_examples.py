"""
Example 1: Basic FOIA Request
This example shows how to make a basic FOIA request using the Python requests library.
"""

import os
import requests
import json

def make_basic_foia_request():
    url = "https://foia-api.agency.gov/components/234/requests"
    headers = {
        "Content-Type": "application/json",
        "FOIA-API-SECRET": os.environ.get("FOIA_API_SECRET", "your_secret_token_here")
    }

    data = {
        "version": "1.1.0",
        "request_id": 1534,
        "agency": "Department of Justice",
        "agency_component_name": "Office of Information Policy",
        "request_description": "I am seeking records pertaining to the implementation of the FOIA Improvement Act of 2016.",
        "name_first": "John",
        "name_last": "Doe",
        "email": "john.doe@example.com",
        "request_category": "individual"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        print(f"Request created successfully. ID: {result['id']}, Tracking Number: {result['status_tracking_number']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

make_basic_foia_request()

"""
Example 2: FOIA Request with Attachments
This example demonstrates how to include attachments with your FOIA request.
"""

import base64

def make_foia_request_with_attachments():
    url = "https://foia-api.agency.gov/components/234/requests"
    headers = {
        "Content-Type": "application/json",
        "FOIA-API-SECRET": os.environ.get("FOIA_API_SECRET", "your_secret_token_here")
    }

    # Read file and encode it
    with open("supporting_document.pdf", "rb") as file:
        file_data = base64.b64encode(file.read()).decode('utf-8')

    data = {
        "version": "1.1.0",
        "request_id": 1535,
        "agency": "Department of Justice",
        "agency_component_name": "Office of Information Policy",
        "request_description": "I am seeking records related to environmental policies from 2020-2022.",
        "name_first": "Jane",
        "name_last": "Smith",
        "email": "jane.smith@example.com",
        "request_category": "individual",
        "attachments_supporting_documentation": [
            {
                "filename": "supporting_document.pdf",
                "content_type": "application/pdf",
                "filesize": 27556,
                "filedata": file_data
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        print(f"Request with attachment created successfully. ID: {result['id']}, Tracking Number: {result['status_tracking_number']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

make_foia_request_with_attachments()

"""
Example 3: FOIA Request with Fee Waiver and Expedited Processing
This example shows how to request a fee waiver and expedited processing.
"""

def make_foia_request_with_fee_waiver_and_expedited_processing():
    url = "https://foia-api.agency.gov/components/234/requests"
    headers = {
        "Content-Type": "application/json",
        "FOIA-API-SECRET": os.environ.get("FOIA_API_SECRET", "your_secret_token_here")
    }

    data = {
        "version": "1.1.0",
        "request_id": 1536,
        "agency": "Department of Justice",
        "agency_component_name": "Office of Information Policy",
        "request_description": "I am seeking urgent records related to recent policy changes affecting public health.",
        "name_first": "Alex",
        "name_last": "Johnson",
        "email": "alex.johnson@newsorg.com",
        "request_category": "news_media",
        "company_organization": "News Organization Inc.",
        "fee_waiver": "yes",
        "fee_waiver_explanation": "As a journalist, I am requesting these records on behalf of the public and intend to disseminate this information widely.",
        "expedited_processing": "yes",
        "expedited_processing_explanation": "This information is urgently needed to inform the public about immediate health risks."
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        print(f"Request with fee waiver and expedited processing created successfully. ID: {result['id']}, Tracking Number: {result['status_tracking_number']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

make_foia_request_with_fee_waiver_and_expedited_processing()

"""
Example 4: Handling API Errors
This example demonstrates how to handle potential API errors.
"""

def make_foia_request_with_error_handling():
    url = "https://foia-api.agency.gov/components/234/requests"
    headers = {
        "Content-Type": "application/json",
        "FOIA-API-SECRET": os.environ.get("FOIA_API_SECRET", "your_secret_token_here")
    }

    data = {
        "version": "1.1.0",
        "request_id": 1537,
        "agency": "Department of Justice",
        "agency_component_name": "Office of Information Policy",
        "request_description": "I am seeking records about FOIA request processing times.",
        "name_first": "Sam",
        "name_last": "Brown",
        "email": "sam.brown@example.com",
        "request_category": "individual"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        result = response.json()
        print(f"Request created successfully. ID: {result['id']}, Tracking Number: {result['status_tracking_number']}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")

make_foia_request_with_error_handling()

"""
Example 5: How to authenticate your API requests using Python.
"""

def authenticate_api_request():
    url = "https://foia-api.agency.gov/components/234/requests"
    headers = {
        "Content-Type": "application/json",
        "FOIA-API-SECRET": os.environ.get("FOIA_API_SECRET", "your_secret_token_here")
    }

    data = {
        "version": "1.1.0",
        "request_id": 1234,
        "agency": "Department of Example",
        "agency_component_name": "Office of Information",
        "request_description": "Sample FOIA request",
        "name_first": "John",
        "name_last": "Doe",
        "email": "john.doe@example.com",
        "request_category": "individual"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        print(f"Request authenticated and created successfully. ID: {result['id']}")
    else:
        print(f"Authentication failed or error occurred: {response.status_code} - {response.text}")

authenticate_api_request()

def load_api_key_from_env():
    import os
    from dotenv import load_dotenv

    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv('FOIA_API_KEY')

    # Make a request to test the API key
    url = "https://api.foia.gov/api/agency_components"
    headers = {"X-API-Key": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API key is valid!")
    else:
        print(f"API key error. Status code: {response.status_code}")

load_api_key_from_env()

def load_api_key_from_config():
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['FOIA']['api_key']

    url = "https://api.foia.gov/api/agency_components"
    headers = {"X-API-Key": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API key is valid!")
    else:
        print(f"API key error. Status code: {response.status_code}")

load_api_key_from_config()

def load_api_key_from_env_var():
    import os

    api_key = os.environ.get('FOIA_API_KEY')

    if not api_key:
        raise ValueError("FOIA_API_KEY environment variable not set")

    url = "https://api.foia.gov/api/agency_components"
    headers = {"X-API-Key": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API key is valid!")
    else:
        print(f"API key error. Status code: {response.status_code}")

load_api_key_from_env_var()

def load_api_key_from_json():
    import json

    with open('secrets.json') as f:
        secrets = json.load(f)

    api_key = secrets['foia_api_key']

    url = "https://api.foia.gov/api/agency_components"
    headers = {"X-API-Key": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API key is valid!")
    else:
        print(f"API key error. Status code: {response.status_code}")

load_api_key_from_json()

def authenticate_api_request_with_error_handling():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv('FOIA_API_KEY')

    url = "https://api.foia.gov/api/agency_components"
    headers = {"X-API-Key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("API key is valid!")
    except requests.exceptions.HTTPError as err:
        print(f"API key error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")

authenticate_api_request_with_error_handling()