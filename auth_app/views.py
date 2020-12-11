from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
from dashboard.models import Group
from doc_managment.settings import MAIN_PAGE


def signup_view(request):
    uuid = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)

            login(request, user)
            uuid = request.GET.get("uuid")
            if uuid:
                try:
                    group = Group.objects.get(group_uuid=uuid)
                except:
                    group = None
                if group is not None:
                    user.profile.groups.add(group)
                    user.save()
            return redirect(MAIN_PAGE)
    else:
        param = request.GET.get("uuid")
        uuid = ("?uuid=" + param) if param else ""
        if not request.user.is_authenticated:
            form = UserCreationForm()
        else:
            group = Group.objects.filter(group_uuid=param).first()
            request.user.profile.groups.add(group)
            return redirect(MAIN_PAGE)

    return render(request, 'auth/signup.html', {'form': form, "uuid": uuid})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard:documents")
            else:
                return redirect('auth_app:login')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html')
