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
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
 
class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def send_email(self, request, recip):
        sender = settings.EMAIL_HOST_USER
        gen = GenerationToken()
        token = gen.make_token()  
        redis_instance.set(recip, token)  
        send_mail(
            'Register',
            'Hi, your token ' + token,
            sender,
            [recip],
            fail_silently=False,
            )  

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

class SuccessTokenForm(forms.Form):
    token = forms.CharField(max_length=200) 


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