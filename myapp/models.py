from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    USER = (
        ('1', 'admin'),
        ('2', 'user'),
    )
    
    user_type = models.CharField(choices=USER, max_length=50, default=2)

    def __str__(self) -> str:
        return self.username
    

