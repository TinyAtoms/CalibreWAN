from django.db import models
from django.urls import reverse

# Create your models here.


class BookProgress(models.Model):
    user = models.TextField()
    book = models.IntegerField()
    progress = models.TextField()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('tag-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.book) + self.user


    class Meta:
        managed = True
        db_table = 'bookprogress'
        indexes = [
            models.Index(fields=["book"], name="bookprogress_idx"),
        ]

