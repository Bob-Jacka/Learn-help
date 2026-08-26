"""
Question transpiler, convert from usual string line into Question object
"""
import os
from os.path import exists
from typing import Final


class Settings:
    ignored_names: Final[list[str]] = ['__main__', '.gitignore']
    ignored_dirs: Final[list[str]] = ['.idea', '.venv', '.git', '__tasks__', '__pycache__', 'python']


class Transpiler:
    def __init__(self, start_path):
        self.start_path = start_path
        self.all_questions: Final[dict[str, dict[str, list[str]]]] = dict()

    def transpile(self, args_count):
        if args_count == 0:
            # filter directories
            for dir_name in filter(lambda x: os.path.isdir(self.start_path + os.sep + x) and x not in Settings.ignored_dirs and not x.startswith('.'), os.listdir(self.start_path)):
                print(f'Directory name: "{dir_name}"')

                # if check if main file exists
                if exists(self.start_path + os.sep + dir_name + os.sep + '__main__') or dir_name == '__global__':
                    self.all_questions[dir_name] = dict()
                    for file_name in filter(lambda x: x not in Settings.ignored_names, os.listdir(self.start_path + os.sep + dir_name)):
                        # open file
                        self.all_questions[dir_name][file_name] = list()
                        with open(self.start_path + os.sep + dir_name + os.sep + file_name, 'r') as file:
                            for line in filter(lambda x: not x.startswith('#') and x != '\n' and not x.startswith('.'), file.readlines()):
                                # exclude already parsed questions from parse
                                if not line.startswith('Question('):
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
    def parse_one_question_static(line: str, type: str = 'Simple') -> str:
        """
        Static version of parse one question
        :param type: type of the Question object
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
            return f'Question(type={type}, question={question}, answer={answer}, priority=NO)'
        else:
            return f'Question(type={type}, question={line.strip().replace(',', '')}, answer=, priority=NO)'

    @staticmethod
    def convert_to_old_format(question_object_line: str) -> str:
        """
        Convert modern new question string line representation to old format
        :param question_object_line: string representation of Question object
        :return: old format string
        """
        dict_param: dict[str, str] = Transpiler.get_data_from_question(question_object_line)
        return f'{dict_param['question']}|{dict_param.get('answer', '')}'

    @staticmethod
    def convert_to_new_format(question_params: dict[str, str]) -> str:
        """
        Convert from params dict to Question string representation
        :param question_params: Question parameters
        :return: string representation
        """
        return f'Question(type={question_params.get('type', 'Simple')}, answer={question_params.get('answer', '')}, priority={question_params.get('priority', '')})'

    @staticmethod
    def get_data_from_question(question_object_line: str) -> dict[str, str]:
        """
        Decomposition of question string line into parameters
        :param question_object_line: string representation of Question object
        :return: dict with param and value
        """
        to_return: dict[str, str] = dict()
        splitted = question_object_line.removeprefix('Question(').removesuffix(')').split(',')
        for elem in splitted:
            param_name, param_value = elem.split('=', 1)  # bug fix, only 1 split due to = sym in answer
            to_return[param_name.strip()] = param_value
        return to_return

    def delete_value_data_from_question(self, question_object_line: str, key_of_value: str) -> dict[str, str]:
        """
        Delete value of the parameter from question object line string
        :param key_of_value: key that points to desired to delete value
        :param question_object_line: string representation of Question object
        :return: changed object line string
        """
        splitted = Transpiler.get_data_from_question(question_object_line)
        del splitted[key_of_value]
        return splitted

    def delete_key_value_data_from_question(self, question_object_line: str) -> dict[str, str]:
        """
        Delete full parameter (key and value) from question object line string
        :param question_object_line: string representation of Question object
        :return: changed object line string
        """
        pass

    def add_data_to_question(self, question_object_line: str, parameter_name: str, parameter_value: str = '') -> dict[str, str]:
        """
        Add parameter (key and value) to question object line string
        :param parameter_name: new parameter name
        :param parameter_value: value of the new parameter
        :param question_object_line: string representation of Question object
        :return: changed object line string
        """
        pass

    def change_parameter_to(self, question_object_line: str, parameter: str, change_to: str) -> dict[str, str]:
        """
        Change parameter in question object line to something
        :param question_object_line: string representation of Question object
        :param parameter: parameter to change
        :param change_to: what value to use in parameter
        :return: changed object line string
        """
        pass


if __name__ == '__main__':
    transpiler = Transpiler(os.path.abspath(os.path.curdir))
    transpiler.transpile()
