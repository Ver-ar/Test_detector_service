import requests

filename = 'E:\projects_python\iStock_87827713_LARGE_9.02.01_AM-1024x640-696x435.jpg'


url = 'http://127.0.0.1:8000/images'


files = {'image': (filename, open(filename, 'rb'))}

response = requests.post(url,files=files)

print(response.json())