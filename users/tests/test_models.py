from django.test import TestCase

from family.models import *
from users.models import CustomUser

class TestCustomUser(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testusername", name="testuser",
                                                    color='#7542f5', password='1234')
        self.family = Family.objects.create(name='testfamily')

    def test_str(self):
        self.assertEqual(self.user.__str__(), "testusername")

    def test_name(self):
        self.assertEqual(self.user.name, "testuser")

    def test_color(self):
        self.assertEqual(self.user.color, "#7542f5")

    def test_get_empty_family_member(self):
        self.assertIsNone(self.user.get_family_member)

    def test_get_family_member(self):
        FamilyMember.objects.create(user=self.user, family=self.family)
        family_member = FamilyMember.objects.get(user=self.user, family=self.family)
        self.assertEqual(self.user.get_family_member, family_member)

    def test_get_family_members(self):
        user2 = CustomUser.objects.create_user(username="testusername2", name="testuser2",
                                                color='#42f5c8', password='1234')
        FamilyMember.objects.create(user=self.user, family=self.family)
        FamilyMember.objects.create(user=user2, family=self.family)
        family_members = FamilyMember.objects.filter(family=self.family)
        self.assertQuerySetEqual(list(self.user.get_family_members), list(family_members))

    def test_get_empty_family_members(self):
        self.assertEqual(self.user.get_family_members.count(), 0)

    def test_get_empty_family_object(self):
        self.assertIsNone(self.user.get_family_object)

    def test_get_family_object(self):
        FamilyMember.objects.create(user=self.user, family=self.family)
        self.assertEqual(self.user.get_family_object, self.family)

class TestSuperUser(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="testusername", name="testuser", color='#7542f5', password='1234')

    def test_roots(self):
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)