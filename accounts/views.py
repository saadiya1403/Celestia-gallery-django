from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'accounts/register.html', { 'form': form})   
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('home')
        else:
            return render(request, 'accounts/register.html', { 'form': form})