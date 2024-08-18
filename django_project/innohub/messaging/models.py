from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)  # Add this line

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

    @classmethod
    def get_conversation(cls, user1, user2):
        return cls.objects.filter(
            (models.Q(sender=user1) & models.Q(receiver=user2)) |
            (models.Q(sender=user2) & models.Q(receiver=user1))
        ).order_by('timestamp')

    class Meta:
        ordering = ['timestamp']
