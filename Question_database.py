"""
QRecord is one question with link to question object and voice object,
QTable is one suit
"""
import os
from os.path import exists
from pathlib import Path
from typing import Optional, override

try:
    from common_py_lib.actions.Input import int_input_from_user
    from common_py_lib.entities.Formatter import TextAnsiFormatter
    from specification.v1.entities.Database import Database
    from specification.v1.entities.Record import Record
    from specification.v1.entities.Table import Table
except ModuleNotFoundError:
    print('Provide libs first')

start_path: str = Path().parent.absolute().as_posix()


def clear_string(string: str) -> str:
    return string.strip()


# TODO delete later
def is_suit(maybe_suit_name: str) -> bool:
    """
    Check that directory is suit by contract
    :param maybe_suit_name: path or name of suit
    :return: bool result
    """
    if os.path.isdir(maybe_suit_name):
        if '__main__' in os.listdir(maybe_suit_name):
            return True
    return False


# TODO delete later
def handle_critical_error(msg: str):
    TextAnsiFormatter.prRed(msg)
    exit(1)


class QRecord(Record):

    def __str__(self) -> str:
        pass

    def __init__(self, textual_question, voicy_question_link):
        """
        Construct record in this small database
        :param textual_question: IQuestion object link in text
        :param voicy_question_link: link to voice of this question by norator
        """
        super().__init__()
        self.text_question = textual_question
        self.voicy_question_link = voicy_question_link


class QTable(Table):
    records: dict[str, QRecord]
    table_name: str

    def __init__(self, table_name: str):
        """
        One suit entity
        :param table_name: suit name
        """
        super().__init__(table_name)
        self.records = dict()
        self.table_name = table_name

    def find_record_by_name(self, name: str) -> Optional[Record]:
        pass

    def find_record_by_id(self, record_id: int) -> Optional[Record]:
        pass

    @override
    def add_record(self, record_name: str, record: QRecord):
        table_key = self.table_name + '_' + record_name
        self.records[table_key] = record

    def update_record(self, params: dict) -> None:
        pass

    def update_record_by_pattern(self, pattern: str, params: dict) -> None:
        pass

    def delete_record(self, params: dict) -> None:
        pass

    def delete_record_by_id(self, record_id: int) -> None:
        pass

    def select_records(self, params: Optional[dict] = None) -> list[Record]:
        pass

    def select_by_pattern(self, pattern: str) -> list[Record]:
        pass

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()


class QDatabase(Database):
    tables: dict[str, QTable]
    voice_table: dict[str, str]
    all_table: dict[str, str]

    def __init__(self, database_name: str):
        super().__init__(database_name)
        self.tables = dict()

    def find_table_by_predicate(self, predicate) -> Table | None:
        return super().find_table_by_predicate(predicate)

    def find_table_by_name(self, table_name: str) -> Table | None:
        return super().find_table_by_name(table_name)

    def create_table(self, table_name: str) -> None:
        super().create_table(table_name)

    def get_all_tables(self) -> list[Table]:
        return super().get_all_tables()

    def add_table(self, table_name: str):
        qtable_obj = QTable(table_name)
        self.tables[table_name] = qtable_obj

    def delete_table(self, table_name: str):
        if self.tables.__contains__(table_name):
            del self.tables[table_name]

    def get_dependency_from_all(self, dependency_name: str) -> str | None:
        if dependency_name in self.all_table:
            return self.all_table[dependency_name]
        else:
            TextAnsiFormatter.prRed(f'No global value found: "{dependency_name}", return "None" instead')
            return None

    def list_all_tables(self):
        pass

    def create_voice_table(self):
        pass

    def create_all_table(self):
        self.all_table = dict()

        # global branch:
        if not exists(start_path + os.sep + '__global__'):
            TextAnsiFormatter.prRed('Global data directory is not created, auto create global directory')
            os.mkdir(start_path + os.sep + '__global__')
        dir_data = os.listdir(start_path + os.sep + '__global__')
        if len(dir_data) > 0:
            for file_line in dir_data:
                # insert global path as a value
                self.all_table[clear_string(file_line.removesuffix('.txt') if '.txt' in file_line else file_line)] = clear_string(
                    start_path + os.sep + '__global__' + os.sep + file_line)

        else:
            TextAnsiFormatter.prYellow('Global directory is empty, fill it with global files!')

        # all file branch:
        if not exists(start_path + os.sep + '__all__'):
            TextAnsiFormatter.prRed('All file is not created, auto create all file')
            open(start_path + os.sep + '__all__', 'r').close()

        file_data = open(start_path + os.sep + '__all__', 'r').readlines()

        for line in file_data:
            if line != '' and '=' in line:
                # path path:
                if line.startswith('Path'):
                    line = line.removeprefix('Path')
                    glob_name, glob_path = line.split('=')
                    self.all_table[clear_string(glob_name)] = clear_string(glob_path)

                # variable path:
                elif line.startswith('Var'):
                    line = line.removeprefix('Var')
                    glob_name, glob_path = line.split('=')
                    self.all_table[clear_string(glob_name)] = clear_string(glob_path)

                else:
                    TextAnsiFormatter.prRed(f'Unknown parameter line in all file {line}')


class DB_interface:
    """
    Console based interface for interacting with db. Provide DB_api v1
    """

    def __init__(self):
        self.database = QDatabase()

    def run(self):
        while True:
            TextAnsiFormatter.prPurple('Choose action by its number:')
            print('1. Run command interpreter')
            print('2. Add question')
            print('3. Add answer to question')
            print('4. To exit')
            user_choice = int_input_from_user()
            match user_choice:
                case 1:
                    pass
                case 2:
                    pass
                case 2:
                    pass
                case 4:
                    exit(0)
