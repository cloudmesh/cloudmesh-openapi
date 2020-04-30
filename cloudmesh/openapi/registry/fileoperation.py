import connexion
from pathlib import Path
from cloudmesh.common.util import path_expand

"""
  This class will help to upload file from restful API
"""
class FileOperation:

    def file_upload(self) -> str:
        file = connexion.request.files.get("upload")
        filename = file.filename
        if file:
            file_path = f"~/.cloudmesh/upload-file"
            p = Path(path_expand(file_path))
            p.mkdir(parents=True, exist_ok=True)
            file.save(f'{p.absolute()}/{filename}')
        return filename
