import datetime
import os.path
import random
import signal
import sys
from pathlib import Path
from typing import Final


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


input_sym: Final[str] = '>> '
learn_filename: str  # file with questions to run
later_learn_filename: Final[str] = 'todo-learn'

questions_to_learn: list[str | list[str]] = list()  # to do learn
all_questions: list[str] = list()  # all questions that need to answer

# time functionality:
start_time: Final[datetime.datetime] = datetime.datetime.now()
finish_time: datetime.datetime


def import_suit(suit_name: str) -> list[str] | None:
    pass


def get_questions(path: str | Path):
    """
    Get questions from file and randomize them
    :return: None
    """
    global learn_filename, all_questions
    all_dir_files = list(filter(lambda x: x.__contains__('learn') and not x.__contains__(later_learn_filename), os.listdir(path)))
    all_dir_files_count: Final[int] = len(all_dir_files)

    if all_dir_files_count > 1:
        Format.prYellow('There are more than one file to learn or 666 to exit')
        Format.prYellow('Choose one file:')
        for num, valid_file in enumerate(all_dir_files):
            Format.prCyan(f'{num} - {valid_file}')
        while True:
            user_choice = int(input(input_sym))
            if user_choice == 666:
                exit(0)
            if user_choice in range(all_dir_files_count):
                learn_filename = all_dir_files[user_choice]
                break
            else:
                Format.prRed('Wrong choice, try again')
                continue

    elif all_dir_files_count == 1:
        learn_filename = all_dir_files[0]

    elif all_dir_files_count == 0:
        Format.prRed('No "learn" file detected')
        exit(1)

    # learn file processing
    try:
        # TODO add import directive
        # all_file_data:list[str] = open(learn_filename, 'r').readlines()
        # if all_file_data.__contains__('.Import'):
        #     all_file_data.insert()

        with open(learn_filename, 'r') as question_file:
            for line in question_file:
                if not line.startswith('#'):  # comment symbol
                    all_questions.append(line.strip())
        if len(all_questions) > 0:
            random.shuffle(all_questions)  # randomize questions before run
            all_questions = list(filter(None, all_questions))  # delete empty strings
            Format.prYellow('All questions are up to date and shuffled')
        else:
            raise Exception('Learn file is empty')
    except Exception as e:
        Format.prRed(f'Some exception occurred during question task - {e}')
        exit(1)


def later_todo():
    """
    Return to user questions that he needs to learn later
    :return: None
    """
    if len(questions_to_learn) > 0:
        with open(f'{later_learn_filename}-{datetime.datetime.now().date()}.txt', 'a+') as todo_file:
            for todo_line in questions_to_learn:
                todo_file.write(todo_line if isinstance(todo_line, str) else todo_line[0])
                todo_file.write('\n')
        Format.prYellow('Questions to learn are written to file')
    else:
        Format.prGreen('No to do questions')


def signal_handler(sig, frame):
    """
    Handle sig int command
    :param sig: signal
    :param frame: function to execute in case of signal
    :return: None
    """
    global finish_time
    print('\n')
    finish_time = datetime.datetime.now()
    Format.prYellow(f'learning time - {(finish_time - start_time)}')
    later_todo()
    Format.prYellow("Out program")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # if program goes wrong

    args: Final[list[str]] = sys.argv
    args_count = len(sys.argv) - 1  # delete program name from arguments

    # path branch:
    if args_count == 1 and args[1].__contains__('/'):
        get_questions(args[1])

    # parameters branch:
    elif args_count == 1:
        # if I want to add another console parameters
        match args[1]:
            case 'new-suit' | 'ns':
                Format.prYellow('Enter file name:')
                user_file_name: str = input(input_sym)
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
    elif args_count == 0:
        get_questions(Path().absolute())  # try search for current directory anyway

    else:
        Format.prRed('No cli arguments passed')
        exit(1)

    # main utility logic:
    question_counter: int = 0
    all_questions_count: Final[int] = len(all_questions)
    while True:
        current_question: str | list[str] = all_questions[question_counter]  # str for old format

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
            choice = input(input_sym)
            match choice:
                case 'pass' | 'p':
                    question_counter += 1
                    if len(all_questions) == question_counter:
                        break
                    continue

                case 'no' | 'n':
                    Format.prRed('Later check this question')
                    questions_to_learn.append(current_question)
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
                    if not questions_to_learn.__contains__(current_question):
                        questions_to_learn.append(current_question)
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
    Format.prYellow(f'learning time - {(finish_time - start_time)}')
    later_todo()
