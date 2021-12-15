# Test_detector_service
## Детектор очередей на кассе
____

*Сделано в виртуальной среде*

1. Создаем FastAPI и делаем POST-запрос: 

```python

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/items/")
async def create_item(image: bytes) -> dict:
    return {"image_id" :  1}
```

2. Конкретизируем запрос:

```python

import requests

filename = "E:\projects_python\iStock_87827713_LARGE_9.02.01_AM-1024x640-696x435.jpg"


url = 'http://127.0.0.1:8000/images'


files = {'my_file': (filename, open(filename, 'rb'))}

response = requests.post(url,files=files)

print(response.json())

```