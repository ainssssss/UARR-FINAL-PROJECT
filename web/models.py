from django.db import models
from api.models import CustomUser

class faq(models.Model):
    question = models.CharField(max_length=100)
    answer= models.CharField(max_length=300)

    def __str__(self):
        return self.question + " -> " + self.answer

class reviews(models.Model):
    username = models.CharField(max_length=100)
    review = models.CharField(max_length=300)

    def __str__(self):
        return self.username + " -> " + self.review