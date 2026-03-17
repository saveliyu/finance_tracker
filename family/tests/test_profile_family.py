from django.urls import reverse
from .base_view import BaseViewTest
from ..models import Family


class ProfileFamilyViewTest(BaseViewTest):

    def test_members_list_view(self):
        url = reverse('family:profile_family')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.family.name)