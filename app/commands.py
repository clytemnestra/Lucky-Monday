import click
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


@click.command()
# @click.argument('asd')
def my_command():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Upload file to folder.
    f = drive.CreateFile({'title': 'Hello.txt', "parents": [
        {'title': 'Hello.txt', "kind": "drive#fileLink", "id": '1gZtlf6luNAQLSE0EvHwBxfpjD5UC6yMT'}]})
    f.SetContentString('asd')
    f.Upload()