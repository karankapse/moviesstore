from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})


def reset_password_request(request):
    template_data = {'title': 'Reset Password'}
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['reset_user_id'] = user.id  # Store user ID in session
            return redirect('accounts.reset_password_confirm')
        except User.DoesNotExist:
            template_data['error'] = "Username not found."

    return render(request, 'accounts/reset_password_request.html', {'template_data': template_data})


def reset_password_confirm(request):
    if 'reset_user_id' not in request.session:
        return redirect('accounts.reset_password_request')  # Redirect if session is lost

    template_data = {'title': 'Set New Password'}
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            template_data['error'] = "Passwords do not match."
        else:
            user = User.objects.get(id=request.session['reset_user_id'])
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            del request.session['reset_user_id']  # Remove user ID from session
            return redirect('accounts.login')

    return render(request, 'accounts/reset_password_confirm.html', {'template_data': template_data})