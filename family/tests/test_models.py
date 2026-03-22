from django.test import TestCase
from family.models import *
from users.models import CustomUser


class FamilyMemberTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="", password="")
        self.family = Family.objects.create(name="test")

    def test_member_creation(self):
        member = FamilyMember.objects.create(family=self.family, user=self.user)
        self.assertEqual(member.user, self.user)
        self.assertEqual(member.family, self.family)

        self.assertEqual(self.user.get_family_member, member)

    def test_user_has_family(self):
        FamilyMember.objects.create(family=self.family, user=self.user)

        self.assertIsNotNone(self.user.get_family_object)

    def test_user_has_not_family(self):
        self.assertIsNone(self.user.get_family_object)

    def test_second_family_creation(self):
        FamilyMember.objects.create(family=self.family, user=self.user)
        with self.assertRaises(Exception):
            FamilyMember.objects.create(family=self.family, user=self.user)

    def test_member_has_status(self):
        member = FamilyMember.objects.create(family=self.family, user=self.user)
        self.assertIsNotNone(member.status)

    def test_user_status_change(self):
        member = FamilyMember.objects.create(family=self.family, user=self.user)
        first_status = member.status
        member.status = FamilyMember.Status.ADMINISTRATOR
        member.save()
        self.assertEqual(member.status, FamilyMember.Status.ADMINISTRATOR)
        self.assertNotEqual(first_status, member.status)



class FamilyInviteTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="", password="")
        self.family = Family.objects.create(name="test")

    def test_invite_has_code(self):
        invite = FamilyInvite.objects.create(family=self.family, created_by=self.user)
        self.assertIsNotNone(invite.code)

    def test_invite_has_family(self):
        invite = FamilyInvite.objects.create(family=self.family, created_by=self.user)
        self.assertIsNotNone(invite.family)

    def test_invite_has_author(self):
        invite = FamilyInvite.objects.create(family=self.family, created_by=self.user)
        self.assertIsNotNone(invite.created_by)

    def test_invite_expires_is_valid(self):
        invite = FamilyInvite.objects.create(family=self.family, created_by=self.user)
        delta = invite.expires_at - invite.created_at
        self.assertGreater(delta.days, 0)

    def test_invite_is_valid(self):
        invite = FamilyInvite.objects.create(family=self.family, created_by=self.user)
        self.assertTrue(invite.is_valid())

    def test_second_invite_creation(self):
        FamilyInvite.objects.create(family=self.family, created_by=self.user)
        with self.assertRaises(Exception):
            FamilyInvite.objects.create(family=self.family, created_by=self.user)


class FamilyTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="", password="")

    def test_family_creation(self):
        family = Family.objects.create(name="test")
        self.assertEqual(family.name, "test")

    def test_family_has_slug(self):
        family = Family.objects.create(name="test")
        self.assertEqual(family.slug, "test")

    def test_family_has_member(self):
        family = Family.objects.create(name="test")
        FamilyMember.objects.create(family=family, user=self.user)
        self.assertEqual(family.members.count(), 1)
