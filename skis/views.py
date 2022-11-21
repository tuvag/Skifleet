from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView


from .models import User, Ski


def index(request):
    return render(request, "skis/index.html")

class SkiListView(ListView):
    model = Ski
    template_name = "ski/index.html"
    context_object_name = "skis"

    def get_queryset(self):
       return Ski.objects.all()
 
    def get_context_data(self):
       context = super().get_context_data()
       context['banner'] = 'Ski Fleet'
       return context


class SkiCreateView(CreateView):
    model = Ski
    fields = ('ski_number', 'technique', 'grind', 'brand', 'img', 'notes')
    success_url = reverse_lazy('index')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "skis/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "skis/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "skis/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "skis/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "skis/register.html")


def contact(request):
    return render(request, "skis/contact.html")

def addski(request):
    return render(request, "skis/addski.html")

def add_skitest(request):
    pass

def skitest(request):
    return render(request, "skis/skitest.html")
