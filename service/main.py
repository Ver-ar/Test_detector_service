from fastapi import FastAPI, File

import detect_faces

def count_faces():
    count_1 = detect_faces.count()
    return count_1

count_faces()

app = FastAPI()

@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:
    return {"image_id" : 1, "faces" : {count_1}}