
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post
from rest_framework.test import APIClient

class PostApiTests(APITestCase):
    def setUp(self):
        """
        Har bir test metodi iske tuspesden aldin orinlanatugin tayarliq jumislari.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test atamasi',
            content = 'Test mazmuni'
        )

    
    #   --- Model testi ---
    def test_model_str_representation(self):
        """ Modeldin standart __str__ metodi duris islep atirganin tekseriw. """
        self.assertEqual(str(self.post), 'Test atamasi')

    
    #   --- API Endpoint Testleri ---
    def test_list_posts_unauthenticated(self):
        """ Authentication nan otpegen paydalaniwshi ushin postlar dizimiz tekseriw """
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test atamasi')
        

    def test_create_post_authenticated(self):
        """ Authentication nan otken paydalaniwshi jana post jarata aliwin tekseriw """
        # Testlew ushin user di sistemaga kirgizemiz
        
        self.client.force_authenticate(user=self.user)
        
        data = {'title': 'Jana post', 'content': 'Jana mazmun'}
        response = self.client.post('/api/v1/posts/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.first().title, 'Jana post')


    def test_create_post_unauthenticated(self):
        """ Authentication nan otpegen paydalaniwshi post jarata almawin tekseredi """
        # Bul sapari testlew ushin userdi sistemaga kirgizbeymiz

        data = {'title': 'Ruqsatsiz post', 'content': 'Ruqsatsiz mazmun'}
        response = self.client.post('/api/v1/posts/', data)

        # IsAuthenticateOrReadOnly ruqsatina muwapiq, 401 UnAuthorized ornina 403 Forbidden boliwi mumkin
        # JWT qollanganda, token joq bolsa 401 Unauthorized boladi
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        

    def test_update_post_by_author(self):
        """ Postdin authori sol postti ozgerte aliwin tekseriw """

        self.client.force_authenticate(user=self.user)

        update_data = {'title': 'Janalangan atama', 'content': 'Janalangan mazmun'}
        response = self.client.put(f'/api/v1/posts/{self.post.id}/', update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()     # post obyetin bazadan janalap alamiz. bolmasa aldingi data meene post obyekti turaberedi
        self.assertEqual(self.post.title, 'Janalangan atama')


    def test_update_post_by_another_user(self):
        """ Basqa user postti ozgerte almawin tekseriw (ozine tiyisli bolmagan postti) (IsAuthorOrReadOnly  permissioni arqali) """
        another_user = User.objects.create_user(
            username='anotheruser',
            password='anotherpassword'
        )
        # another_user atinan sistemaga kirip aldiq
        self.client.force_authenticate(user=another_user)

        update_data = {'title': 'Urlaniwshi atama'}
        response = self.client.put(f'/api/v1/posts/{self.post.id}/', update_data)
        print("qaytqan koddi korset: ", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





