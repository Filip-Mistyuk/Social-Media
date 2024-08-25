from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.user.username
    

class Follow(models.Model):
    from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} follows {self.to_user.username}"
        
class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='following_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follower_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'