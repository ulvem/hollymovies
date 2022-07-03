from logging import getLogger

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Movie
from .forms import MovieForm, GenreForm

LOGGER = getLogger()


def about_view(request):
    return render(
        request,
        "viewer/about.html",
    )


def index(request):
    return render(request, template_name="base.html")


class MoviesView(ListView):
    template_name = "viewer/movies.html"
    model = Movie


class MovieCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = "customized_form.html"
    success_url = reverse_lazy('movies')
    form_class = MovieForm
    permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data in the movie creation form.', )
        messages.error(self.request,
                       "Invalid data provided",
                       extra_tags="btn-warning")
        return super().form_invalid(form)


class GenreCreateView(LoginRequiredMixin, CreateView):
    template_name = "form.html"
    success_url = reverse_lazy('movies')
    form_class = GenreForm


class MovieUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'customized_form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movies')
    permission_required = "movie.change_movie"

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data in the movie update form.', )
        messages.error(self.request,
                       "Invalid data provided",
                       extra_tags="btn-warning")
        return super().form_invalid(form)


class MovieDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'viewer/delete.html'
    model = Movie
    success_url = reverse_lazy('movies')
    permission_required = "viewer.delete_movie"

    def form_valid(self, form):
        messages.success(self.request,
                         "Movie has been deleted succesfully",
                         extra_tags="btn-success")
        return super(MovieDeleteView, self).form_valid(form)


class MovieDetailView(DetailView):
    template_name = 'viewer/movie_detail.html'
    model = Movie