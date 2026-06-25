import datetime
import os.path
import random
import signal
import sys
from collections import OrderedDict
from os.path import exists
from pathlib import Path
from typing import Final


class Global_statement:
    """
    Some constants and global data
    """
    # containers
    questions_to_learn: Final[list[str | list[str]]] = list()  # to do learn
    all_file_data: Final[dict[str, str | Path]] = dict()

    # time functionality:
    start_time: Final[datetime.datetime] = datetime.datetime.now()
    finish_time: datetime.datetime

    # consts:
    later_learn_filename: Final[str] = 'todo-learn'
    main_file_name: Final[str] = 'main.txt'
    app_version: Final[str] = '2.0.0'

    @staticmethod
    def enter_data_int():
        user_data = int(input('>> '))
        return user_data

    @staticmethod
    def enter_data_str():
        user_data = input('>> ')
        return user_data


class Format:
    """
    Utility class for text formater
    Includes print functions in different colors and underline technology.
    """
    underline_end: Final[str] = '\033[0m'
    underline_start: Final[str] = '\033[4m'

    @staticmethod
    def prRed(string: str):
        print("\033[91m {}\033[00m".format(string))

    @staticmethod
    def prGreen(string: str):
        print("\033[92m {}\033[00m".format(string))

    @staticmethod
    def prYellow(string: str):
        print("\033[93m {}\033[00m".format(string))

    @staticmethod
    def prCyan(string: str):
        print("\033[96m {}\033[00m".format(string))


class Suit:
    start_suit_path: str
    suit_files: list[str]  # list with suit files
    all_suit_questions: list[str]

    def __init__(self, suit_start):
        self.start_suit_path = suit_start
        self.all_suit_questions = list()

    def show_suit_files(self):
        for num, suit in enumerate(self.suit_files, start=1):
            print(f'{num}: {suit}')

    def get_statistics(self) -> None:
        file_handler = open(Global_statement.main_file_name, 'w+')
        main_file_data = file_handler.readlines()
        try:
            stat_start = main_file_data.index('#Statistics:')  # special commentary for statistics
        except ValueError:
            Format.prRed('No statistics in this suit, create partition')
            file_handler.write('\n#Statistics:')

    def later_todo(self):
        """
        Return to user questions that he needs to learn later
        :return: None
        """
        if len(Global_statement.questions_to_learn) > 0:
            with open(f'{Global_statement.later_learn_filename}-{datetime.datetime.now().date()}.txt', 'a+') as todo_file:
                for todo_line in Global_statement.questions_to_learn:
                    todo_file.write(todo_line if isinstance(todo_line, str) else todo_line[0])
                    todo_file.write('\n')
            Format.prYellow('Questions to learn are written to file')
        else:
            Format.prGreen('No to do questions')

    def add_statistics(self):
        with open(Global_statement.main_file_name, 'w+') as main_file:
            pass

    def get_question_count(self):
        return len(self.all_suit_questions)

    def get_questions(self):
        """
        Get questions from file and randomize them
        :return: None
        """
        # learn file processing
        try:
            main_file_data: list[str] = open(self.start_suit_path + os.sep + Global_statement.main_file_name, 'r').readlines()

            for _, value in enumerate(main_file_data):

                # Local import branch:
                if value.startswith('.Import_local'):
                    _, file_to_import = value.split(' ')

                    full_path: str = self.start_suit_path + os.sep + file_to_import.strip()
                    if exists(full_path):
                        self.all_suit_questions.extend(proceed_import_file(full_path))
                        continue
                    else:
                        Format.prRed('File to import is not exist')

                # Global import directive:
                elif value.startswith('.Import_global'):
                    _, name_to_resolve = value.split(' ')
                    global_path = App.resolve_global(name_to_resolve)
                    if global_path is not None:
                        self.all_suit_questions.extend(proceed_import_file(global_path))
                        continue

                # comment branch:
                if value != '\n' and not value.startswith('#'):  # comment symbol
                    self.all_suit_questions.append(value.strip())

            if len(self.all_suit_questions) > 0:
                random.shuffle(self.all_suit_questions)  # randomize questions before run
                Format.prYellow('All questions are up to date and shuffled')
            else:
                raise Exception('Learn file is empty')
        except Exception as e:
            Format.prRed(f'Some exception occurred during question task - {e}')
            exit(1)


class App:

    def __init__(self):
        try:
            self.all_file_data = dict()
            self.start_path = Path().parent.absolute().as_posix()
            self.question_runner = App.Question_runner(args, self.start_path)
        except Exception as e:
            Format.prRed(f'Failed to initialize app with error {e}')

    def __check_for_all(self):
        """
        Check for all file with paths
        :return: None
        """
        if not exists(self.start_path + os.sep + 'all.txt'):
            Format.prRed('All file is not created, auto create')

        with open(self.start_path + os.sep + 'all.txt', 'w+') as all_file:
            for line in all_file:
                glob_name, glob_path = line.split('=')
                Global_statement.all_file_data[glob_name] = glob_path

    def start_app(self):
        try:
            self.__check_for_all()
            self.question_runner.init()
            self.question_runner.run_question_runner()
        except Exception as e:
            Format.prRed(f'Failed to start app with error - {e}')

    @staticmethod
    def resolve_global(dependency_name: str) -> str | None:
        """
        Resolve global dependencies from all file
        :return: string path to global dependency or None otherwise
        """
        if dependency_name in Global_statement.all_file_data:
            return Global_statement.all_file_data[dependency_name]
        else:
            Format.prRed(f'Wrong global value - {dependency_name}')
            return None

    class Question_runner:
        suits: OrderedDict[str, Suit]  # key - suit name, value - suit

        def __init__(self, args: list, start_path: str | Path):
            self.start_path = start_path
            self.args_count = len(args) - 1  # delete program name from arguments

        def init(self):
            """
            Post init method to create question suits
            :return: None
            """
            dirs = list(filter(lambda x: not x.startswith('.'), os.listdir(self.start_path)))
            if len(dirs) > 0:
                self.suits = OrderedDict()
                for dir in dirs:
                    if self.is_suit(dir):  # todo parallelize
                        self.suits[dir] = Suit(dir)
            else:
                Format.prRed('No files found')
                exit(1)

        def run_question_runner(self):
            active_suit: Suit = None
            # parameters branch:
            if self.args_count == 1:
                # if I want to add another console parameters
                match args[1]:
                    case 'new-suit' | 'ns':
                        Format.prYellow('Enter file name:')
                        user_file_name: str = Global_statement.enter_data_str()
                        with open(user_file_name + '.txt', 'w+') as new_file:
                            new_file.write(f'#{user_file_name} suit: \n')  # add suit name
                            new_file.write('#<Question text>|<Optional answer>\n')  # add instruction
                        exit(0)  # exit after creation

                    case 'help' | 'h':
                        Format.prGreen('"new-suit" for creating new suit')
                        Format.prGreen('also available first argument is path to directory with learn files')
                        exit(0)

                    case _:
                        Format.prRed(f'Unknown start parameter {args[1]}')
                        exit(0)

            # local start branch:
            elif self.args_count == 0:
                suits_key: Final[list[str]] = list()
                if len(self.suits) > 1:
                    Format.prYellow('Detected several available suits:')
                    for suit_num, suit_name in enumerate(self.suits):
                        print(f'{suit_num}: {suit_name}')
                        suits_key.append(suit_name)  # add suit name into keys
                    while True:
                        Format.prYellow('Choose suit to run by its number')
                        user_choice = Global_statement.enter_data_int()
                        if user_choice in range(len(self.suits)):
                            active_suit = self.suits[suits_key[user_choice]]
                            break
                        else:
                            Format.prRed('Try again')
                            continue

                elif len(self.suits) == 1:
                    active_suit = list(self.suits.items())[0][1]

                if active_suit is not None:
                    active_suit.get_questions()  # try search for current directory anyway
                else:
                    Format.prRed('No active suit')
                    exit(1)

            else:
                Format.prRed('No CLI arguments passed')
                exit(1)

            # main utility logic:
            question_counter: int = 0
            all_questions_count: Final[int] = active_suit.get_question_count()
            while True:
                current_question: str | list[str] = active_suit.all_suit_questions[question_counter]  # str for old format

                # new question method (with answer)
                if current_question.__contains__("|"):
                    current_question = current_question.split("|")
                    current_question = list(filter(None, current_question))

                if len(current_question) > 0:
                    print('\n')
                    Format.prCyan(f'{question_counter + 1}/{all_questions_count}: "{current_question.capitalize() if isinstance(current_question, str) else current_question[0].capitalize()}"')
                    Format.prYellow('Enter "pass" (p) to pass question,')
                    Format.prYellow('Enter "no"   (n) if you do not know answer,')
                    Format.prYellow('Enter "help" (h) to view answer,')
                    Format.prYellow('Enter "save" (s) to save question for later learning,')
                    Format.prYellow('Enter "exit" (e) to exit program.')
                    choice = Global_statement.enter_data_str()
                    match choice:
                        case 'pass' | 'p':
                            question_counter += 1
                            if all_questions_count == question_counter:
                                break
                            continue

                        case 'no' | 'n':
                            Format.prRed('Later check this question')
                            Global_statement.questions_to_learn.append(current_question)
                            question_counter += 1

                        case 'help' | 'h':
                            if isinstance(current_question, list):
                                if len(current_question) > 1:
                                    Format.prGreen(f'Answer: {current_question[1].capitalize()}')
                                else:
                                    Format.prRed('No answer available')
                            else:
                                Format.prRed('No answer available')

                        case 'save' | 's':
                            Format.prYellow('Save question for later study')
                            if not Global_statement.questions_to_learn.__contains__(current_question):
                                Global_statement.questions_to_learn.append(current_question)
                            else:
                                Format.prRed('Question already saved')

                        case 'exit' | 'e':
                            break

                        case _:
                            Format.prRed('Wrong value, try again')
                else:
                    question_counter += 1
                    continue

            finish_time = datetime.datetime.now()
            Format.prYellow(f'learning time - {(finish_time - Global_statement.start_time)}')
            active_suit.later_todo()

        @staticmethod
        def is_suit(maybe_suit_name: str) -> bool:
            if os.path.isdir(maybe_suit_name):
                if Global_statement.main_file_name in os.listdir(maybe_suit_name):
                    return True
            return False


def signal_handler(sig, frame):
    """
    Handle sig int command
    :param sig: signal
    :param frame: function to execute in case of signal
    :return: None
    """
    print('\n')
    Global_statement.finish_time = datetime.datetime.now()
    Format.prYellow(f'learning time - {(Global_statement.finish_time - Global_statement.start_time)}')
    Format.prYellow("Out program")
    exit(0)


def proceed_import_file(path_to_read: str | Path) -> list[str]:
    """
    Proceed file to import and return its data
    :param path_to_read:
    :return: list with file data
    """
    to_return: list[str] = list()
    with open(path_to_read, 'r') as import_file:
        for line in import_file:
            if line != '\n' and not line.startswith('#'):  # comments
                to_return.append(line.strip())
            # TODO
            # elif line.startswith(): #functions
            #     pass
    return to_return


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # if program goes wrong

    args: Final[list[str]] = sys.argv
    app = App()
    app.start_app()
