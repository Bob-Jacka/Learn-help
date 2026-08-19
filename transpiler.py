"""
Question transpiler, convert from usual string line into Question object
"""
import os
import sys
from os.path import exists
from typing import Final

if __name__ == '__main__':
    start_dir_path: Final[str] = '/home/kirill/PycharmProjects/Learn-help'
    args_length: Final[int] = len(sys.argv) - 1

    args: Final[list[str]] = sys.argv if args_length > 1 else []
    dir_questions: Final[dict[str, dict[str, list[str]]]] = dict()
    ignored_names: Final[list[str]] = ['__main__', '.gitignore']
    ignored_dirs: Final[list[str]] = ['.idea', '.venv', '.git', '__tasks__', '__pycache__', 'python']

    if args_length == 0:
        # filter directories
        for dir_name in filter(lambda x: os.path.isdir(start_dir_path + os.sep + x) and x not in ignored_dirs and not x.startswith('.'), os.listdir(start_dir_path)):
            print(f'Directory name: "{dir_name}"')

            # if check if main file exists
            if exists(start_dir_path + os.sep + dir_name + os.sep + '__main__') or dir_name == '__global__':
                dir_questions[dir_name] = dict()
                for file_name in filter(lambda x: x not in ignored_names, os.listdir(start_dir_path + os.sep + dir_name)):
                    # open file
                    dir_questions[dir_name][file_name] = list()
                    with open(start_dir_path + os.sep + dir_name + os.sep + file_name, 'r') as file:
                        for line in filter(lambda x: not x.startswith('#') and x != '\n' and not x.startswith('.'), file.readlines()):
                            if '|' in line:
                                # replace zapitaya with empty line
                                split_line = line.strip().replace(',', '').split('|')
                                question = split_line[0].strip()
                                answer = split_line[1].strip()

                                if answer.find('answer') > 1:  # bug fix
                                    answer = answer.replace('answer=', ',')
                                dir_questions[dir_name][file_name].append(f'Question(type=Simple, question={question}, answer={answer}, priority=NO)')
                            else:
                                dir_questions[dir_name][file_name].append(f'Question(type=Simple, question={line.strip().replace(',', '')}, answer=, priority=NO)')

            else:
                continue
        print()  # just new line
        counter: int = 0
        for dir_name, file_suit in dir_questions.items():
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
