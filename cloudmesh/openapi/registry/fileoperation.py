import connexion
from pathlib import Path
from cloudmesh.common.util import path_expand


class FileOperation:
    """
      This class will help to upload file from restful API
    """
    def file_upload(self) -> str:
        """
           This function will upload file into .cloudmesh/upload-file location
           This will first get upload file object from request.files function
           and then override this object in given location.
           """
        file = connexion.request.files.get("upload")
        filename = file.filename
        if file:
            file_path = f"~/.cloudmesh/upload-file"
            p = Path(path_expand(file_path))
            p.mkdir(parents=True, exist_ok=True)
            file.save(f'{p.absolute()}/{filename}')
        return filename
