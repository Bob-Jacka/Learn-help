"""
Question transpiler, convert from usual string line into Question object
"""
import os
import sys
from os.path import exists
from typing import Final

ignored_names: Final[list[str]] = ['__main__', '.gitignore']
ignored_dirs: Final[list[str]] = ['.idea', '.venv', '.git', '__tasks__', '__pycache__', 'python']
args_length: Final[int] = len(sys.argv) - 1
args: Final[list[str]] = sys.argv if args_length > 1 else []


class Transpiler:
    def __init__(self, start_path):
        self.start_path = start_path
        self.all_questions: Final[dict[str, dict[str, list[str]]]] = dict()

    def transpile(self):
        if args_length == 0:
            # filter directories
            for dir_name in filter(lambda x: os.path.isdir(self.start_path + os.sep + x) and x not in ignored_dirs and not x.startswith('.'), os.listdir(self.start_path)):
                print(f'Directory name: "{dir_name}"')

                # if check if main file exists
                if exists(self.start_path + os.sep + dir_name + os.sep + '__main__') or dir_name == '__global__':
                    self.all_questions[dir_name] = dict()
                    for file_name in filter(lambda x: x not in ignored_names, os.listdir(self.start_path + os.sep + dir_name)):
                        # open file
                        self.all_questions[dir_name][file_name] = list()
                        with open(self.start_path + os.sep + dir_name + os.sep + file_name, 'r') as file:
                            for line in filter(lambda x: not x.startswith('#') and x != '\n' and not x.startswith('.'), file.readlines()):
                                self.parse_one_question(line, dir_name, file_name)

                else:
                    continue
            print()  # just new line
            counter: int = 0
            for dir_name, file_suit in self.all_questions.items():
                print(f'Directory "{dir_name}" contains:')
                if len(file_suit) > 0:
                    for file_name, files in file_suit.items():
                        print(f'\tFile "{file_name}" constains:')
                        for question in files:
                            print(f'\t\t{question}')
                            counter += 1
                        print(f'\t"{file_name}" questions count: {len(files)}')
            print(f'All question counter: {counter}')

        else:
            raise Exception('Wrong argument count, expected <File name>, received 0')

    def parse_one_question(self, line: str, dir_name: str, file_name: str) -> None:
        if '|' in line:
            # replace zapitaya with empty line
            split_line = line.strip().replace(',', '').split('|')
            question = split_line[0].strip()
            answer = split_line[1].strip()

            if answer.find('answer') > 1:  # bug fix, do not watch on this
                answer = answer.replace('answer=', ',')
            self.all_questions[dir_name][file_name].append(f'Question(type=Simple, question={question}, answer={answer}, priority=NO)')
        else:
            self.all_questions[dir_name][file_name].append(f'Question(type=Simple, question={line.strip().replace(',', '')}, answer=, priority=NO)')

    @staticmethod
    def parse_one_question_static(line: str) -> str:
        """
        Static version of parse one question
        :param line: question line to parse
        :return: string representation of Question object
        """
        if '|' in line:
            # replace zapitaya with empty line
            split_line = line.strip().replace(',', '').split('|')
            question = split_line[0].strip()
            answer = split_line[1].strip()

            if answer.find('answer') > 1:  # bug fix, do not watch on this
                answer = answer.replace('answer=', ',')
            return f'Question(type=Simple, question={question}, answer={answer}, priority=NO)'
        else:
            return f'Question(type=Simple, question={line.strip().replace(',', '')}, answer=, priority=NO)'

    def convert_to_old_format(self, question_object_line: str) -> str:
        """
        Convert modern new question string line representation to old format
        :param question_object_line: string representation of Question object
        :return: old format string
        """
        pass

    def get_data_from_question(self, question_object_line: str) -> dict[str, str]:
        """
        Decomposition of question string line
        :param question_object_line: string representation of Question object
        :return: dict with param and value
        """
        to_return: dict[str, str] = dict()
        splitted = question_object_line.removeprefix('Question(').removesuffix(')').split(',')
        for elem in splitted:
            param_name, param_value = elem.split('=')
            to_return[param_name] = param_value
        return to_return

    def delete_data_from_question(self, question_object_line: str) -> dict[str, str]:
        """
        Delete parameter from question object line string
        :param question_object_line: string representation of Question object
        :return: changed object line string
        """
        pass

    def add_data_to_question(self, question_object_line: str) -> dict[str, str]:
        """
        Add parameter to question object line string
        :param question_object_line: string representation of Question object
        :return: changed object line string
        """
        pass

    def change_parameter_to(self, question_object_line: str, parameter: str, change_to: str) -> dict[str, str]:
        """
        Change parameter in question object line to something
        :param question_object_line:
        :param parameter:
        :param change_to:
        :return: changed object line string
        """
        pass


if __name__ == '__main__':
    # os.path.abspath(os.path.curdir)
    transpiler = Transpiler()
    transpiler.transpile()
