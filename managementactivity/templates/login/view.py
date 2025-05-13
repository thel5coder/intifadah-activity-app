from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard/')
        else:
            print(form.errors)
            return render(request, 'login/login.html', {'errors': form.errors})
    else:
        form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect('dashboard/')

    return render(request, 'login/login.html', {'form': form})


def logout_view(request):
    print("halo")
    logout(request)
    return redirect("login")
