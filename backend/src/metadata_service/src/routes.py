import logging
from fastapi import APIRouter, Body, HTTPException, Depends, status
from src.models import MetadataInput
from src.core.dependencies import get_metadata_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_metadata(file_service=Depends(get_metadata_service)):
    try:
        files = await file_service.list_metadata_service()
        return files
    except Exception as e:
        logger.exception(f"Error occured during file metadata listing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_metadata(
    metadata_input: MetadataInput = Body(...),
    file_service=Depends(get_metadata_service),
):
    try:
        await file_service.upload_metadata_service(metadata_input)
        return "Metadata uploaded successfully"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occured during file upload: {str(e)}",
        )


@router.delete("/delete/{file_id}", status_code=status.HTTP_200_OK)
async def delete_metadata(file_id, file_service=Depends(get_metadata_service)):
    try:
        await file_service.delete_metadata_service(file_id)
        return "Metadata sucessfully deleted"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occured during deletion of file: {str(e)}",
        )
