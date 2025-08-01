from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import JSONField  

# Create your models here.

class AnonymousUserToken(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    user_agent = models.TextField(blank=True, null=True)
    token_count = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ip_address',)  # Faqat IP asosida bitta token guruhi
        indexes = [
            models.Index(fields=["ip_address"]),
        ]

    def __str__(self):
        return f"Anon: {self.ip_address} - {self.token_count} ta token"
    
class UserSubjectHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anon_user = models.ForeignKey(AnonymousUserToken, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject or "No Subject"


class UserHistory(models.Model):
    prompt_subject = models.ForeignKey(UserSubjectHistory, on_delete=models.CASCADE, related_name='histories')
    prompt = models.TextField(blank=True, null=True)
    image_url = JSONField(default=list, blank=True, null=True)  # Bir nechta rasm URL larini saqlash uchun
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Prompt: {self.prompt[:50]}..." if self.prompt else "No Prompt"


class ImageGenerationConfig(models.Model):
    max_images = models.PositiveIntegerField(default=4)

    def __str__(self):
        return f"Max images: {self.max_images}"