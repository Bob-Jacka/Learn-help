"""
AI functionality in utility for manual desktop mode
"""
try:
    # TODO move AI and Data driver into separate local libraries and connect them
    pass
except Exception:
    pass


class AI:
    """
    Class for generating answer to question if it not written
    """

    # TODO
    def __init__(self):
        pass

    def generate_questions(self, question_topic: str) -> list[str] | None:
        """
        Generate questions (more than one) for your question suit
        :param question_topic: which topic to use to generate
        :return: list with questions to proceed
        """
        pass

    def decide_which_suit_questions_use(self, suit_names: list[str]):
        """
        Ask AI about what suit to use (need to declare function in suit to ask)
        :param suit_names:
        :return:
        """
        pass

    def generate_question(self, question_topic: str) -> str | None:
        """
        Generate single question by AI.
        :param question_topic:  which topic to use to generate
        :return: questions string
        """
        pass

    def generate_answer(self, question: str) -> str | None:
        """
        Generate answer with AI (yeah, i know)
        :param question: question to search for
        :return: string value of question
        """
        pass
