from fastapi import FastAPI

# Levantar servidor: uvicorn main:app --reload
app = FastAPI()

@app.get("/")
def index():
  return "MessIAs API"