from django.contrib import admin

from movie_app.models import UserAccount, Movie

# Register your models here.
@admin.register(UserAccount)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'is_staff',
        'is_active',
        'email',
        'first_name',
        'last_name',
        'username'
    )

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "type",
        "genre",
        "children_max_age",
        "release_year",
        "avatar",
        "rent_price",
        "max_rent_days"
    )
