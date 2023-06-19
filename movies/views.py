from rest_framework.views import APIView, Request, Response, status
from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.models import Movie, MovieOrder
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
# essas são as permições padrão do rest
from users.permissions import IsEmployeeOrReadOnly, IsUserOwner

from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.pagination import PageNumberPagination



class MoviesView(APIView, PageNumberPagination):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsEmployeeOrReadOnly]

    def get(self, request:Request) -> Response:
        # movies = Movie.objects.all()
        movies = get_list_or_404(Movie)

        movies_per_page = self.paginate_queryset(movies, request)

        serializer = MovieSerializer(instance=movies_per_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request:Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # esse request.user vem da validação do token, pq o user está logado
        serializer.save(user=request.user)
        # é preciso passar ele pos ele faz a ligação do movie o com o seu "dono", ligas as tabelas
        # o campo user na tabela movie esta se recebedno o dict do request.user

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class MoviesByIdView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsEmployeeOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        # movie = Movie.objects.get(id=movie_id)
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(instance=movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(instance=movie,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        # esse save roda a operação do serializer
        serializer.save()



        # FORMA ANTIGA

        # for key, value in serializer.validated_data.items():
        #     setattr(movie, key, value)
        
        # movie.save()

        # serializer = MovieSerializer(data=movie)
        # toda essa logica agora foi para o serializer

        return Response(instance=serializer.data, status=status.HTTP_200_OK)


class MoviesOrdersView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request: Request, movie_id:int) -> MovieOrder:
        movie_obj = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # para a criação da tabela pivo e preciso add as achaves extrangeiras, isso se faz atraves do save
        serializer.save(user=request.user, movie=movie_obj)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)