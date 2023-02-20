from django.db import models

# Create your models here.


class Post(models.Model):
    post_name = models.CharField(max_length=200,blank=False, null=False)
    post_bio = models.CharField(max_length=200, blank=False, null=False)
    post_likes = models.IntegerField(blank=True)
    post_comment = models.IntegerField(blank=True)
    post_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.post_name