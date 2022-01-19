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


def test_get_asm_app_list():

    url = "https://" + server_name + ".jamfcloud.com/api/v1/auth/token"
    headers = {"Accept": "application/json"}
    response = requests.request(
        "POST", url, headers=headers, auth=(user_name, password)
    ).json()
    token = response.get("token")

    url = (
        "https://" + server_name + ".jamfcloud.com/JSSResource/mobiledeviceapplications"
    )
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}
    result = requests.request("GET", url, headers=headers)
    result_json = result.json()
    first_app_id = result_json.get("mobile_device_applications")[0].get("id")
    assert first_app_id is not None

    with open(
        os.path.join(file_path, "api_response_json", "get_asm_app_list.json"), "w"
    ) as f:
        json.dump(result_json, f)


def test_install_an_app():
    url = "https://" + server_name + ".jamfcloud.com/api/v1/auth/token"
    headers = {"Accept": "application/json"}
    response = requests.request(
        "POST", url, headers=headers, auth=(user_name, password)
    ).json()
    token = response.get("token")

    url = (
        "https://" + server_name + ".jamfcloud.com/JSSResource/mobiledeviceapplications"
    )
    headers = {"Accept": "application/json", "Authorization": "Bearer " + token}
    result = requests.request("GET", url, headers=headers)
    result_json = result.json()
    first_app_id = result_json.get("mobile_device_applications")[0].get("id")

    json_file = open(
        os.path.join(file_path, "json_data", "test_install_app.json"), encoding="utf-8"
    )
    data = json.load(json_file)
    data["mobile_device_application"]["scope"]["mobile_devices"]["mobile_device"][
        "name"
    ] = device_serial_number
    data = dict2xml(data)

    url = (
        "https://"
        + server_name
        + ".jamfcloud.com/JSSResource/mobiledeviceapplications/id/"
        + str(first_app_id)
    )
    headers = {
        "Accept": "application/json",
        "Authorization": "Basic amFtZmFwaXVzZXI6NTJsOVI0cVdUTQ==",
        "Content-Type": "text/plain",
    }
    result = requests.request("PUT", url, headers=headers, data=data)
    assert result.status_code == 201


def test_update_inventory():
    url = "https://" + server_name + ".jamfcloud.com/api/v1/auth/token"
    headers = {"Accept": "application/json"}
    response = requests.request(
        "POST", url, headers=headers, auth=(user_name, password)
    ).json()
    token = response.get("token")

    json_file = open(
        os.path.join(file_path, "json_data", "test_update_inventory.json"),
        encoding="utf-8",
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

    result = requests.request("POST", url, headers=headers, data=data)
    assert result.status_code == 201


if __name__ == "__main__":
    test_get_asm_app_list()
    test_install_an_app()
    test_update_inventory()
