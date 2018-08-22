class Mimetypes:
    mimetypes = {
        # Drive Document files as MS Word files.
        'application/vnd.google-apps.document': {
            'mimetype': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'extension': 'docx'
        },

        # Drive Sheets files as MS Excel files.
        'application/vnd.google-apps.spreadsheet': {
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'extension': 'xlsx'
        }

    }


class Files:
    TOKENS_FILE_ID = '1aSDqJAc0iOkCgXI_LLwG_gVfY9tivJ8z6xjsuSZhiO4'
    ANSWERS_FILE_ID = '1WrvkkPfxRrICvtBKyb-KmS7R2woQ7aCH3-lkEYacrnE'

    TOKENS_FILE_DOWNLOAD_NAME = 'tokens'
    ANSWERS_FILE_DOWNLOAD_NAME = 'answers'

    TOKENS_SHEET = 'Tokens'
    TOKENS_USED_COL = 'A'
    TOKENS_BONUS_COL = 'B'
    TOKENS_CURRENT_COL = 'C'
    TOKENS_NICKNAMES_COL = 'D'

    ANSWERS_NICKNAMES_COL = 'D'
    ANSWERS_TOKENS_COL = 'E'