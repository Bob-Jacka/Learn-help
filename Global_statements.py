import datetime
from typing import Final


class Global_statement:
    """
    Some constants and global data in one class
    """
    # containers
    questions_to_later_learn: Final[list[str]] = list()  # to do learn
    all_file_data: Final[dict[str, str]] = dict()  # available global paths and variables

    # time functionality:
    start_time: datetime.datetime = datetime.datetime.now()
    finish_time: datetime.datetime

    # consts:
    later_learn_filename: Final[str] = 'todo-learn'
    main_file_name: Final[str] = '__main__' # control file in suit with imports
    all_file_name: Final[str] = '__all__' # almost deprecated file for global dependencies
    global_dir_name: Final[str] = '__global__' # directory with global dependencies
    statistics_file_name: Final[str] = '__stat__'  # file where stored statistics
    app_version: Final[str] = '4.0.0'
