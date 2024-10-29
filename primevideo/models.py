from django.db import models
from django.contrib.auth.models import User

class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)

    class Meta:
        abstract = True

class Movie(BaseContent):
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return f"Movie: {self.title}"

class Series(BaseContent):
    seasons = models.IntegerField()
    episodes = models.IntegerField()

    def __str__(self):
        return f"Series: {self.title}"