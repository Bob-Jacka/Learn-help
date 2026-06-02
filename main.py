import os.path
import random
from typing import Final

input_sym: Final[str] = '>> '
learn_filename: Final[str] = os.path.curdir + os.path.sep + 'learn.txt'  # file with questions
later_learn_filename: Final[str] = 'todo-learn.txt'

questions_to_learn: list[str] = list()  # to do learn
all_questions: list[str] = list()


def get_questions():
    """
    Get questions from file and randomize them
    :return: None
    """
    try:
        with open(learn_filename, 'r') as question_file:
            for line in question_file:
                all_questions.append(line.strip())
        if len(all_questions) > 0:
            random.shuffle(all_questions)  # randomize questions
            print('All questions are up to date and shuffled')
        else:
            raise Exception('Learn file is empty')
    except Exception as e:
        print(f'Some exception occurred during question task - {e}')
        exit(1)


def later_todo():
    if len(questions_to_learn) > 0:
        print('Here are question to learn:')
        with open(later_learn_filename, 'w+') as todo_file:
            for todo_line in questions_to_learn:
                todo_file.write(todo_line)
                todo_file.write('\n')
    else:
        print('No to do questions')


def add_to_todo(question_todo: str):
    questions_to_learn.append(question_todo)


if __name__ == '__main__':
    get_questions()

    question_counter: int = 0
    while True:
        print('\n')
        current_question: str = all_questions[question_counter]
        print(current_question)
        print('Enter "pass" (p) to pass, "no" (n) for no pass or "save" to save question or "exit"')
        choice = input(input_sym)
        match choice:
            case 'pass' | 'p':
                question_counter += 1
                continue
            case 'no' | 'n':
                print('Later check this question')
                questions_to_learn.append(current_question)
                question_counter += 1
            case 'save':
                print('Save question for later study')
                questions_to_learn.append(current_question)
                question_counter += 1
            case 'exit':
                break
            case _:
                print('Wrong value, try again')

    later_todo()
