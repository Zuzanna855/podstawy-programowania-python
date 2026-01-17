import cv2
import numpy as np
import requests
import os
import tarfile
import time
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="People Counter API (Draw Boxes)")

MODEL_DIR = "model_data"
OUTPUT_DIR = "processed_images"
MODEL_WEIGHTS = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
MODEL_CONFIG = os.path.join(MODEL_DIR, "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

URL_WEIGHTS_TAR = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"
URL_CONFIG = "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"

net = None


def download_file(url, path):
    print(f"Pobieranie: {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass
        raise e


def setup_model():
    global net
    if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR)

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    try:
        if not os.path.exists(MODEL_CONFIG): download_file(URL_CONFIG, MODEL_CONFIG)
        if not os.path.exists(MODEL_WEIGHTS):
            tar_path = os.path.join(MODEL_DIR, "model.tar.gz")
            download_file(URL_WEIGHTS_TAR, tar_path)
            with tarfile.open(tar_path, "r:gz") as tar:
                found = False
                for member in tar.getmembers():
                    if member.name.endswith("frozen_inference_graph.pb"):
                        member.name = os.path.basename(member.name)
                        tar.extract(member, path=MODEL_DIR)
                        os.rename(os.path.join(MODEL_DIR, os.path.basename(member.name)), MODEL_WEIGHTS)
                        found = True
                        break
                if not found: raise Exception("Błąd archiwum .pb")
            time.sleep(1)
            try:
                os.remove(tar_path)
            except:
                pass

        print("Inicjalizacja OpenCV DNN...")
        net = cv2.dnn.readNetFromTensorflow(MODEL_WEIGHTS, MODEL_CONFIG)
        print("Model załadowany pomyślnie!")

    except Exception as e:
        print(f"\n!!! BŁĄD SETUPU !!!: {e}")
        net = None


@app.on_event("startup")
async def startup_event():
    setup_model()


def process_image(image, source_name="image"):
    global net
    if net is None:
        setup_model()
    if net is None:
        raise HTTPException(status_code=500, detail="Model nie został załadowany.")

    height, width = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    people_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            class_id = int(detections[0, 0, i, 1])

            if class_id == 1:
                people_count += 1


                box_x = int(detections[0, 0, i, 3] * width)
                box_y = int(detections[0, 0, i, 4] * height)
                box_w = int(detections[0, 0, i, 5] * width)
                box_h = int(detections[0, 0, i, 6] * height)

                cv2.rectangle(image, (box_x, box_y), (box_w, box_h), (0, 255, 0), 2)

                cv2.putText(image, f"Person {confidence:.2f}", (box_x, box_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    unique_name = f"result_{uuid.uuid4().hex[:8]}.jpg"
    save_path = os.path.join(OUTPUT_DIR, unique_name)

    cv2.imwrite(save_path, image)

    return people_count, save_path


def decode_image(data):
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None: raise ValueError
    return img


class CountResponse(BaseModel):
    source: str
    people_count: int
    saved_path: str


@app.get("/", include_in_schema=False)
def root(): return RedirectResponse(url="/docs")


@app.get("/count/local", response_model=CountResponse)
def count_local(path: str):
    if not os.path.exists(path): raise HTTPException(404, "Brak pliku")
    img = cv2.imread(path)
    if img is None: raise HTTPException(400, "Błąd pliku obrazu")

    count, saved = process_image(img, source_name=path)
    return {"source": path, "people_count": count, "saved_path": saved}


@app.get("/count/url", response_model=CountResponse)
def count_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        img = decode_image(r.content)
    except:
        raise HTTPException(400, "Błąd pobierania obrazu")

    count, saved = process_image(img, source_name=url)
    return {"source": url, "people_count": count, "saved_path": saved}


@app.post("/count/upload", response_model=CountResponse)
async def count_upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"): raise HTTPException(400, "To nie obraz")
    try:
        content = await file.read()
        img = decode_image(content)
    except:
        raise HTTPException(400, "Uszkodzony plik")

    count, saved = process_image(img, source_name=file.filename)
    return {"source": file.filename, "people_count": count, "saved_path": saved}