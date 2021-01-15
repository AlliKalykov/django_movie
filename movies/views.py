from django.db import models
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewsCreateSerializer,
    RatingCreateSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """
    Вывод списка фильмов
    """
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """ Вывод фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """
    Добавление отзыва к фильму
    """
    serializer_class = ReviewsCreateSerializer


class RatingAddStarView(generics.CreateAPIView):
    """
    Поставить оценку (звезду) к фильму
    """
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """
    Вывод списка актеров
    """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """
    Вывод списка актеров
    """
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
