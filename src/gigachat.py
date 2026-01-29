import requests
import uuid

# Это твой ключ из личного кабинета (PERS)
AUTHORIZATION_KEY = (
    "MDE5YjUxMzMtOGQ4Ni03NmJhLWJjOWEtMjM3Y2I5Zjk4NTRm"
    "OmNjMzFlMTk3LTAxNzUtNDFhZC04NzdlLTYyNTY3NzM0NjI3MA=="
)

headers = {
    "Authorization": f"Basic {AUTHORIZATION_KEY}",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "RqUID": str(uuid.uuid4())
}

# Самое важное — scope должен быть PERS!
data = "scope=GIGACHAT_API_PERS"

response = requests.post(
    "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
    headers=headers,
    data=data,
    verify=False  # потом замени на сертификат
)

print("STATUS:", response.status_code)
print("TEXT:", response.text)