import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends, status
from src.models import FileUploadInput, UploadUrlResponse
from src.core.dependencies import get_file_service

logger = logging.getLogger(__name__)

router = APIRouter()


# @router.get("/list")
# async def list_files_metadata(file_service=Depends(get_file_service)):
#     try:
#         files = await file_service.list_files_metadata_service()
#         return {"status": 200, "message": "Files retrieved successfully", "body": files}
#     except Exception as e:
#         logger.exception(f"Error occured during file metadata listing: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/upload", status_code=status.HTTP_201_CREATED, response_model=UploadUrlResponse
)
async def upload_file(
    file: UploadFile = File(...), file_service=Depends(get_file_service)
):
    try:
        file_input = FileUploadInput(
            original_name=file.filename,
            content=await file.read(),
            extension=Path(file.filename).suffix,
            size=file.size,
        )

        return await file_service.generate_upload_url_service(file_input)
    except Exception as e:
        logger.exception(f"Error occured during file upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/download/{stored_name}")
async def download_file(stored_name, file_service=Depends(get_file_service)):
    try:
        content = await file_service.download_file_service(stored_name)
        return {
            "status": 200,
            "message": "File downloaded successfully",
            "body": content,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{stored_name}")
async def delete_file(stored_name, file_service=Depends(get_file_service)):
    try:
        await file_service.delete_file_service(stored_name)
        return {"status": 200, "message": "File and its metadata deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
