from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def create(request):
    if request.method == "POST":
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        else:
            return render(request, "user/create.html", {'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, "user/create.html", {'form': form})
