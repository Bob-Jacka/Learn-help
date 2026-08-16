"""
Your training camp on path to your favourite work,
Learn new by repeating boring questions again and again.
"""

import argparse
import datetime
import os.path
import random
import signal
import subprocess
import sys
from argparse import Namespace
from collections import OrderedDict
from enum import Enum
from os.path import exists
from pathlib import Path
from typing import Final

try:
    from PyQt6 import QtWidgets
    from PyQt6.QtWidgets import QMessageBox, QDialog

    from AI import AI
    from UI import UI, Choose_suit_dialog
    from device_lib.devices.virtual import IVirtDevice
    from common_py_lib.entities.Formatter import TextAnsiFormatter
    from common_py_lib.actions.Input import *
except Exception as e:
    print(f'No available modules found: {e}')

os.environ['TERM'] = 'xterm-256color'
start_path: Final[str] = Path().parent.absolute().as_posix()


class Question:
    """
    Just marker class for questions
    """
    question: str


class Simple_question(Question):
    answer: str | None


class Question_with_variants(Question):
    """
    Question with several options,
    example:
    What came before
    1. Egg,
    2. Chicken

    or maybe more options
    """
    variants: dict[int, str]


class Question_with_ai_check(Question):
    """
    User answers and AI check this answer
    """

    def get_answer(self):
        pass


class Question_with_timer(Question):
    """
    Small time to answer question
    """
    time_to_wait: Final[int] = 10  # how many seconds to wait for answer
    answer: str | None


class Task_with_writing_code(Question):
    """
    Give user a task and wait him to answer, then show correct answer
    """
    answer: str | None


class Suit:
    """
    Aka directory with text files, where stored questions
    """
    start_suit_path: str
    suit_files: list[str]  # list with suit files names
    all_suit_questions: list[str | Question]

    def __init__(self, suit_start):
        self.start_suit_path = suit_start
        self.all_suit_questions = list()

    def get_suit_questions(self) -> list[str | Question]:
        return self.all_suit_questions

    @staticmethod
    def is_suit(maybe_suit_name: str) -> bool:
        """
        Check that directory is suit by contract
        :param maybe_suit_name: path or name of suit
        :return: bool result
        """
        if os.path.isdir(maybe_suit_name):
            if App.Global_statement.main_file_name in os.listdir(maybe_suit_name):
                return True
        return False

    def show_suit_files(self):
        for num, suit in enumerate(self.suit_files, start=1):
            print(f'{num}: {suit}')

    def get_statistics(self) -> None:
        file_handler = open(App.Global_statement.main_file_name, 'w+')
        main_file_data = file_handler.readlines()
        try:
            stat_start = main_file_data.index(App.Syntax_rules.statistics_symbol)  # special commentary for statistics
        except ValueError:
            TextAnsiFormatter.prRed('No statistics in this suit, create partition')
            file_handler.write('\n#Statistics:')

    def later_todo(self) -> None:
        """
        Return to user questions that he needs to learn later
        :return: None
        """
        if len(App.Global_statement.questions_to_learn) > 0:
            with open(f'{App.Global_statement.later_learn_filename}-{datetime.datetime.now().date()}.txt', 'a+') as todo_file:
                for todo_line in App.Global_statement.questions_to_learn:
                    todo_file.write(todo_line if isinstance(todo_line, str) else todo_line[0])
                    todo_file.write('\n')
            TextAnsiFormatter.prYellow('Questions to learn are written to file')
        else:
            TextAnsiFormatter.prGreen('No to do questions')

    def get_question_count(self) -> int:
        return len(self.all_suit_questions)

    def change_suit(self) -> bool:
        """
        Dynamic change suits when run
        :return: bool result of changing suit
        """
        # TODO
        pass

    @staticmethod
    def get_suit_name(question_line: list) -> str:
        # TODO cut path to suit
        return question_line[-1].removeprefix(App.Syntax_rules.suit_name_symbol)

    def get_questions(self):
        """
        Get questions from file and randomize them
        :return: None
        """
        # learn file processing
        try:
            main_file_data: list[str] = open(self.start_suit_path + os.sep + App.Global_statement.main_file_name, 'r').readlines()

            for suit_line in main_file_data:

                # Local import branch:
                if suit_line.startswith(App.Syntax_rules.local_import_directive):
                    # TODO add * (start) parameter, add local files with one import directive
                    _, file_to_import = suit_line.split(' ')

                    proceed_import_file(self.start_suit_path + os.sep + file_to_import.strip(), self)
                    continue

                # Global import directive:
                elif suit_line.startswith(App.Syntax_rules.global_import_directive):
                    _, name_to_resolve = suit_line.split(' ')

                    if '.txt' in name_to_resolve:  # only global name, not path to file
                        raise Exception('Global name should not contain path to file')

                    proceed_import_file(App.resolve_global_dep(clear_string(name_to_resolve)), self)
                    continue

                # comment branch:
                if suit_line != '\n' and not suit_line.startswith(App.Syntax_rules.comment_symbol):  # comment symbol
                    self.all_suit_questions.append(clear_string(suit_line))

            if len(self.all_suit_questions) > 0:
                if App.Flags.is_random_run:
                    self.all_suit_questions = fisher_yates_shuffle(self.all_suit_questions)  # randomize questions before run
                    TextAnsiFormatter.prYellow('All questions are up to date and shuffled')
                else:
                    TextAnsiFormatter.prYellow('Run in sequential mode')
                    # TODO
                    # TODO
            # else:
            #     if App.data_driver is None:
            #         TextAnsiFormatter.prRed('Cannot use Data driver, because driver is None')
            #         raise Exception('Learn file is empty, cannot execute')
            #     else:
            #         # TODO
            #         TextAnsiFormatter.prGreen('Using Data driver to load questions')
            #         self.all_suit_questions = App.data_driver.load_questions_from_remote()
        except Exception as e:
            if App.Flags.debug_mode:
                TextAnsiFormatter.prRed(f'Using start path - {self.start_suit_path}')
                for file in self.suit_files:
                    print(file)
            handle_critical_error(f'Critical exception during question task - {e}')


class App:
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

    class Global_statement:
        """
        Some constants and global data in one class
        """
        # containers
        questions_to_learn: Final[list[str | list[str]]] = list()  # to do learn
        tasks_data: Final[dict[str, str]] = dict()
        all_file_data: Final[dict[str, str]] = dict()  # available paths and variables

        # time functionality:
        start_time: Final[datetime.datetime] = datetime.datetime.now()
        finish_time: datetime.datetime

        # consts:
        later_learn_filename: Final[str] = 'todo-learn'
        main_file_name: Final[str] = '__main__'
        all_file_name: Final[str] = '__all__'
        global_dir_name: Final[str] = '__global__'
        tasks_dir_name: Final[str] = '__tasks__'
        app_version: Final[str] = '2.5.1'

    class Global_functions:
        class Function_id:
            decide_id_sym: str = 'Decide'
            dynamic_id_sym: str = 'Dynamic_import'

        @staticmethod
        def decide(var_name: str):
            """
            Decide conditions in suit
            :param var_name: expression
            :return:
            """
            if var_name in App.Global_statement.all_file_data:
                pass
            else:
                TextAnsiFormatter.prRed(f'No global variable found with name - {var_name}')

        @staticmethod
        def dynamic_import(var_name: str):
            pass

        @staticmethod
        def as_a_separate_suit(separate_suit_name: str):
            """
            Use sub suit as a separate suit, ex. you have sub suit, called qa, which has cucumber questions
            and you want to use this sub suit as a suit, without main file.
            ex. ex. $Func separe_suit(cucumber)
            :param separate_suit_name: name of the sub suit
            :return: None
            """
            pass

        @staticmethod
        def ask_ai_about_which_suit_to_run(skills_for_job: list[str]):
            pass

    class Flags:
        """
        Utility flags
        """

        class App_mode(str, Enum):
            GRAPHICAL = 'graphical'
            CONSOLE = 'console'
            WEB_SERV = 'web'
            DEV = 'dev'

        is_random_run: bool = True  # sequential order if false and random otherwise
        verbose_mode: bool = False  # output suit name when run and other control hints
        debug_mode: bool = False  # for debug msgs
        high_prior: bool = False  # run only high priority questions
        is_ai_generating_answer: bool = False  # generate every answer with AI
        app_mode: App_mode  # False for console mode and True for graphical user interface

        def turn_on_flags(self) -> None:
            self.is_random_run = ns['random_run']
            self.verbose_mode = ns['verbose_mode']
            self.debug_mode = ns['debug_mode']
            self.high_prior = ns['high_prior']
            self.is_ai_generating_answer = ns['ai']

    class Statistics:
        def print_statistics(self):
            pass

    class Question_runner:
        _suits: OrderedDict[str, Suit]  # key - suit name, value - suit

        def __init__(self):
            suits = App.get_suits()
            self._suits = suits if suits is not None else OrderedDict()
            if App.Flags.app_mode == App.Flags.App_mode.GRAPHICAL:
                self.outer_app = QtWidgets.QApplication(args)
                self.main_window: Final[UI] = UI()
                self.main_window.setup_slots()
                self.main_window.show()

        def run_question_runner_graphical(self):
            """
            Run main app activity in graphical user interface
            :return: None
            """
            suits_key: Final[list[str]] = list()
            active_suit: Suit = None
            if len(self._suits) > 1:
                for suit_num, suit_name in enumerate(self._suits):
                    suits_key.append(suit_name)  # add suit name into keys

                QMessageBox(QMessageBox.Icon.Information, 'Info', 'Detected several available suits:').exec()

                msg_box = QMessageBox.question(None, "Question", "Would you like to take first (Yes) or see all suits (No)", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if msg_box == QMessageBox.StandardButton.Yes:
                    active_suit = list(self._suits.items())[0][1]
                else:
                    # if user wants to choose suit by himself
                    combo_suits = Choose_suit_dialog(options=self._suits)
                    if combo_suits.exec() == QDialog.DialogCode.Accepted:
                        chosen_suit = combo_suits.result
                    else:
                        chosen_suit = ""

                    active_suit = self._suits[chosen_suit]


            elif len(self._suits) == 1:
                active_suit = list(self._suits.items())[0][1]  # if only one suit, just take first

            active_suit.get_questions()
            all_questions_count: Final[int] = active_suit.get_question_count()  # how many questions to run
            question_counter: int = 0  # position of question in suit
            while True:
                current_question: str | list[str] = active_suit.all_suit_questions[question_counter]  # str for old textAnsiFormatter
                self.main_window.take_question(current_question)
                # TODO there is a problem with stopping app in infinity loop

        def run_question_runner_console(self):
            """
            Run main app activity in console
            :return: None
            """
            active_suit: Suit = None
            # parameters branch:
            if args_length == 1:
                # if I want to add another console parameters
                match args[1]:
                    case 'new-suit' | 'ns':
                        App.str_input_data = str_input_from_user('Enter file name:')
                        with open(App.str_input_data, 'w+') as new_file:
                            new_file.write(f'#{App.str_input_data} suit: \n')  # add suit name
                            new_file.write('#<Question text>|<Optional answer>\n')  # add instruction
                        exit(0)  # exit after creation

                    case 'help' | 'h':
                        TextAnsiFormatter.prGreen('"new-suit" for creating new suit')
                        TextAnsiFormatter.prGreen('also available first argument is path to directory with learn files')
                        exit(0)

                    case _:
                        handle_critical_error(f'Unknown start parameter {args[1]}')

            # local start branch:
            elif args_length == 0:
                suits_key: Final[list[str]] = list()
                if len(self._suits) > 1:
                    TextAnsiFormatter.prYellow('Detected several available suits:')
                    for suit_num, suit_name in enumerate(self._suits):
                        print(f'{suit_num}: {suit_name}')
                        suits_key.append(suit_name)  # add suit name into keys

                    while True:
                        TextAnsiFormatter.prYellow('Choose suit to run by its number or type 666 to exit')
                        App.int_input_data = int_input_from_user()
                        if App.int_input_data == 666:
                            TextAnsiFormatter.prYellow('Exit from utility')
                            exit(0)
                        if App.int_input_data in range(len(self._suits)):
                            active_suit = self._suits[suits_key[App.int_input_data]]
                            break
                        else:
                            TextAnsiFormatter.prRed('Try again')
                            continue

                elif len(self._suits) == 1:
                    active_suit = list(self._suits.items())[0][1]  # if only one suit, just take first

                if active_suit is not None:
                    active_suit.get_questions()
                else:
                    handle_critical_error('No active suit')

            else:
                handle_critical_error('No CLI arguments passed')

            # main utility logic:
            question_counter: int = 0  # position of question in suit
            all_questions_count: Final[int] = active_suit.get_question_count()  # how many questions to run
            if App.Flags.debug_mode:
                print('Run these files in suit:')  # print files that includes in suit
                for num, suit_file in enumerate(active_suit.suit_files):
                    print(f'{num}: {suit_file}')
            while True:
                current_question: str | list[str] = active_suit.all_suit_questions[question_counter]  # str for old textAnsiFormatter

                # new question method (with answer)
                if current_question.__contains__("|"):
                    current_question = current_question.split("|")
                    current_question = list(filter(None, current_question))

                if len(current_question) > 0:
                    print('\n')
                    TextAnsiFormatter.prCyan(
                        f'{question_counter + 1}/{all_questions_count}: "{current_question.capitalize() if isinstance(current_question, str) else current_question[0].capitalize()}"')

                    if App.Flags.verbose_mode:
                        # print suit name:
                        TextAnsiFormatter.prUnderline(f'Question suit: {Suit.get_suit_name(question_line=current_question)}')

                        # print other question data:
                        TextAnsiFormatter.prYellow('Enter "pass"   (p) to pass question,')
                        TextAnsiFormatter.prYellow('Enter "no"     (n) if you do not know answer,')
                        TextAnsiFormatter.prYellow('Enter "help"   (h) to view answer,')
                        # TODO
                        if App.Flags.debug_mode:
                            TextAnsiFormatter.prUnderline('Enter "ans" (a) to add answer')  # to add answer
                            TextAnsiFormatter.prUnderline('Enter "add" (add) to add question to suit')
                            # self._suits[Suit.get_suit_name(current_question)]
                        TextAnsiFormatter.prYellow('Enter "save"   (s) to save question for later learning,')
                        TextAnsiFormatter.prYellow('Enter "reload" (r) to reload question suit,')
                        TextAnsiFormatter.prYellow('Enter "exit"   (e) to exit program.')
                    App.str_input_data = str_input_from_user()
                    match App.str_input_data:
                        case 'pass' | 'p':
                            question_counter += 1
                            if all_questions_count == question_counter:
                                break
                            clear_screen()
                            continue

                        case 'no' | 'n':
                            TextAnsiFormatter.prRed('Later check this question')
                            App.Global_statement.questions_to_learn.append(current_question)
                            question_counter += 1
                            clear_screen()

                        case 'help' | 'h':
                            if App.Flags.is_ai_generating_answer:
                                TextAnsiFormatter.prGreen(f'Answer: {self.ai_gen.generate_answer(current_question)}')
                            else:
                                if isinstance(current_question, list):
                                    if len(current_question[1]) > 1 and not current_question[1].startswith(App.Syntax_rules.suit_name_symbol):  # bug fix, when question line with 2 or 3
                                        TextAnsiFormatter.prGreen(f'Answer: {current_question[1].capitalize()}')
                                    else:
                                        TextAnsiFormatter.prRed('No answer available')
                                else:
                                    TextAnsiFormatter.prRed('No answer available')

                        case 'save' | 's':
                            TextAnsiFormatter.prYellow('Save question for later study')
                            if not current_question in App.Global_statement.questions_to_learn:
                                App.Global_statement.questions_to_learn.append(current_question)
                            else:
                                TextAnsiFormatter.prRed('Question already saved')

                        case 'reload' | 'r':
                            TextAnsiFormatter.prYellow('Reload')
                            pass

                        case 'exit' | 'e':
                            if question_counter < all_questions_count:
                                TextAnsiFormatter.prYellow(f'Solved only {question_counter}/{all_questions_count}, session is not ended')
                                TextAnsiFormatter.prYellow('Do you want to save current session for later continue? (y/n)')
                                while True:
                                    App.str_input_data = str_input_from_user()
                                    match App.str_input_data:
                                        case 'y' | 'yes':
                                            TextAnsiFormatter.prGreen('Saving file')
                                            with open(f'savefile-{datetime.date.today()}.txt', 'w+') as save_file:
                                                for question_line in range(question_counter, all_questions_count):
                                                    save_file.write(active_suit.all_suit_questions[question_line])
                                                    save_file.write('\n')
                                            TextAnsiFormatter.prGreen('Save complete')
                                            break

                                        case 'n' | 'no':
                                            TextAnsiFormatter.prGreen('No save')
                                            break

                                        case _:
                                            TextAnsiFormatter.prRed('Wrong value added, try again')
                                            continue
                                break
                            else:
                                break
                        case _:
                            TextAnsiFormatter.prRed('Wrong value, try again')
                else:
                    question_counter += 1
                    continue

            finish_time = datetime.datetime.now()
            TextAnsiFormatter.prYellow(f'learning time - {(finish_time - App.Global_statement.start_time)}')
            active_suit.later_todo()

    class Task_runner:
        def __init__(self):
            pass

        def run_tasks(self):
            tasks_count = len(App.Global_statement.tasks_data)
            if tasks_count > 1:
                TextAnsiFormatter.prYellow('Detected several tasks suits, choose one:')
                for num, t_suit in enumerate(App.Global_statement.tasks_data):
                    print(f'{num}: {t_suit}')

                App.int_input_data = int_input_from_user()
                if App.int_input_data in tasks_count:
                    pass
                    # active_task_suit = App.Global_statement.tasks_data[]
                    # TODO continue
            else:
                pass

        @staticmethod
        def check_for_tasks():
            """
            Check for directory with practical tasks in App
            :return: None
            """
            path_to_tasks_dir = start_path + os.sep + App.Global_statement.tasks_dir_name
            if exists(path_to_tasks_dir):
                for f_name in os.listdir(path_to_tasks_dir):
                    App.Global_statement.tasks_data[f_name] = path_to_tasks_dir + os.sep + f_name
            else:
                TextAnsiFormatter.prRed('No tasks directory found')

    int_input_data: int
    str_input_data: str

    def __init__(self, namespace: Namespace = None):
        try:
            # create app entities:
            self.ai_gen = AI()
            self.all_file_data: dict[str, str] = dict()
            self.data_driver: IVirtDevice | None = None
            self.statistic = App.Statistics()
            self.task_runner = App.Task_runner()
            self.question_runner = App.Question_runner()
        except Exception as e:
            handle_critical_error(f'Failed to initialize app with error {e}')

    @staticmethod
    def check_for_global() -> None:
        """
        Check for global files (suits)
        :return: None
        """
        if not exists(start_path + os.sep + App.Global_statement.global_dir_name):
            TextAnsiFormatter.prRed('Global data directory is not created, auto create global directory')
            os.mkdir(start_path + os.sep + App.Global_statement.global_dir_name)
        dir_data = os.listdir(start_path + os.sep + App.Global_statement.global_dir_name)
        if len(dir_data) > 0:
            for file_line in dir_data:
                # insert global path as a value
                App.Global_statement.all_file_data[clear_string(file_line.removesuffix('.txt') if '.txt' in file_line else file_line)] = (
                    clear_string(start_path + os.sep + App.Global_statement.global_dir_name + os.sep + file_line))
        else:
            TextAnsiFormatter.prYellow('Global directory is empty, fill it with global files!')

    @staticmethod
    def check_for_all() -> None:
        """
        Check for all file with paths and global variables
        :return: None
        """
        if not exists(start_path + os.sep + App.Global_statement.all_file_name):
            TextAnsiFormatter.prRed('All file is not created, auto create all file')
            open(start_path + os.sep + App.Global_statement.all_file_name, 'r').close()

        file_data = open(start_path + os.sep + App.Global_statement.all_file_name, 'r').readlines()

        for line in file_data:
            if line != '' and '=' in line:

                # path path:
                if line.startswith(App.Syntax_rules.path_prefix):
                    line = line.removeprefix(App.Syntax_rules.path_prefix)
                    glob_name, glob_path = line.split('=')
                    App.Global_statement.all_file_data[clear_string(glob_name)] = clear_string(glob_path)

                # variable path:
                elif line.startswith(App.Syntax_rules.variable_prefix):
                    line = line.removeprefix(App.Syntax_rules.variable_prefix)
                    glob_name, glob_path = line.split('=')
                    App.Global_statement.all_file_data[clear_string(glob_name)] = clear_string(glob_path)

                else:
                    TextAnsiFormatter.prRed(f'Unknown parameter line in all file {line}')

    def start_app(self):
        """
        Main app pipeline
        :return: None
        """
        try:
            # checks for question runner filesystem:
            self.check_for_all()
            self.check_for_global()

            clear_screen()
            # Console mode:
            if App.Flags.app_mode == App.Flags.App_mode.CONSOLE:
                TextAnsiFormatter.prYellow('Choose what to run:')
                print('1. Questions (Theoretical)')
                print('2. Tasks (Practical)')
                App.int_input_data = int_input_from_user()
                match App.int_input_data:
                    case 1:
                        self.question_runner.run_question_runner_console()
                    case 2:
                        App.Task_runner.check_for_tasks()
                        self.task_runner.run_tasks()
                    case _:
                        raise Exception(f'Unknown mode entered: {App.int_input_data}')

            # Web server mode:
            elif App.Flags.app_mode == App.Flags.App_mode.WEB_SERV:
                from Web_module import web_server

                # run uvicorn web server to connect with mobile app
                print(f'Documentation: {web_server.docs_url}')
                subprocess.run("uvicorn Web_module:web_server --reload --host 0.0.0.0 --port 8000", shell=True, capture_output=False, text=True)

            # Dev mode:
            elif App.Flags.app_mode == App.Flags.App_mode.DEV:
                TextAnsiFormatter.prYellow('Choose app action:')
                print('1. Create suit')
                print('2. Append new question to suit')
                print('3. Append new Globap path variable')
                App.int_input_data = int_input_from_user()
                match App.int_input_data:
                    case 1:
                        TextAnsiFormatter.prYellow('Enter suit name:')
                        App.str_input_data = str_input_from_user()
                        new_suit_path = start_path + os.sep + App.str_input_data

                        os.mkdir(new_suit_path)
                        TextAnsiFormatter.prYellow('Created new suit directory')
                        with open(App.str_input_data + os.sep + App.Global_statement.main_file_name, 'w+'):
                            TextAnsiFormatter.prYellow('Created main file for new suit')
                    case 2:
                        # TODo first choose suit
                        TextAnsiFormatter.prYellow('Enter new question')
                        App.str_input_data = str_input_from_user()
                    case 3:
                        TextAnsiFormatter.prYellow('Enter new global path variable name')
                        App.str_input_data = str_input_from_user()
                        with open(start_path + os.sep + App.Global_statement.all_file_name, 'a') as all_file:
                            all_file.write(f'Path {App.str_input_data.split(os.sep)[-1]} = {App.str_input_data}')
                    case _:
                        TextAnsiFormatter.prRed('Wrong option')

            # Graphical mode:
            else:
                self.question_runner.run_question_runner_graphical()
        except Exception as e:
            handle_critical_error(f'Failed to start app with error - {e}')

    def exit_from_app(self):
        if App.Flags.app_mode == App.Flags.App_mode.GRAPHICAL:
            sys.exit(self.question_runner.outer_app.exec())
        self.statistic.print_statistics()

    @staticmethod
    def resolve_global_dep(dependency_name: str) -> str | None:
        """
        Resolve global dependencies from all file
        :return: string path to global dependency or None otherwise
        """
        if dependency_name in App.Global_statement.all_file_data:
            return App.Global_statement.all_file_data[dependency_name]
        else:
            TextAnsiFormatter.prRed(f'No global value found: "{dependency_name}", return "None" instead')
            return None

    @staticmethod
    def get_suits(with_questions: bool = False) -> OrderedDict[str, Suit] | None:
        suits: OrderedDict[str, Suit]
        dirs = list(filter(lambda x: not x.startswith('.'), os.listdir(start_path)))
        if len(dirs) > 0:
            suits = OrderedDict()
            for dir in dirs:
                if Suit.is_suit(dir):
                    suit = Suit(dir)
                    if with_questions:
                        suit.get_questions()  # init questions (parse them)
                    suits[dir] = suit
            return suits
        else:
            handle_critical_error('No files found')
            return None


def proceed_import_file(path_to_read: str | None, suit: Suit) -> None:
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
                if line != '\n' and not line.startswith(App.Syntax_rules.comment_symbol):  # comments
                    if App.Flags.verbose_mode:
                        line += f'|{App.Syntax_rules.suit_name_symbol}{suit_name}'  # append additional data only in case of verbose flag

                    to_return.append(clear_string(line))

                # experimental feature, nested suits
                elif line.startswith(App.Syntax_rules.global_import_directive) or line.startswith(App.Syntax_rules.local_import_directive):
                    _, file_to_include = line.split('=')
                    proceed_import_file(clear_string(file_to_include), suit)

                elif line.startswith(App.Syntax_rules.function_directive):  # functions
                    pass
        suit.all_suit_questions.extend(to_return)
    else:
        TextAnsiFormatter.prRed(f'Path to import file is not exists: "{path_to_read}"')


def signal_handler(sig, frame):
    """
    Handle sig int command
    :param sig: signal
    :param frame: function to execute in case of signal
    :return: None
    """
    print('\n')
    App.Global_statement.finish_time = datetime.datetime.now()
    TextAnsiFormatter.prYellow(f'learning time - {(App.Global_statement.finish_time - App.Global_statement.start_time)}')
    TextAnsiFormatter.prYellow("Out program")
    app.exit_from_app()
    exit(0)


def clear_screen() -> None:
    subprocess.run('clear')


def fisher_yates_shuffle(arr) -> list:
    """
    Random algorithm for random elements in list
    :param arr: sequence with elements
    :return: randomized sequence
    """
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return list(arr)


def clear_string(string: str) -> str:
    return string.strip()


def handle_critical_error(msg: str):
    TextAnsiFormatter.prRed(msg)
    app.exit_from_app()
    exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # if program goes wrong

    TextAnsiFormatter.prYellow('Choose app mode:')
    print('1. Web server (for mobile app transfer data only)')
    print('2. Usual mode (question or task runner in console)')
    print('3. Graphical mode (question or task runner in graphical app)')
    print('4. Dev mode')
    App.int_input_data = int_input_from_user()

    args_length: Final[int] = len(sys.argv) - 1  # delete program name from arguments
    args: Final[list[str]] = sys.argv if args_length > 1 else []

    parser = argparse.ArgumentParser('Learn-help', description='App for learning')
    parser.add_argument('-r', '--random-run', action='store', help='Run questions randomly or sequential', required=False)
    parser.add_argument('-v', '--verbose', action='store', help='More details in messages', required=False)
    parser.add_argument('-d', '--debug', action='store', help='Debug messages', required=False)
    parser.add_argument('-hp', '--high-prior', action='store', help='Run only high priority questions', required=False)
    parser.add_argument('-ai', '--is-ai', action='store', help='Every attempt to see answer will cause AI to generate it', required=False)

    ns = parser.parse_args(args)

    if App.int_input_data == 1:
        App.Flags.app_mode = App.Flags.App_mode.WEB_SERV

    elif App.int_input_data == 2 or App.int_input_data == 3:
        App.Flags.app_mode = App.Flags.App_mode.CONSOLE if App.int_input_data == 2 else App.Flags.App_mode.GRAPHICAL

    elif App.int_input_data == 4:
        App.Flags.app_mode = App.Flags.App_mode.DEV

    else:
        TextAnsiFormatter.prRed('Wrong option selected')
        exit(0)

    app: Final[App] = App(ns)
    app.start_app()
    app.exit_from_app()
