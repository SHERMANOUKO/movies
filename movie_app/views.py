from movie_app.authentication import token_generator, expired_token_handler, expires_in
from movie_app.models import UserAccount, TokenModel, Movie, RentMovie
from movie_app.serializers import LoginSerializer, MovieSerializer, ListMovieSerializer, \
                                    RentMovieSerializer, ListRentMovieSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

class MovieViewset(viewsets.ViewSet):
    # permission_classes = []

    def list(self, request):

        queryset = Movie.objects.all()
        movie_serializer = ListMovieSerializer(queryset, many=True)
        
        if not movie_serializer.data:
            return Response(
                {'details':'No movie added to database yet.', 'code':400},
                status=status.HTTP_200_OK
            )
        return Response(
            {'details':movie_serializer.data, 'code':200},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        
        movie_serializer = MovieSerializer(data=request.data)

        if not movie_serializer.is_valid():
            return Response(
                {'details':movie_serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        
        validated_data = movie_serializer.validated_data
        Movie.objects.create(
            title = validated_data.get("title"),
            type = validated_data.get("type"),
            genre = validated_data.get("genre"),
            release_year = validated_data.get("release_year"),
            avatar = validated_data.get("avatar"),
            rent_price = validated_data.get("rent_price"),
            max_rent_days = validated_data.get("max_rent_days")
        )

        return Response(
            {'details':'Movie succesfully created', 'code':200},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):

        Movie.objects.filter(id=pk).delete()

        return Response(
            {'details':'Movie succesfully deleted', 'code':200},
            status=status.HTTP_200_OK
        )

class RentedMovieViewset(viewsets.ViewSet):
    permission_classes = []

    def list(self, request):

        queryset = RentMovie.objects.select_related('movie_id').all()
        
        rented_movies = []

        for movie in queryset:
            rented_movies.append({
                'id': movie.id,
                'title': movie.movie_id.title,
                'national_id_number': movie.national_id_number,
                'phone_number': movie.phone_number,
                'issue_date': movie.issue_date,
                'return_date': movie.return_date,
                'returned': movie.returned
            })
        
        rented_movie_serializer = ListRentMovieSerializer(rented_movies, many=True)
        
        if not rented_movie_serializer:
            return Response(
                {'details':'No rented movies available.', 'code':400},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'details':rented_movie_serializer.data, 'code':200},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        
        rented_movie_serializer = RentMovieSerializer(data=request.data)

        if not rented_movie_serializer.is_valid():
            return Response(
                {'details':rented_movie_serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        validated_data = rented_movie_serializer.validated_data

        try:
            movie = Movie.objects.get(id=validated_data.get("movie_id"))
        except TokenModel.DoesNotExist:
            return Response(
                {'details':"The selected movie does not exist in database", 'code':404},
                status=status.HTTP_404_NOT_FOUND
            )

        RentMovie.objects.create(
            movie_id = movie,
            national_id_number = validated_data.get("national_id_number"),
            phone_number = validated_data.get("phone_number"),
            issue_date = validated_data.get("issue_date"),
            return_date = validated_data.get("return_date"),
            returned = validated_data.get("returned")
        )

        return Response(
            {'details':'Movie succesfully created', 'code':200},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):

        Movie.objects.filter(id=pk).delete()

        return Response(
            {'details':'Movie succesfully deleted', 'code':200},
            status=status.HTTP_200_OK
        )

class SessionViewset(viewsets.ViewSet):    

    @action(methods=['POST'], detail=False, permission_classes=[])
    def login(self, request):
        """login a user"""

        login_serializer = LoginSerializer(data=request.data)

        if not login_serializer.is_valid():
            return Response(
                {'details':login_serializer.errors, 'code': 400}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = UserAccount.objects.filter(
            username=login_serializer.data['username'],
            password=login_serializer.data['password'],
            is_active=True
        )
        
        if not user:
            return Response(
                {'details':'Invalid Credentials', 'code':401},
                status=status.HTTP_200_OK
            )

        try:
            token = TokenModel.objects.get(user=user[0])
        except TokenModel.DoesNotExist:
            token = token_generator(user[0])

        is_expired, token = expired_token_handler(token)

        if is_expired:
            token = token_generator(user[0])
        
        return Response({
            'expires_in': expires_in(token),
            'token': token.token,
            'code': 200
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, )
    def logout(self, request):
        """delete a token"""

        token = request.query_params.get('token')
        TokenModel.objects.filter(token=token).delete()

        return Response({
            'code': 200
        }, status=status.HTTP_200_OK)
