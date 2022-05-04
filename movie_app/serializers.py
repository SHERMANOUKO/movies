from tkinter.messagebox import RETRY
from movie_app.models import Movie

from rest_framework import serializers

class NestedMovieSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=100)

class RentMovieSerializer(serializers.Serializer):
    
    national_id_number = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=25)
    issue_date = serializers.DateField()
    return_date = serializers.DateField()
    movie = NestedMovieSerializer()

class MovieSerializer(serializers.Serializer):
    GENRE_CHOICES = (
        ("ACTION", 'action'),
        ("DRAMA", 'drama'),
        ("ROMANCE", 'romance'),
        ("COMEDY", 'comedy'),
        ("HORROR", 'horror')
    )
  
    TYPE_CHOICES = (
        ("REGULAR", 'regular'),
        ("CHILDREN", 'children'),
        ("NEW", 'new')
    )

    title = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    genre = serializers.ChoiceField(choices=GENRE_CHOICES)
    children_max_age = serializers.IntegerField(required=False)
    release_year = serializers.IntegerField()
    avatar = serializers.FileField()
    rent_price = serializers.IntegerField()
    max_rent_days = serializers.IntegerField()

    def validate(self, data):
        if data["type"] == "CHILDREN":
            print(99999)
            if not data.get("children_max_age"):
                raise serializers.ValidationError("Children maximum age should be provided for Children movies")
        return data

class ListMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "type",
            "genre",
            "children_max_age",
            "release_year",
            "avatar",
            "rent_price",
            "max_rent_days"
        ]
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
