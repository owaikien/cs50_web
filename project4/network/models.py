from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Post class
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.timestamp.strftime('%d %b %Y %H:%M:%S')}"
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

class Profile(models.Model):
    # using OnetoOneField to make sure that each user can have exactly only one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

