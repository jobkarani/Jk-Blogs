import unittest
from app.models import Comment


class TestComment(unittest.TestCase):
    """
    Test class to test the behaviour of the Comment class
    """

    def setUp(self):
        """
        Method that will run before every test
        """
        self.new_comment = Comment(
            content="This is a comment")

    def test_instance(self):
        """
        Test to check if the new_comment is an instance of Comment
        """
        self.assertTrue(isinstance(self.new_comment, Comment))