from django.db import models

class Participant(models.Model):
    uid = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']