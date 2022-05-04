from rest_framework import routers
from movie_app import views

router = routers.DefaultRouter()
router.register('session', views.SessionViewset, basename='session')
router.register('movies', views.MovieViewset, basename='movies')
# router.register('products', views.ProductsViewset, basename='products')
