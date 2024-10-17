from django.db import models

import custom_user


# Create your models here.

class UserCart(models.Model):
    user = models.OneToOneField(custom_user, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
