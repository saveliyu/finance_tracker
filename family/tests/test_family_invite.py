from django.urls import reverse
from django.contrib.messages import get_messages

from .base_view import BaseViewTest
from family.models import *


class InviteViewTest(BaseViewTest):

    def test_invite_creation(self):
        self.client.force_login(self.user)
        url = reverse('family:create_invite')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:invite'))

        self.assertTrue(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_creation_without_login(self):
        self.client.logout()
        FamilyInvite.objects.all().delete()
        url = reverse('family:create_invite')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse('users:login', )}?next=/family/create_invite/')
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_creation_with_existing_invite(self):
        code = FamilyInvite.objects.create(created_by=self.user, family=self.family).code
        url = reverse('family:create_invite')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:invite'))
        self.assertEqual(code, FamilyInvite.objects.filter(created_by=self.user).last().code)

    def test_invite_deletion(self):
        self.client.force_login(self.user)
        FamilyInvite.objects.create(created_by=self.user, family=self.family)
        url = reverse('family:delete_invite')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('family:create_invite'))
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_empty_invite_deletion(self):
        self.client.force_login(self.user)
        url = reverse('family:delete_invite')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('family:create_invite'))
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_deletion_without_login(self):
        self.client.logout()
        FamilyInvite.objects.create(created_by=self.user, family=self.family)

        url = reverse('family:delete_invite')
        response = self.client.get(url)

        self.assertRedirects(response, f'{reverse('users:login', )}?next=/family/delete_invite/')
        self.assertTrue(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_view(self):
        code = FamilyInvite.objects.create(created_by=self.user, family=self.family).code

        self.client.force_login(self.user)
        url = reverse('family:invite')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, code)

    def test_invite_view_without_login(self):

        self.client.logout()
        url = reverse('family:invite')
        response = self.client.get(url)

        self.assertRedirects(response, f'{reverse('users:login', )}?next=/family/invite/')

    def test_empty_invite_view(self):
        FamilyInvite.objects.all().delete()
        self.client.force_login(self.user)
        url = reverse('family:invite')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('family:create_invite'))
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_enter_invite_get(self):
        self.client.force_login(self.user)
        url = reverse('family:enter_invite')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family/enter_invite.html')
        self.assertIn('form', response.context)

    def test_enter_invite_post_valid(self):
        self.client.force_login(self.user)

        invite = FamilyInvite.objects.create(
            created_by=self.user,
            family=self.family
        )

        url = reverse('family:enter_invite')
        response = self.client.post(url, {
            'code': invite.code
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('family:login_by_invite', kwargs={'code': invite.code})
        )

    def test_enter_invite_post_invalid(self):
        self.client.force_login(self.user)
        url = reverse('family:enter_invite')

        response = self.client.post(url, {
            'code': ''  # пустой код
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family/enter_invite.html')
        form = response.context['form']
        self.assertFormError(form, 'code', 'Обязательное поле.')

    def test_enter_invite_without_login(self):
        self.client.logout()
        url = reverse('family:enter_invite')

        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next=/family/enter_invite/"
        )

    def test_invalid_code(self):
        self.client.force_login(self.user)

        url = reverse('family:login_by_invite', kwargs={'code': 'wrongcode'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:enter_invite'))

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), 'Неверный код')

    def test_already_in_same_family(self):
        self.client.force_login(self.user)

        invite = FamilyInvite.objects.create(
            created_by=self.user,
            family=self.family
        )


        url = reverse('family:login_by_invite', kwargs={'code': invite.code})
        response = self.client.get(url)

        self.assertRedirects(response, reverse('family:enter_invite'))

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), 'Вы уже состоите в этой семье')

    def test_already_in_other_family(self):
        self.client.force_login(self.user)

        FamilyMember.objects.filter(user=self.user).delete()
        other_family = Family.objects.create(name='Other', slug='other')

        invite = FamilyInvite.objects.create(
            created_by=self.user,
            family=self.family
        )

        FamilyMember.objects.create(
            family=other_family,
            user=self.user,
            status=0
        )

        url = reverse('family:login_by_invite', kwargs={'code': invite.code})
        response = self.client.get(url)

        self.assertRedirects(response, reverse('family:enter_invite'))

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), 'Вы уже состоите в другой семье')

    def test_success_join_family(self):
        self.client.force_login(self.user)

        FamilyMember.objects.filter(user=self.user).delete()

        invite = FamilyInvite.objects.create(
            created_by=self.user,
            family=self.family
        )

        url = reverse('family:login_by_invite', kwargs={'code': invite.code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:profile_family'))

        self.assertTrue(
            FamilyMember.objects.filter(
                family=self.family,
                user=self.user
            ).exists()
        )

        self.assertFalse(
            FamilyInvite.objects.filter(code=invite.code).exists()
        )