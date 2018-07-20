# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client
from django.urls import reverse

# Create your tests here.
# -*- coding: utf-8 -*-


class MarcaModelTest(TestCase):
    '''def test_insert(self):
        response = self.client.get(reverse('marca:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])'''
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='developer123*')

    '''def test_login(self):
        response=self.client.post('/login/', {'username': 'admin', 'password': 'developer123*'})
        self.assertEqual(response.status_code, 200, 'No aceptado')'''

    def test_index(self):
        response = self.client.get(reverse('marca:marca_index'))
        # self.assertEqual(str(response.context['user']), 'developer')
        self.assertEqual(response.status_code, 200)
