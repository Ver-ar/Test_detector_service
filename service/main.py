from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post('/images')
def file_upload(my_file: UploadFile = File(...)):
    print(my_file.file.read()) # так можно считать файл
    return {
        "image_id": 1
    }