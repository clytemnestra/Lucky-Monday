import click

from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

from app.constants import Files
from app.observers import CommandOutput, CommandLogger, CommandPrinter
from app.services.drive import AuthServiceAccount, LMDownloader
from app.services.tokens import AnswersParser, TokensUpdater


@click.command()
# @click.argument('asd')
def asd():
    start = 252
    end = 255
    verbose = True
    log = True


    sessions_to_update = list(range(start, end + 1))
    out,printer,logger = setup_output(verbose, log)
    return
    # drive = AuthServiceAccount().drive
    # print('Downloading files...')
    # downloaded_files = LMDownloader(drive).download_files()
    # answers_file = downloaded_files[Files.ANSWERS_FILE_ID]
    # tokens_file = downloaded_files[Files.TOKENS_FILE_ID]
    # print('Downloaded' + answers_file + tokens_file)
    answers_file = 'answers.xlsx'
    tokens_file = 'tokens.xlsx'
    out.notifyObservers('Extracting answers...')
    extracted_answers = AnswersParser(answers_file, sessions_to_update).extract_answers_data()
    TokensUpdater(tokens_file, extracted_answers).update()

def setup_output(verbose, log):
    out = CommandOutput()
    printer = CommandPrinter()
    logger = CommandLogger()

    if verbose:
        out.addObserver(printer)
    if log:
        out.addObserver(logger)

    return (out, printer, logger)

