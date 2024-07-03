from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="posted_by")
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    edited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post: {self.id} by {self.user} on {self.date}"

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="liked_by")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=False, related_name="liked")

    def __str__(self):
        return f"{self.user} likes {self.post}"

class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="user")
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="following")

    def __str__(self):
        return f"{self.user} follows {self.following}"
    
