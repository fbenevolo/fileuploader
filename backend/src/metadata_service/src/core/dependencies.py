from fastapi import Request


def get_metadata_service(request: Request):
    return request.app.state.metadata_service
