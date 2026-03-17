from django.urls import reverse
from .base_view import BaseViewTest
from family.models import *


class ProfileFamilyViewTest(BaseViewTest):

    def test_delete_member(self):
        url = reverse('family:delete_member', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:profile_family'))
        self.assertIsNone(FamilyMember.objects.filter(user__pk=self.user.pk).first())

    def test_delete_empty_member(self):
        url = reverse('family:delete_member', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:profile_family'))

