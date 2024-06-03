from fastapi import FastAPI, File, UploadFile
import shutil,pytesseract


app = FastAPI()

@app.post("/ocr")
def ocr(image: UploadFile = File(...)):
    filepath = "txtfile"
    with open(filepath,"w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)
    return pytesseract.image_to_string(filepath,lang="eng")