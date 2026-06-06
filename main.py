import datetime
import os.path
import random
import signal
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

questions_to_learn: list[str] = list()  # to do learn
all_questions: list[str] = list()  # all questions that need to answer

# time functionality:
start_time: Final[datetime.datetime] = datetime.datetime.now()
finish_time: datetime.datetime


def get_questions():
    """
    Get questions from file and randomize them
    :return: None
    """
    global learn_filename
    all_dir_files = filter(lambda x: x.__contains__('learn') and not x.__contains__(later_learn_filename), os.listdir())
    all_dir_files = list(all_dir_files)
    all_dir_files_count = len(all_dir_files)
    if all_dir_files_count > 1:
        Format.prYellow('There are more than one file to learn')
        Format.prYellow('Choose one file:')
        for num, valid_file in enumerate(all_dir_files):
            Format.prCyan(f'{num} - {valid_file}')
        while True:
            user_choice = int(input(input_sym))
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
        exit()

    try:
        with open(learn_filename, 'r') as question_file:
            for line in question_file:
                all_questions.append(line.strip())
        if len(all_questions) > 0:
            random.shuffle(all_questions)  # randomize questions before run
            Format.prYellow('All questions are up to date and shuffled')
        else:
            raise Exception('Learn file is empty')
    except Exception as e:
        Format.prRed(f'Some exception occurred during question task - {e}')
        exit(1)


def later_todo():
    """
    Return to user questions that he needs to learn later
    :return:
    """
    if len(questions_to_learn) > 0:
        with open(f'{later_learn_filename}-{datetime.datetime.now()}.txt', 'w+') as todo_file:
            for todo_line in questions_to_learn:
                todo_file.write(todo_line)
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
    Format.prYellow(f'learning time - {finish_time - start_time}')
    later_todo()
    Format.prYellow("Out program")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    get_questions()

    question_counter: int = 0
    all_questions_count: Final[int] = len(all_questions)
    while True:
        current_question: str = all_questions[question_counter]
        if len(current_question) > 0:
            print('\n')
            Format.prCyan(f'{question_counter}/{all_questions_count}: "{current_question}"')
            Format.prGreen('Enter "pass" to pass, "no" for no pass or "save" to save question or "exit"')
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

                case 'save' | 's':
                    Format.prYellow('Save question for later study')
                    questions_to_learn.append(current_question)
                    question_counter += 1

                case 'exit' | 'e':
                    break

                case _:
                    Format.prRed('Wrong value, try again')
        else:
            continue
    finish_time = datetime.datetime.now()
    Format.prYellow(f'learning time - {finish_time - start_time}')
    later_todo()
