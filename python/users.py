# This script uses an external Python package called Requests to make its HTTP requests.
# Install this package on your system using pip with the command:
#    pip install requests
import requests
from config import username, password, api_key, base_url

# This is an example User object to create a new administrator account.
user = {
    "username": "john.doe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@happyhills.com",
    "title": "Facility Administrator",
    "password": "Kittens123!!",
    "external_id": "A1125543",
    "enabled": True,
    "roles": [
        # 11 = Administrator
        {"role_id": 11, "subject_id": "A"}
    ]
}

# This creates a Session object which saves headers across requests
s = requests.Session()
s.auth = (username, password)
s.headers.update({'SLTC-Api-Key': api_key})

# Issuing the post to the remote API endpoint with the User payload
response = s.post(base_url + '/Users', json=user)

# Status code 200 == HTTP OK, user was created
if response.status_code == 200:
    print('User created successfully!')
else:
    info = response.json()
    print('Error creating user: {}, {}'.format(response.status_code, info['Message']))
