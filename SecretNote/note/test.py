from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Note
class TestCreateNote(TestCase):
    def test_create_note(self):
        get_user_model().objects.create_user(username='test_user', password='strong_password')
        data = {
            'username': 'test_user',
            'password': 'strong_password'
        }
        self.client.post('/accounts/login/', data=data,follow=True) 


        data={
            'title':'unit test note',
            'content':'this is the unit test note for create note correctly test case',
            'max_views':5
        }
        response=self.client.post('/notes/create/',data=data,follow=True)
        self.assertRedirects(response,'/notes/')

        response=self.client.get('/notes/',follow=False)

        recent_note=Note.objects.latest('url_id')
        self.assertIn(recent_note,response.context['notes'])
        

        
