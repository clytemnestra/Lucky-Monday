import click

from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

from app.constants import Files
from app.services.drive import AuthServiceAccount, LMDownloader
from app.services.tokens import TokensParser, AnswersParser, TokensUpdater


@click.command()
# @click.argument('asd')
def asd():

    sessions_to_update = list(range(240,266))

    # drive = AuthServiceAccount().drive
    # downloaded_files = LMDownloader(drive).download_files()
    # answers_file = downloaded_files[Files.ANSWERS_FILE_ID]
    # tokens_file = downloaded_files[Files.TOKENS_FILE_ID]
    answers_file = 'answers.xlsx'
    tokens_file = 'tokens.xlsx'
    #todo object pt extracted_answers
    extracted_answers = AnswersParser(answers_file, sessions_to_update).extract_answers_data()

    TokensUpdater(tokens_file, extracted_answers).update()
