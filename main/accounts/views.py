from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import LoginForm, RegisterForm, ProfileUserForm, UserPasswordChangeForm
from main.settings import SITE_URL

User = get_user_model()


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    extra_context = {'title': 'Авторизация'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/registration.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('accounts:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = SITE_URL
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: {current_site}{activation_url}',
            None,
            [user.email],
            fail_silently=False,
        )
        return redirect('accounts:email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:email_confirmed')
        else:
            return redirect('accounts:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'accounts/email_confirmation_sent.html'
    extra_context = {'title': 'Письмо активации отправлено'}


class EmailConfirmedView(TemplateView):
    template_name = 'accounts/email_confirmed.html'
    extra_context = {'title': 'Ваш электронный адрес активирован'}


class EmailConfirmationFailedView(TemplateView):
    template_name = 'accounts/email_confirmation_failed.html'
    extra_context = {'title': 'Ваш электронный адрес не активирован'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'accounts/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}