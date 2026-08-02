import requests


response = requests.post(

    "http://127.0.0.1:8000/api/v1/investigation/1102"

)


print(response.status_code)

print(
    response.json()
)