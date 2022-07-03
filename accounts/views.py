# accounts.views
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView

from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignUpForm


class CustomizedLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomizedPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('index')


class CustomizedLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super().get_next_page()
        messages.success(
            self.request,
            'You successfully log out!',
            extra_tags="btn-success"
        )
        return next_page


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(
            self.request,
            "New Account Created!",
            extra_tags="btn-success"
        )
        return super(SignUpView, self).form_valid(form)
