from fastapi import Request


def get_file_service(request: Request):
    return request.app.state.file_service
