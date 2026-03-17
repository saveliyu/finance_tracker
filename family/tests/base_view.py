from django.test import TestCase, Client

from users.models import CustomUser
from family.models import *


class BaseViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='1234', name='test')

        self.client = Client()
        self.client.login(username='test', password='1234')

        self.family = Family.objects.create(name='Test Family')
        self.member = FamilyMember.objects.create(family=self.family, user=self.user)
