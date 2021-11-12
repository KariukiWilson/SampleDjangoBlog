# Notice that we are using Class-Based Views
# So, we shall use Testcase

# Notes on Test Code
# Importing the get_user_model to reference our active user.
# Importing Client() which is used as a dummy webBrowser for stimulating 
# GET and POST requests on a URL.
# In other words, whenever you are testing views, you should use Client().
# In our set up method, we add a sample blog post to test and then confirm 
# that both its string representation and content are correct.

# The we use test_post_list_view to confirm that our homepage returns a 200 HTTP
# status code, contains our body text, and uses the correct home.html template.
# Finally test_post_detail_view tests that our detail page works as expected 
# and that an incorrect page returns a 404. 

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post

# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret',
        )

        self.post = Post.objects.create(
            title = 'A good title',
            content= 'A good well-written content',
            author = self.user,
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.content}', 'Nice content')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')