import click
import flask
from flask import current_app, Flask
from flask.cli import with_appcontext

from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

import app
from app.constants import Files
from app.observers import CommandOutput, CommandLogger, CommandPrinter
from app.services.drive import AuthServiceAccount, LMDownloader
from app.services.tokens import AnswersParser, TokensUpdater


@click.command()
@with_appcontext
# @click.argument('asd')
def asd():
    start = 240
    end = 268
    verbose = True
    log = True

    app_config = current_app.config

    sessions_to_update = list(range(start, end + 1))
    out, printer, logger = setup_output(verbose, log)

    drive = AuthServiceAccount().drive
    print('Downloading files...')
    downloaded_files = LMDownloader(drive).download_files()
    answers_file = downloaded_files[Files.ANSWERS_FILE_ID]
    tokens_file = downloaded_files[Files.TOKENS_FILE_ID]
    print('Downloaded ' + answers_file + tokens_file)
    answers_file = 'answers.xlsx'
    tokens_file = 'tokens.xlsx'
    out.notifyObservers('Extracting answers...')
    extracted_answers = AnswersParser(answers_file, sessions_to_update).extract_answers_data()

    updater = TokensUpdater(tokens_file)

    for session_id, session_results in extracted_answers.items():
        out.notifyObservers('Updating session %s with %s entries' % (session_id, len(session_results)))

        session_column, new_column_placement = updater.find_session_column(session_id)
        out.notifyObservers('Searching if session column exists')

        if not session_column:
            out.notifyObservers('Didn\'t find column. Creating...')
            updater.create_session_column(new_column_placement, session_id)
            out.notifyObservers('Created column at letter %s' % new_column_placement)
            session_column = new_column_placement
        else:
            out.notifyObservers('Found the column at letter %s' % + session_column)

        out.notifyObservers('Updating results...')

        for nickname, tokens_value in session_results:
            out.notifyObservers('Updating %s with %s tokens' % (nickname, tokens_value))
            out.notifyObservers('Checking if username exists')

            nickname_row = updater.find_nickname_row(nickname)

            if nickname_row:
                out.notifyObservers('Username exists at row %s' % nickname_row)
            else:
                out.notifyObservers('Username doesn\'t exist. Creating...')
                nickname_row = updater.create_nickname_row(nickname)
                out.notifyObservers('Created username at row %s' % nickname_row)

            out.notifyObservers('Updating tokens...')
            updater.update_user_tokens(nickname_row, session_column, tokens_value)
            # out.notifyObservers('Updating bonuses...')
            # updater.update_user_bonuses(nickname_row, session_column)

    out.notifyObservers('Updating tokens formula...')
    updater.update_users_formula()

    out.notifyObservers('Saving file locally...')

    updater.save_file()


def setup_output(verbose, log):
    out = CommandOutput()
    printer = CommandPrinter()
    logger = CommandLogger()

    if verbose:
        out.addObserver(printer)
    if log:
        out.addObserver(logger)

    return (out, printer, logger)
