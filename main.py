from fastapi import FastAPI
from PIL import Image
import easyocr
import cv2
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import base64
import io

API_URL = "https://api-inference.huggingface.co/models/genia-vdg/genia-model"
headers = {"Authorization": "Bearer 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"}

def query(filename):
  with open(filename, "rb") as f:
      data = f.read()
  response = requests.post(API_URL, headers=headers, json={"wait_for_model": True}, data=data)
  return response.json()

# Levantar servidor: uvicorn app:app --reload
# Agregar condicional desktop/responsive según ancho de imagen -> given

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = easyocr.Reader(["es"], gpu=False)

def decode_base64(base64_string):
  decoded_string = io.BytesIO(base64.b64decode(base64_string))
  img = Image.open(decoded_string)
  return img


def get_device(img):
  ancho = img.size[0]
  if(ancho == 1280):
    return "desktop"
  elif(ancho == 320):
    return "mobile"
  else:
    return "unknown"

def get_header(img):
  ancho_inicio = 0
  ancho_fin = img.size[0]
  altura_inicio = 0
  altura_fin = 56
  coordenadas = (ancho_inicio, altura_inicio,ancho_fin, altura_fin)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("header.png")
  image = cv2.imread("header.png")
  result = reader.readtext(image, paragraph=False, detail=0)
  print(result)
  return result

def get_title_description(img):
  width = 450
  height = 72
  coordenadas = (175,120,width + 175,height + 120)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("title_description.png")

def get_doctype(img):
  width = 450
  height = 48
  coordenadas = (175,232,width + 175,height + 232)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("doctype.png")

def get_docnumber(img):
  width = 450
  height = 48
  coordenadas = (175,320,width + 175,height + 320)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("docnumber.png")

def get_buttons(img):
  width = 450
  height = 48
  coordenadas = (175,448,width + 175,height + 448)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("buttons.png")

@app.post("/obtenercasos")
async def index(image: str = Body(..., embed=True)):
  img2 = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
  img2.save("image.png")
  img2.close()
  img = Image.open("image.png")
  header_text = get_header(img)
  device = get_device(img)
  index = 1 if device == "desktop" else 0
  circuit = header_text[index]
  given = f"<b>DADO</b> un usuario en el circuito de <b>{circuit}</b> desde un dispositivo <b>{device}</b>"
  when = "Sarasa"
  then = "Sarasa"
  get_title_description(img)
  get_doctype(img)
  get_docnumber(img)
  get_buttons(img)
  return [
    {
      "id": 1,
      "body":{
        "given": [given], 
        "when": [""], 
        "then": [""]
      },
      "accepted": False,
      "discarded": False
    },
    {
      "id": 2,
      "body":{
        "given": [given], 
        "when": [""], 
        "then": [""]
      },
      "accepted": False,
      "discarded": False
    },
    {
      "id": 3,
      "body":{
        "given": [given], 
        "when": [""], 
        "then": [""]
      },
      "accepted": False,
      "discarded": False
    },
    {
      "id": 4,
      "body":{
        "given": [given], 
        "when": [""], 
        "then": [""]
      },
      "accepted": False,
      "discarded": False
    }
  ]

@app.get("/", tags=["Root"])
async def hello():
  return {"hello": "Hola mundo"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)