from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from movie_app.managers import CustomUserManager
# Create your models here.

# UserAccount and Token models would traditionally live in a 
# user app. For this simple demo, we let them live here
class UserAccount(AbstractUser):
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True,max_length=255,null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class TokenModel(models.Model):
    token = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

class Movie(models.Model):

    def _image_file_name(instance, filename):
        filename = filename.replace(' ', '-')
        filename = f"{instance.genre}/{instance.type}/{filename}"
        return filename

    REGULAR = "REGULAR"
    CHILDREN = "CHILDREN"
    NEW = "NEW"
  
    TYPE_CHOICES = (
        (REGULAR, 'regular'),
        (CHILDREN, 'children'),
        (NEW, 'new')
    )

    ACTION = "ACTION"
    DRAMA = "DRAMA"
    ROMANCE = "ROMANCE"
    COMEDY = "COMEDY"
    HORROR = "HORROR"

    GENRE_CHOICES = (
        (ACTION, 'action'),
        (DRAMA, 'drama'),
        (ROMANCE, 'romance'),
        (COMEDY, 'comedy'),
        (HORROR, 'horror')
    )

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    children_max_age = models.IntegerField(null=True)
    release_year = models.IntegerField()
    avatar = models.ImageField(upload_to=_image_file_name)
    rent_price = models.IntegerField() # flat rate for renting per day
    max_rent_days = models.IntegerField() # max days you can rent a copy of this movie

class RentMovie(models.Model):

    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    national_id_number = models.BigIntegerField()
    phone_number = models.CharField(max_length=25)
    issue_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False)
