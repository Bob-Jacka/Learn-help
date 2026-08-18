"""
Learn help tests
"""
import unittest

try:
    from common_py_lib.testing.Testing import parametrize
except Exception as e:
    print(f'No available modules found: {e}')

from main import parse_question


class Free_functions(unittest.TestCase):
    """
    Functions within any class
    """

    @parametrize(type='Simple', question='Что такое баг?', answer='Различие ожидаемого и фактического поведения')
    def test_should_parse_questions_as_simple(self, type, question, answer):
        var = not self.assertRaises(parse_question(f'Question(type={type}), question={question}, answer={answer}'))

    def test_should_not_parse_questions(self):
        parse_question()
