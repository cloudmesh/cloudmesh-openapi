from cloudmesh.openapi.registry.fileoperation import FileOperation

def upload() -> str:

    filename=FileOperation().file_upload()
    return filename
