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


def test_erase_device():
    url = "https://" + server_name + ".jamfcloud.com/api/v1/auth/token"
    headers = {"Accept": "application/json"}
    response = requests.request(
        "POST", url, headers=headers, auth=(user_name, password)
    ).json()
    token = response.get("token")

    json_file = open(
        os.path.join(file_path, "json_data", "test_erase_device.json"), encoding="utf-8"
    )
    data = json.load(json_file)
    data["mobile_device_command"]["mobile_devices"]["mobile_device"][
        "name"
    ] = device_serial_number
    data = dict2xml(data)

    url = (
        "https://"
        + server_name
        + ".jamfcloud.com/JSSResource/mobiledevicecommands/command"
    )
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}

    result = requests.request("POST", url, headers=headers, data=data.encode())
    assert result.status_code == 201


if __name__ == "__main__":
    test_erase_device()
