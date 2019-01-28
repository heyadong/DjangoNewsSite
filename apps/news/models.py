from django.db import models

# Create your models here.


class Comments(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey('authdemo.User', on_delete=models.DO_NOTHING)
    article = models.ForeignKey('cms.Article', on_delete=models.DO_NOTHING)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-add_time']