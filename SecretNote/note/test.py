from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from .models import Note
from unittest.mock import patch

class TestCreateNote(TestCase):
    def test_create_note(self):
        self.client = Client(REMOTE_ADDR='192.127.0.1')
        get_user_model().objects.create_user(username='test_user', password='strong_password')
        data = {
            'username': 'test_user',
            'password': 'strong_password'
        }
        self.client.post('/accounts/login/', data=data,follow=True) 


        data={
            'title':'unit test note',
            'content':'this is the unit test note for create note correctly test case',
            'expiration':timezone.now() + timezone.timedelta(hours=1),
            'max_views':5
        }
        response=self.client.post('/notes/create/',data=data,follow=True)
        self.assertRedirects(response,'/notes/')

        response=self.client.get('/notes/',follow=False)

        recent_note=Note.objects.latest('url_id')
        self.assertIn(recent_note,response.context['notes'])


    def test_note_max_views(self):
        self.client = Client(REMOTE_ADDR='192.168.0.1')
        get_user_model().objects.create_user(username='test_user', password='strong_password')
        data = {
            'username': 'test_user',
            'password': 'strong_password'
        }
        self.client.post('/accounts/login/', data=data,follow=True) 


        data={
            'title':'unit test note [max_views]',
            'content':'this is the unit test note for create note deleted in maxviews is reached',
            'max_views':3,
            'expiration':timezone.now() + timezone.timedelta(hours=1),
        }
        self.client.post('/notes/create/',data=data,follow=True)

        recent_note=Note.objects.latest('url_id')
        for _ in range(4):
            self.client.get(reverse('view_note', args=[recent_note.url_id]),follow=False)

        response=self.client.get('/notes/',follow=False)
        self.assertNotIn(recent_note,response.context['notes'])

    def test_note_expiration(self):
        self.client = Client(REMOTE_ADDR='192.168.0.1')

        get_user_model().objects.create_user(username='test_user', password='strong_password')
        data = {
            'username': 'test_user',
            'password': 'strong_password'
        }
        self.client.post('/accounts/login/', data=data,follow=True) 

        data={
            'title':'unit test note [expiration]',
            'content':'this is the unit test note for create note deleted if expiration date is reached',
            'max_views':50,
            'expiration':timezone.now() - timezone.timedelta(hours=5)
        }
        
        response=self.client.post('/notes/create/',data=data,follow=True)

        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('expiration', response.context['form'].errors)

        

