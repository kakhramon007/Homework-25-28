from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegisterForm, VideoRegisterForm
from .models import User_detail, Video_model
from django.contrib import messages


def main(request):
    return render(request, 'main.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            User_detail.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email']
            )

            login(request, user)
            messages.success(request, f'Registration successful! Welcome {form.cleaned_data['username']}')

            return redirect('main')
    else:
        form = UserRegisterForm()

    return render(request, 'register_user.html', {'form': form})



