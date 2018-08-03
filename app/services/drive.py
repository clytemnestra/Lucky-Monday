from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile

from app.constants import Mimetypes, Files


class AuthServiceAccount:
    JSON_FILE = 'client_secrets.json'
    scopes = ['https://www.googleapis.com/auth/drive']
    drive = None

    def __init__(self, json_file=JSON_FILE, scopes=None):
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file,
                                                                             self.scopes if not scopes else scopes)
        drive = GoogleDrive(gauth)

        self.drive = drive


class LMDownloader:
    def __init__(self, drive: GoogleDrive):
        self.drive = drive

    def download_files(self):

        files = {Files.TOKENS_FILE_ID: Files.TOKENS_FILE_DOWNLOAD_NAME,
                 Files.ANSWERS_FILE_ID: Files.ANSWERS_FILE_DOWNLOAD_NAME}

        downloaded_files = {}

        for file_id, file_name in files.items():

            file = self.drive.CreateFile({'id': file_id})
            file_me = self.__decide_mimetype_and_extension(file)
            mimetype = None
            if file_me:
                file_name = file_name + '.' + file_me['extension']
                mimetype = file_me['mimetype']

            file.GetContentFile(file_name, mimetype=mimetype)
            downloaded_files[file_id] = file_name

        return downloaded_files

    def __decide_mimetype_and_extension(self, file: GoogleDriveFile):
        mimetypes = Mimetypes.mimetypes
        download_mimetype = None

        if file['mimeType'] in Mimetypes.mimetypes:
            download_mimetype = mimetypes[file['mimeType']]

        return download_mimetype


class LMUploader:
    pass
