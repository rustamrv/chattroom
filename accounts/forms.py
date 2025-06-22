from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import send_mail
from .generation import GenerationToken
from .models import Profile
from django.contrib.auth import get_user_model
import redis  
import project.settings as setting

redis_instance = redis.StrictRedis(host=setting.REDIS_HOST,
                                   port=setting.REDIS_PORT, db=0)
# redis_instance = redis.Redis(setting.REDIS_HOST)

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ResetForm(forms.Form):
    email = forms.EmailField()

    def send_email(self, request, recip):
        sender = settings.EMAIL_HOST_USER
        # gen = GenerationToken()
        # token = gen.make_token()
        # request.session[recip] = token
        # try:
        #     user = User.objects.get(email=recip)
        # except User.DoesNotExist:
        #     return False
        # context = {
        #     'user': user.username,
        #     'email': recip,
        #     'protocol': settings.PROTOCOL,
        #     'token': token
        # }
        # template = get_template('reset/password_reset_email.html')
        # html = template.render(context)
        # subject = 'Reset password'
        # email = EmailMessage(subject, html, sender, [recip])
        # email.send() 
        return True


class ResetPassword(forms.Form):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
    )

class DateInput(forms.DateInput):
    input_type = 'date'


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'image',
                  'birthday']
        widgets = {
            'birthday':  DateInput(attrs={'type': 'date'})
        }