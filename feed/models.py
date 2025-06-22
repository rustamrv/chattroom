from django.db import models
from accounts.models import Profile

class Post(models.Model):
    name = models.CharField(max_length=60)
    created_date = models.DateTimeField("Date created", auto_now=True,
                                        auto_now_add=False)
    author = models.ForeignKey(Profile, verbose_name="Post author",
                               related_name="posts",
                               on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, verbose_name="Post recipient",
                                  null=True, blank=True,
                                  related_name="received_posts",
                                  on_delete=models.CASCADE)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name
