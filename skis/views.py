from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django import forms
from .forms import SkiForm, SettingForm


from .models import User, Ski, Setting


def index(request):
    return render(request, "skis/index.html")

class SkiListView(ListView):
    model = Ski
    template_name = "skis/index.html"
    context_object_name = "skis"

    def get_queryset(self):
       return Ski.objects.all()
 
    def get_context_data(self):
       context = super().get_context_data()
       context['banner'] = 'Ski Fleet'
       return context


class SkiCreateView(CreateView):
    model = Ski
    fields = ('ski_number', 'technique', 'grind','color_tag', 'brand', 'img', 'notes')
    success_url = reverse_lazy('addski')

    def form_valid(self, form):
        form.instance.ski_owner = self.request.user
        return super().form_valid(form)

def addski(request):
    if request.method == "POST":
        form = SkiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("skis/index.html")
        else: 
            msg = "Invalid entry, please try again"
            return (request, "skis/addski.html", {"form": form, "message":msg})
    else:
        form = SkiForm()
        return render(request, "skis/addski.html", {"form": form})

class SettingCreateView(CreateView):
    model = Setting
    fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')
    success_url = reverse_lazy('addskitest')

class SettingListView(ListView):
    model = Setting
    template_name = "skis/setting.html"
    context_object_name = "setting"

    def get_queryset(self):
       return Setting.objects.all()
 
    def get_context_data(self):
       context = super().get_context_data()
       context['banner'] = 'Ski Tests'
       return context

def setting(request):
    return render(request, "skis/setting.html")

def addsetting(request):
    if request.method == "POST":
        form = SettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("skis/index.html")
        else: 
            msg = "Invalid entry, please try again"
            return (request, "skis/addsetting.html", {"form": form, "message":msg})
    else:
        form = SettingForm()
        return render(request, "skis/addsetting.html", {"form": form})


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


def add_skitest(request):
    pass

def skitest(request):
    return render(request, "skis/skitest.html")
