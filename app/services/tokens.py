from copy import copy
from typing import NamedTuple

from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.styles.cell_style import CellStyle
from openpyxl.styles.colors import RED
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
        self.excel = load_workbook(file, data_only=False)
        self.sheet = self.excel[Files.TOKENS_SHEET]
        self.answers = answers

    def update(self):
        for session_id, session_results in self.answers.items():
            self.update_session(session_id, session_results)

    def update_session(self, id, data):
        column = self.place_session(id)
        #todo

    def update_bonuses(self):
        pass

    def place_session(self, id):
        """Find column where to place current session."""
        # check if it exists already
        # place it if it doesn't
        tokens_first_column = column_index_from_string(Files.TOKENS_NICKNAMES_COL) + 1

        session_column = None
        new_column_placement = tokens_first_column

        for col in self.sheet.iter_cols(min_col=tokens_first_column, max_row=1):
            column_session_number = int(col[0].value.replace('#', ''))
            current_column_index = column_index_from_string(col[0].column)

            if id < column_session_number:
                new_column_placement = current_column_index + 1

            if column_session_number == int(id):
                session_column = current_column_index
                break

        if not session_column:
            self.create_session_column(new_column_placement, id)

        return session_column

    def create_session_column(self, column, session_id):
        self.sheet.insert_cols(column)
        cell = self.sheet.cell(1, column)
        cell.value = '#' + str(session_id)
        CellCopy(self.sheet).copy_session_header_from_previous(cell).add_session_borders(cell)

        self.excel.save(self.file)  # todo delete this - temporary save to check


class CellCopy:

    def __init__(self, sheet):
        self.sheet = sheet

    def copy_session_header_from_previous(self, session_header_cell):
        properties = ['font', 'fill', 'border', 'alignment', 'number_format', 'protection']
        previous_session_column = column_index_from_string(session_header_cell.column) + 1
        previous_session_header_cell = self.sheet.cell(1, previous_session_column)

        self.__copy_properties(previous_session_header_cell, session_header_cell, properties)

        return self

    def add_session_borders(self, session_header_cell):
        properties = ['border', 'alignment', 'number_format', 'protection']
        session_column = column_index_from_string(session_header_cell.column)
        previous_session_row = session_header_cell.row + 1
        previous_session_column = column_index_from_string(session_header_cell.column) + 1
        previous_session_first_result_cell = self.sheet.cell(previous_session_row, previous_session_column)

        for row in self.sheet.iter_rows(min_row=2, min_col=session_column, max_col=session_column):
            for cell in row:
                self.__copy_properties(previous_session_first_result_cell, cell, properties)

        return self

    def __copy_properties(self, from_cell, to_cell, properties):
        for cell_property in properties:
            setattr(to_cell, cell_property, copy(getattr(from_cell, cell_property)))

        return self


class AnswersParser:
    def __init__(self, file: str, sessions_to_extract: list):
        self.sessions_to_extract = sessions_to_extract
        self.excel = load_workbook(file, data_only=True)

    def __extract_session_data(self, number):
        sheet = self.excel['#' + str(number)]
        session_data = []
        tokens_column = column_index_from_string(Files.ANSWERS_TOKENS_COL) - 1
        nicknames_column = column_index_from_string(Files.ANSWERS_NICKNAMES_COL) - 1

        for row in sheet.iter_rows(min_row=2):
            # todo throw error or skip - tokens column not defined
            if row[tokens_column].value:
                session_data.append({row[nicknames_column].value: row[tokens_column].value})

        return session_data

    def extract_answers_data(self):
        answers_data = {}

        for session_no in self.sessions_to_extract:
            answers_data[session_no] = self.__extract_session_data(session_no)

        return answers_data

class Result(NamedTuple):
    nickname:int
    answer: str

class Results(NamedTuple):
    pass

class SessionResults(NamedTuple):
    session: int
    results: Result

