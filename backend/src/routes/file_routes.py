
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.file_services import upload_file_service, download_file_service, list_files_metadata_service
from src.models.file_models import FileUploadInput

router = APIRouter()

@router.get("/list")
async def list_files_metadata():
    try:
        files = await list_files_metadata_service()
        return { "status": 200, "message": "Files retrieved successfully", "body": files   }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_input = FileUploadInput(
            original_name=file.filename,
            content = await file.read(),
            extesion=Path(file.filename).suffix,
            size=file.size
        )
        await upload_file_service(file_input)
        return { "status": 200, "message": "File uploaded successfully" }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{stored_name}")
async def download_file(stored_name):
    try:
        await download_file_service(stored_name)
        return { "status": 200, "message": "File downloaded successfully" }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{stored_name}")
async def delete_file(stored_name):
    return "Delete file"