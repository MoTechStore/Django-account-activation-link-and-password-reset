from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode


from authentication.forms import UserRegistrationForm

def register(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            current_site =get_current_site(request)
            mail_subject = "Activate your account"
            
            message = render_to_string('authentication/email_activation/activate_email_message.html',{
            'user': form.cleaned_data['username'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            })
            
            to_mail = form.cleaned_data['email']
            mail = EmailMessage(
                mail_subject, message, to=[to_mail]
                )
            mail.send()
            
            messages.success(request, 'Account created successfully')
            return redirect('/') # redirect a user to a login page
        else:
            messages.error(request, 'Account failed try again')
    
    return render(request, 'authentication/register.html', {'form':form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/email_activation/activation_successful.html')
    else:
        return render(request, 'authentication/email_activation/activation_unsuccessful.html')


@login_required
def homepage(request):
    return render(request, 'homepage.html')