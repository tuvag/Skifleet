from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django import forms
from .forms import SkiForm, SettingForm, SkiSearchForm, SettingSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django_filters import BaseRangeFilter, NumberFilter, FilterSet

from .models import User, Ski, Setting, SkiTest

#class NumberRangeFilter(BaseRangeFilter, NumberFilter):
#    pass

def index(request):
    if 'search' in request.GET:
        search = request.GET['search']
        skis = Ski.objects.filter(title_icontains= search)
        return render(request, "skis/index.html", {'skis': skis})
    else:
        skis
        return render(request, "skis/index.html", {'skis': skis})


class SkisFilter(BaseFilter):
    search_fields = {
        'search_ski' : ['ski_number', 'grind', 'brand', 'notes']
    }

class SettingsFilter(BaseFilter):
    #temprature__range = NumberRangeFilter(field_name='temprature', lookup_expr='range')
    search_fields = {
        'search_text' : ['location', 'snow_type', 'notes'],
        'search_temprature' : { 'operator': '__gte', 'fields' : ['temprature'] },
        'search_date' : ['date']
    }

class SkiSearchList(SearchListView):
    # regular django.views.generic.list.ListView configuration
    model = Ski
    paginate_by = 10
    template_name = "skis/index.html"
    context_object_name = "skis"

    # additional configuration for SearchListView
    form_class = SkiSearchForm
    filter_class = SkisFilter

class SettingSearchList(SearchListView):
    # regular django.views.generic.list.ListView configuration
    model = Setting
    paginate_by = 10
    template_name = "skis/setting.html"
    context_object_name = "setting"

    form_class = Setting

    # additional configuration for SearchListView
    form_class = SettingSearchForm
    filter_class = SettingsFilter


class SkiListView(ListView):
    model = Ski
    template_name = "skis/index.html"
    context_object_name = "skis"

    """   def get_queryset(self):
        if len(self.args) > 0:
            return Ski.objects.filter(name__icontains=self.args[0])
        else:
            return Ski.objects.all() """

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = Ski.objects.filter(ski_owner = self.request.user.id)
        return object_list

    """  query = self.request.GET.get('q')
        if query:
            object_list = Ski.objects.filter(name__icontains=query)
        else:
            object_list = Ski.objects.all()
        return object_list """
 
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

class SkiUpdateView(UpdateView):
    model = Ski
    fields = ('ski_number', 'technique', 'grind', 'color_tag', 'brand', 'img', 'notes' )
    success_url = reverse_lazy("index")

class SkiDeleteView(DeleteView):
    model = Ski
    success_url = reverse_lazy("index")

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

    def form_valid(self, form):
        form.instance.tester = self.request.user
        return super().form_valid(form)



class SettingListView(ListView):
    model = Setting
    template_name = "skis/setting.html"
    context_object_name = "setting"

    def get_queryset(self):
       return Setting.objects.filter(tester =self.request.user.id)
 
    def get_context_data(self):
       context = super().get_context_data()
       context['banner'] = 'Ski Tests'
       return context

class SettingUpdateView(UpdateView):
    model = Setting
    fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')
    success_url = reverse_lazy("setting")

class SettingDeleteView(DeleteView):
    model = Setting
    success_url = reverse_lazy("setting")

def ski_details(request, id):
    ski = Ski.objects.get(id= id)
    ski_test = SkiTest.objects.filter(ski=ski)
    details_setting = Setting.objects.filter(skis=ski)
    return render(request,"skis/ski_details.html", {'ski': ski, 'skitest': ski_test, 'setting': details_setting})
    #return render(request,"skis/ski_details.html", {'ski': ski})

def setting_details(request, id):
    setting = Setting.objects.get(id= id)
    return render(request,"skis/setting_details.html", {'setting': setting})

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
