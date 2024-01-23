from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .form import RegisterCustomerForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.username = var.email

            # Use get_or_create to handle potential errors during user creation
            user, created = User.objects.get_or_create(email=var.email, defaults={'username': var.email, 'is_customer': True})
            
            if not created:
                messages.warning(request, 'An account with this email already exists. Please log in.')
                return redirect('login')

            user.is_active = False
            user.save()

            # Email verification setup
            current_site = get_current_site(request)
            subject = 'Innovation Hub Activation Email'
            message = render_to_string('accounts/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {'form': form}
        return render(request, 'accounts/register_customer.html', context)



def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            print(f"Username: {username}, Password: {password}, User: {user}")

            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("Login Successful!")
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Your account is not yet activated. Please check your email for activation instructions.')
                    return redirect('login')
            else:
                messages.warning(request, 'Invalid username or password. Please try again.')
                return redirect('login')
        else:
            #messages.warning(request, 'Something went wrong. Please check form errors.')
            return redirect('login')
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'Active session ended. Log in to continue')
    return redirect('/')

#email verification
def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    #success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')

    #failed
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'accounts/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'accounts/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'accounts/email-verification-failed.html')
# change password - in app
# update profile 