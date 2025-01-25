from django.db import models
from django.contrib.auth.models import User
from shared.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.upload_handers import profile_pictureupload_to


class VerificationCode(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_verification_code_set"
    )
    code = models.CharField(max_length=6, unique=True)
    otp_used = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Verification Codes"
        ordering = ["-created_at"]
        unique_together = ["user", "code"]


class UserProfile(BaseModel):
    # def document_upload_to(instance, doctype, contain_name, filename):
    # def document_upload_to(instance, doctype, contain_name, filename):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_set"
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=profile_pictureupload_to,
        null=True,
        blank=True,
    )
    state = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
