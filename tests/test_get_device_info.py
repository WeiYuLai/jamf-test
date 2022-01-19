from dotenv import load_dotenv
import requests
import json
from dict2xml import dict2xml
import os


file_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(file_path, "..", ".env")
load_dotenv(env_path)

server_name = os.getenv("SEVER_NAME")
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
device_serial_number = os.getenv("DEVICE_SERIALNUMBER")


def test_get_device_info():
    url = "https://" + server_name + ".jamfcloud.com/api/v1/auth/token"
    headers = {"Accept": "application/json"}
    response = requests.request(
        "POST", url, headers=headers, auth=(user_name, password)
    ).json()
    token = response.get("token")

    url = (
        "https://"
        + server_name
        + ".jamfcloud.com/JSSResource/mobiledevices/serialnumber/"
        + device_serial_number
    )
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}
    response = requests.request("GET", url, headers=headers)
    device_info = response.json()
    assert device_info is not None

    with open(
        os.path.join(file_path, "api_response_json", "get_device_info.json"), "w"
    ) as f:
        json.dump(response.json(), f)


if __name__ == "__main__":
    test_get_device_info()
