import pytest
from django.contrib.auth.models import User
from rest_framework import status
from .models import Post
from rest_framework.test import APIClient

@pytest.fixture
def test_user():
    """ Testlew ushin paydalaniwshi (user) jaratatugun fixture. """
    return User.objects.create_user(username='pytestuser', password='pytestpassword')


@pytest.fixture
def test_post(test_user):
    """ Test ushin post jaratatugin fixture (test_user fixture in ebaylanisli) """
    return Post.objects.create(
        author = test_user,
        title = 'Pytest Test Atamasi',
        content = 'Pytest Test Mazmuni'
    )


# Testlerdin APITestCase den miyras aliwi shart emes
# @pytest.mark.django_db  dekaratori test ushin bazani aktivlestiredi

@pytest.mark.django_db
def test_list_posts(client, test_post):
    """ Postlar dizimi duris qaytip atirganin tekseriw """
    client = APIClient()
    response = client.get('/api/v1/posts/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'Pytest Test Atamasi'


@pytest.mark.django_db
def test_create_post_auth(client, test_user):
    """ Sistemaga kirgen paydalaniwshi post jarata aliwin tekseriw """
    client = APIClient()
    client.force_authenticate(user=test_user)

    data = {
        'title': 'Pytest Jana Post',
        'content': 'Pytest Jana Post'
    }
    response = client.post('/api/v1/posts/', data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1    # Tek usi post ushin baza bos boladi
    assert Post.objects.first().title == 'Pytest Jana Post'






