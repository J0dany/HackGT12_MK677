from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from routes.parser import parse_degreeworks_remaining

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_degreeworks(file: UploadFile = File(...)):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    remaining_courses = parse_degreeworks_remaining(file_path)

    if not remaining_courses:
        return JSONResponse({"error": "Could not detect remaining courses in the PDF"}, status_code=400)

    return JSONResponse({
        "remaining_courses": remaining_courses
    })
