from django.shortcuts import render
from django.views.generic import ListView, FormView

from viewer.models import Movie
from viewer.templates.forms import MovieForm


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
