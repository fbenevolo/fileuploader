import logging
from pathlib import Path
from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    Header,
    Body,
    File,
    Request,
    Depends,
    status,
)
from src.models import FileUploadInput, FileUploadedEvent, UploadUrlResponse
from src.core.dependencies import get_file_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/upload", status_code=status.HTTP_200_OK, response_model=UploadUrlResponse
)
async def create_upload(
    file: UploadFile = File(...), file_service=Depends(get_file_service)
):
    try:
        file_input = FileUploadInput(
            original_name=file.filename,
            extension=Path(file.filename).suffix,
            size=file.size,
        )

        return await file_service.generate_upload_url_service(file_input)
    except Exception as e:
        logger.exception(f"Error occured during file creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# ROUTE ONLY USED IN LOCAL DEVELOPMENT
@router.post(
    "/files/upload/{filename}",
    status_code=status.HTTP_201_CREATED,
    response_model=FileUploadedEvent,
)
async def upload_file(
    filename,
    request: Request,
    content: bytes = Body(...),
    original_name: str = Header(alias="X-Original-Name"),
    created_at: str = Header(alias="X-Created-At"),
    file_service=Depends(get_file_service),
):
    original_name = request.headers["X-Original-Name"]
    created_at = request.headers["X-Created-At"]

    try:
        metadata = FileUploadedEvent(
            file_id=filename.rsplit(".", 1)[0],
            original_name=original_name,
            stored_name=filename,
            size=len(content),
            created_at=created_at,
        )
        await file_service.save_file_service(metadata, content)
        return metadata
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
