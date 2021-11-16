import unittest
from app.models import BlogPost


class TestPost(unittest.TestCase):
    def setUp(self):
        """
        Method that will run before every test
        """
        self.new_blog = BlogPost(
            user_id=1,
            title="Test Title",
            post="Test Post",
            date="12-4-2020"
        )

    def test_instance(self):
        """
        Test to check if the post object is an instance of the Post class
        """
        self.assertTrue(isinstance(self.new_blog, BlogPost))

    def test_save_blog(self):
        """
        Test to save a post
        """
        self.new_blog.save_blog()
        self.assertTrue(len(BlogPost.query.all()) > 0)

    def test_get_blog_by_id(self):
        """
        Test to check if the get post by id method is working
        """
        self.new_blog.save_blog()
        got_blog = BlogPost.get_blog(1)
        self.assertTrue(got_blog is not None)