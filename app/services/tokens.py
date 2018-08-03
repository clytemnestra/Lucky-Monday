from openpyxl import load_workbook
from openpyxl.utils import coordinate_from_string, column_index_from_string

from app.constants import Files


# class TokensUpdater:
#
#     def __init__(self, tokens_file, answers_file):
#         pass
#
#     def update_session(self, session: int):
#         pass
#
#     def update_sessions(self, sessions: []):
#         for session in sessions:
#             self.update_session(session)


class TokensUpdater:
    def __init__(self, file, answers):
        self.file = file
        self.answers = answers

    def update(self):
        for session_id,session_results in self.answers:
            self.update_session(session)


    def update_session(self, session_data):
        pass

    def place_session(self):
        """Find column where to place current session."""
        # check if it exists already
        # place it if it doesn't
        pass


class AnswersParser:
    def __init__(self, file: str, sessions_to_extract: list):
        self.file = file
        self.sessions_to_extract = sessions_to_extract
        self.excel = load_workbook(file, data_only=True)

    def __extract_session_data(self, number):
        sheet = self.excel['#' + str(number)]
        session_data = []
        tokens_column = column_index_from_string(Files.ANSWERS_TOKENS_COL) - 1
        nicknames_column = column_index_from_string(Files.ANSWERS_NICKNAMES_COL) - 1

        for row in sheet.iter_rows(min_row=2):
            if row[tokens_column].value:
                session_data.append({row[nicknames_column].value: row[tokens_column].value})

        return session_data

    def extract_answers_data(self):
        answers_data = {}

        for session_no in self.sessions_to_extract:
            answers_data[session_no] = self.__extract_session_data(session_no)

        return answers_data
