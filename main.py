from fastapi import FastAPI
from PIL import Image
import easyocr
import cv2
import requests
from fastapi.middleware.cors import CORSMiddleware


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

def get_header(img):
  ancho_inicio = 0
  ancho_fin = img.size[0]
  altura_inicio = 0
  altura_fin = 56
  coordenadas = (ancho_inicio, altura_inicio,ancho_fin, altura_fin)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("components/header.png")
  image = cv2.imread("components/header.png")
  result = reader.readtext(image, paragraph=False, detail=0)
  return result

def get_title_description(img):
  width = 450
  height = 72
  coordenadas = (175,120,width + 175,height + 120)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("components/title_description.png")

def get_doctype(img):
  width = 450
  height = 48
  coordenadas = (175,232,width + 175,height + 232)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("components/doctype.png")

def get_docnumber(img):
  width = 450
  height = 48
  coordenadas = (175,320,width + 175,height + 320)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("components/docnumber.png")

def get_buttons(img):
  width = 450
  height = 48
  coordenadas = (175,448,width + 175,height + 448)
  crop_image = img.crop(coordenadas)
  # crop_image.show()
  crop_image.save("components/buttons.png")

@app.get("/cases")
def index():
  img = Image.open('imagen.png')
  header_text = get_header(img)
  circuit = header_text[1]
  given = f"DADO un usuario en el circuito de {circuit}"
  when = "Sarasa"
  then = "Sarasa"
  get_title_description(img)
  get_doctype(img)
  get_docnumber(img)
  get_buttons(img)
  return f"MessIAs API: {given} ||||||||||||||||| RTA MODELO: {query("components/docnumber.png")}"

@app.get("/", tags=["Root"])
async def hello():
  return {"hello": "Hola mundo"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)