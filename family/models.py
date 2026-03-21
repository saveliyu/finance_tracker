import secrets

from django.db import models
from django.conf import settings
from django.utils import timezone

from datetime import timedelta
from slugify import slugify




class Family(models.Model):
    name = models.CharField(max_length=100,)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Families"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Family.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



class FamilyMember(models.Model):
    class Status(models.IntegerChoices):
        MEMBER = 0, 'Участник'
        ADMINISTRATOR = 1, 'Админ'
        CREATOR = 2, 'Создатель'



    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='family_member')

    status = models.IntegerField(choices=Status.choices, default=Status.MEMBER)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Family Members"

    def __str__(self):
        return self.user.username




class FamilyInvite(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='invites')
    code = models.CharField(max_length=8, unique=True, blank=True, editable=False)

    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invites')

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Family Invites"

    def __str__(self):
        return self.family.name + '/' + self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_urlsafe(8)[:8]
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=3)
        super().save(*args, **kwargs)

    def is_valid(self):
        if self.expires_at:
            return self.expires_at >= timezone.now()
        return True