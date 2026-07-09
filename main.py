import argparse
import datetime
import os.path
import random
import signal
import sys
from collections import OrderedDict
from os.path import exists
from pathlib import Path
from typing import Final, Protocol

import requests

os.environ['TERM'] = 'xterm-256color'


class Data_driver(Protocol):
    """
    Save questions on remote drive or load them to local
    """

    def close_driver(self) -> None: ...

    def upload_questions(self) -> None: ...

    def load_questions_from_remote(self) -> None: ...


class Yandex_driver:
    def close_driver(self) -> None:
        pass

    def upload_questions(self) -> None:
        pass

    def load_questions_from_remote(self) -> None:
        pass


class Google_driver:
    def close_driver(self) -> None:
        pass

    def upload_questions(self) -> None:
        pass

    def load_questions_from_remote(self) -> None:
        pass


class AI:
    """
    Class for generating answer to question if it not written
    """

    def __init__(self):
        pass

    def generate_answer(self, question: str) -> str | None:
        """
        Generate answer with AI (yeah, i know)
        :param question: question to search for
        :return: string value of question
        """
        Format.prYellow('Wait for response from AI')
        response = requests.get(f'https://yandex.ru/alice/chat&source_query={question}')
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        title_element = soup.find('textarea')
        title = title_element.string
        if title != '':
            return title
        else:
            Format.prRed('No answer from AI')
            return None


class Flags:
    """
    Utility flags
    """
    is_random_run: Final[bool] = True  # sequential order if false and random otherwise
    verbose_mode: Final[bool] = True  # output suit name when run
    debug_mode: Final[bool] = False  # for debug msgs
    high_prior: Final[bool] = False  # run only high priority questions
    is_ai_generating_answer: Final[bool] = False  # generate every answer with AI


class Global_statement:
    """
    Some constants and global data
    """
    # containers
    questions_to_learn: Final[list[str | list[str]]] = list()  # to do learn
    all_file_data: Final[dict[str, str | Path]] = dict()  # available paths and variables

    # time functionality:
    start_time: Final[datetime.datetime] = datetime.datetime.now()
    finish_time: datetime.datetime

    # consts:
    later_learn_filename: Final[str] = 'todo-learn'
    main_file_name: Final[str] = 'main'
    all_file_name: Final[str] = 'all'
    app_version: Final[str] = '2.3.1'


class Global_functions:
    class Function_id:
        decide_id_sym: str = 'Decide'
        dynamic_id_sym: str = 'Dynamic_import'

    @staticmethod
    def decide(var_name: str):
        if var_name in Global_statement.all_file_data:
            pass
        else:
            Format.prRed(f'No global variable found with name - {var_name}')

    @staticmethod
    def dynamic_import(var_name: str):
        pass


class Syntax_rules:
    """
    Syntax rules for suits
    """
    # suit file consts:
    global_import_directive: Final[str] = '.Import_global'
    local_import_directive: Final[str] = '.Import_local'
    function_directive: Final[str] = '$Func'
    comment_symbol: Final[str] = '#'
    suit_name_symbol: Final[str] = '^'

    statistics_symbol: Final[str] = '#Statistics:'

    # all file config:
    variable_prefix: Final[str] = 'Var'
    path_prefix: Final[str] = 'Path'


class Format:
    """
    Utility class for text formater
    Includes print functions in different colors and underline technology.
    """

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

    @staticmethod
    def prUnderline(string: str):
        print("\033[4m {}\033[0m".format(string))


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
            stat_start = main_file_data.index(Syntax_rules.statistics_symbol)  # special commentary for statistics
        except ValueError:
            Format.prRed('No statistics in this suit, create partition')
            file_handler.write('\n#Statistics:')

    def later_todo(self) -> None:
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

    def get_question_count(self) -> int:
        return len(self.all_suit_questions)

    def get_questions(self):
        """
        Get questions from file and randomize them
        :return: None
        """
        # learn file processing
        try:
            main_file_data: list[str] = open(self.start_suit_path + os.sep + Global_statement.main_file_name, 'r').readlines()

            for _, suit_line in enumerate(main_file_data):

                # Local import branch:
                if suit_line.startswith(Syntax_rules.local_import_directive):
                    _, file_to_import = suit_line.split(' ')

                    proceed_import_file(self.start_suit_path + os.sep + file_to_import.strip(), self)
                    continue

                # Global import directive:
                elif suit_line.startswith(Syntax_rules.global_import_directive):
                    _, name_to_resolve = suit_line.split(' ')

                    if '.txt' in name_to_resolve:  # only global name, not path to file
                        raise Exception('Global name should not contain path to file')

                    proceed_import_file(App.resolve_global(clear_string(name_to_resolve)), self)
                    continue

                # comment branch:
                if suit_line != '\n' and not suit_line.startswith(Syntax_rules.comment_symbol):  # comment symbol
                    self.all_suit_questions.append(clear_string(suit_line))

            if len(self.all_suit_questions) > 0:
                if Flags.is_random_run:
                    self.all_suit_questions = fisher_yates_shuffle(self.all_suit_questions)  # randomize questions before run
                    Format.prYellow('All questions are up to date and shuffled')
                else:
                    Format.prYellow('Run in sequential mode')
            else:
                raise Exception('Learn file is empty')
        except Exception as e:
            if Flags.debug_mode:
                pass
                # TODO print all import suits name
            handle_critical_error(f'Critical exception during question task - {e}')


class App:

    def __init__(self):
        try:
            self.all_file_data = dict()
            self.start_path = Path().parent.absolute().as_posix()
            self.question_runner = App.Question_runner(self.start_path)
        except Exception as e:
            handle_critical_error(f'Failed to initialize app with error {e}')

    def __check_for_all(self):
        """
        Check for all file with paths
        :return: None
        """
        if not exists(self.start_path + os.sep + Global_statement.all_file_name):
            Format.prRed('All file is not created, auto create all file')
            open(self.start_path + os.sep + Global_statement.all_file_name, 'r').close()

        file_data = open(self.start_path + os.sep + Global_statement.all_file_name, 'r').readlines()

        for line in file_data:
            if line != '' and '=' in line:

                # path path:
                if line.startswith(Syntax_rules.path_prefix):
                    line = line.removeprefix(Syntax_rules.path_prefix)
                    glob_name, glob_path = line.split('=')
                    Global_statement.all_file_data[clear_string(glob_name)] = clear_string(glob_path)

                # variable path:
                elif line.startswith(Syntax_rules.variable_prefix):
                    line = line.removeprefix(Syntax_rules.variable_prefix)
                    glob_name, glob_path = line.split('=')
                    Global_statement.all_file_data[clear_string(glob_name)] = clear_string(glob_path)

                else:
                    Format.prRed(f'Unknown parameter line in all file {line}')

    def start_app(self):
        """
        Main app pipeline
        :return: None
        """
        try:
            self.__check_for_all()
            clear_screen()
            self.question_runner.run_question_runner()
        except Exception as e:
            handle_critical_error(f'Failed to start app with error - {e}')

    @staticmethod
    def resolve_global(dependency_name: str) -> str | None:
        """
        Resolve global dependencies from all file
        :return: string path to global dependency or None otherwise
        """
        if dependency_name in Global_statement.all_file_data:
            return Global_statement.all_file_data[dependency_name]
        else:
            Format.prRed(f'No global value found - {dependency_name}, return None instead')
            return None

    class Question_runner:
        _suits: OrderedDict[str, Suit]  # key - suit name, value - suit

        def __init__(self, start_path: str | Path):
            self.start_path = start_path
            dirs = list(filter(lambda x: not x.startswith('.'), os.listdir(self.start_path)))
            if Flags.is_ai_generating_answer:
                self.ai_gen = AI()
            if len(dirs) > 0:
                self._suits = OrderedDict()
                for dir in dirs:
                    if self.is_suit(dir):
                        self._suits[dir] = Suit(dir)
            else:
                handle_critical_error('No files found')

        def run_question_runner(self):
            """
            Run main app activity
            :return: None
            """
            active_suit: Suit = None
            # parameters branch:
            if args_length == 1:
                # if I want to add another console parameters
                match args[1]:
                    case 'new-suit' | 'ns':
                        Format.prYellow('Enter file name:')
                        user_file_name: str = enter_data_str()
                        with open(user_file_name, 'w+') as new_file:
                            new_file.write(f'#{user_file_name} suit: \n')  # add suit name
                            new_file.write('#<Question text>|<Optional answer>\n')  # add instruction
                        exit(0)  # exit after creation

                    case 'help' | 'h':
                        Format.prGreen('"new-suit" for creating new suit')
                        Format.prGreen('also available first argument is path to directory with learn files')
                        exit(0)

                    case _:
                        handle_critical_error(f'Unknown start parameter {args[1]}')

            # local start branch:
            elif args_length == 0:
                suits_key: Final[list[str]] = list()
                if len(self._suits) > 1:
                    Format.prYellow('Detected several available suits:')
                    for suit_num, suit_name in enumerate(self._suits):
                        print(f'{suit_num}: {suit_name}')
                        suits_key.append(suit_name)  # add suit name into keys

                    while True:
                        Format.prYellow('Choose suit to run by its number or type 666 to exit')
                        user_choice = enter_data_int()
                        if user_choice == 666:
                            Format.prYellow('Exit from utility')
                            exit(0)
                        if user_choice in range(len(self._suits)):
                            active_suit = self._suits[suits_key[user_choice]]
                            break
                        else:
                            Format.prRed('Try again')
                            continue

                elif len(self._suits) == 1:
                    active_suit = list(self._suits.items())[0][1]

                if active_suit is not None:
                    active_suit.get_questions()  # try search for current directory anyway
                else:
                    handle_critical_error('No active suit')

            else:
                handle_critical_error('No CLI arguments passed')

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

                    if Flags.verbose_mode:
                        # print suit name:
                        Format.prYellow(f'Question suit: {current_question[-1].removeprefix(Syntax_rules.suit_name_symbol)}')

                    # print other question data:
                    Format.prYellow('Enter "pass"   (p) to pass question,')
                    Format.prYellow('Enter "no"     (n) if you do not know answer,')
                    Format.prYellow('Enter "help"   (h) to view answer,')
                    Format.prYellow('Enter "save"   (s) to save question for later learning,')
                    Format.prYellow('Enter "reload" (r) to reload question suit,')
                    Format.prYellow('Enter "exit"   (e) to exit program.')
                    choice: str = enter_data_str()
                    match choice:
                        case 'pass' | 'p':
                            question_counter += 1
                            if all_questions_count == question_counter:
                                break
                            clear_screen()
                            continue

                        case 'no' | 'n':
                            Format.prRed('Later check this question')
                            Global_statement.questions_to_learn.append(current_question)
                            question_counter += 1
                            clear_screen()

                        case 'help' | 'h':
                            if Flags.is_ai_generating_answer:
                                Format.prGreen(f'Answer: {self.ai_gen.generate_answer(current_question)}')
                            else:
                                if isinstance(current_question, list):
                                    if len(current_question[1]) > 1 and not current_question[1].startswith(Syntax_rules.suit_name_symbol):  # bug fix, when question line with 2 or 3
                                        Format.prGreen(f'Answer: {current_question[1].capitalize()}')
                                    else:
                                        Format.prRed('No answer available')
                                else:
                                    Format.prRed('No answer available')

                        case 'save' | 's':
                            Format.prYellow('Save question for later study')
                            if not current_question in Global_statement.questions_to_learn:
                                Global_statement.questions_to_learn.append(current_question)
                            else:
                                Format.prRed('Question already saved')

                        case 'reload' | 'r':
                            Format.prYellow('Reload')
                            pass

                        case 'exit' | 'e':
                            if question_counter < all_questions_count:
                                Format.prYellow(f'Solved only {question_counter}/{all_questions_count}, session is not ended')
                                Format.prYellow('Do you want to save current session for later continue? (y/n)')
                                while True:
                                    user_choice: str = enter_data_str()
                                    match user_choice:
                                        case 'y' | 'yes':
                                            Format.prGreen('Saving file')
                                            with open(f'savefile-{datetime.date.today()}.txt', 'w+') as save_file:
                                                for question_line in range(question_counter, all_questions_count):
                                                    save_file.write(active_suit.all_suit_questions[question_line])
                                                    save_file.write('\n')
                                            Format.prGreen('Save complete')
                                            break

                                        case 'n' | 'no':
                                            Format.prGreen('No save')
                                            break

                                        case _:
                                            Format.prRed('Wrong value added, try again')
                                            continue
                                break
                            else:
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


def proceed_import_file(path_to_read: str | Path, suit: Suit) -> None:
    """
    Proceed file to import and return its data
    :param suit: suit to add data
    :param path_to_read: full path to file with data
    :return: list with file data
    """
    if path_to_read is None:
        return
    if exists(path_to_read):
        to_return: Final[list[str]] = list()
        with open(path_to_read, 'r') as import_file:
            suit_name: Final[str] = import_file.name  # add suit name

            for line in import_file:
                if line != '\n' and not line.startswith(Syntax_rules.comment_symbol):  # comments
                    if Flags.verbose_mode:
                        line += f'|{Syntax_rules.suit_name_symbol}{suit_name}'  # append additional data only in case of verbose flag

                    to_return.append(clear_string(line))

                # experimental feature, nested suits
                elif line.startswith(Syntax_rules.global_import_directive) or line.startswith(Syntax_rules.local_import_directive):
                    _, file_to_include = line.split('=')
                    proceed_import_file(clear_string(file_to_include), suit)

                elif line.startswith(Syntax_rules.function_directive):  # functions
                    pass
        suit.all_suit_questions.extend(to_return)
    else:
        Format.prRed(f'Path to import file is not exists: {path_to_read}')


def clear_screen() -> None:
    os.system('clear')


def fisher_yates_shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def enter_data_int():
    user_data = int(input('>> '))
    if user_data is not None:
        return user_data


def enter_data_str():
    user_data = input('>> ')
    return user_data


def clear_string(string: str) -> str:
    return string.strip()


def handle_critical_error(msg: str):
    Format.prRed(msg)
    exit(1)


def handle_non_major_error(msg: str):
    Format.prRed(msg)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # if program goes wrong

    parser = argparse.ArgumentParser('Learn-help', description='App for learning')
    parser.add_argument('-ns', '--new-suit', action='store', help='create new test suit with name', required=False)

    args_length: Final[int] = len(sys.argv) - 1  # delete program name from arguments
    args: Final[list[str]] = sys.argv if args_length > 1 else []
    ns = parser.parse_args(args)

    app = App()
    app.start_app()
