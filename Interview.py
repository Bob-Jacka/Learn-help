from Progon import Progon


class Interview(Progon):
    """
    Interview strategy
    """

    start_words: list[str]
    questions: list[str]
    questions_after_main: list[str]
