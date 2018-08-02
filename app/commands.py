import click

from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive


@click.command()
# @click.argument('asd')
def my_command():
    def auth():
        JSON_FILE = 'client_secrets.json'

        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scopes=[
            'https://www.googleapis.com/auth/drive'])
        drive = GoogleDrive(gauth)

        return drive

    def update(drive: GoogleDrive):
        TOKENS_FILE_ID = '1aU9ATPq5HsraAFOIiijYJx0OqQgIVQ5LdKB3yKioZhg'
        ANSWERS_FILE_ID = '1c701qti631UnXbo_nlD1qFkSrLDxAEsA6db0WAllmS0'

        tokens_file = drive.CreateFile({'id': TOKENS_FILE_ID})
        # print('title: %s, mimeType: %s' % (tokens_file['title'], tokens_file['mimeType']))

        mimetypes = {
            # Drive Document files as MS Word files.
            'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

            # Drive Sheets files as MS Excel files.
            'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

            # etc.
        }

        download_mimetype = None
        if tokens_file['mimeType'] in mimetypes:
            download_mimetype = mimetypes[tokens_file['mimeType']]
        tokens_file.FetchMetadata(fetch_all=True)
        tokens_file.GetContentFile(tokens_file['title'] +'.xlsx', mimetype=download_mimetype)
    drive = auth()
    update(drive)
