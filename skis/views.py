from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django import forms
from .forms import SettingForm, SkiSearchForm, SettingSearchForm, SettingCreationMultiForm, ContactForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django_filters import BaseRangeFilter, NumberFilter, FilterSet
from django.contrib.admin.widgets import AdminDateWidget
from django.core.mail import send_mail, BadHeaderError
#from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from .models import User, Ski, Setting, SkiTest

#class NumberRangeFilter(BaseRangeFilter, NumberFilter):
#    pass


class SettingCreateView(CreateView):
    form_class = SettingCreationMultiForm
    #fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')
    success_url = reverse_lazy('addskitest')
    template_name = "skis/addsetting.html"

    """ def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form """

    def form_valid(self, form):
        setting = form['setting'].save(commit=False)
        setting.tester = self.request.user
        setting.save()
        ski1 = form['ski1'].save(commit=False)
        ski1.setting = setting
        ski1.save()
        ski2 = form['ski2'].save(commit=False)
        ski2.setting = setting
        ski2.save()
        ski3 = form['ski3'].save(commit=False)
        ski3.setting = setting
        ski3.save()
        ski4 = form['ski4'].save(commit=False)
        ski4.setting = setting
        ski4.save()
        ski5 = form['ski5'].save(commit=False)
        ski5.setting = setting
        ski5.save()
        ski6 = form['ski6'].save(commit=False)
        ski6.setting = setting
        ski6.save()
        ski7 = form['ski7'].save(commit=False)
        ski7.setting = setting
        ski7.save()
        ski8 = form['ski8'].save(commit=False)
        ski8.setting = setting
        ski8.save()
        return super().form_valid(form)

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
    #paginate_by = 10
    template_name = "skis/index.html"
    context_object_name = "skis"

    # additional configuration for SearchListView
    form_class = SkiSearchForm
    filter_class = SkisFilter

    def get_queryset(self):
        object_list = Ski.objects.filter(ski_owner = self.request.user.id)
        return object_list

class SettingSearchList(SearchListView):
    # regular django.views.generic.list.ListView configuration
    model = Setting
    #paginate_by = 10
    template_name = "skis/setting.html"
    context_object_name = "setting"

    form_class = Setting

    # additional configuration for SearchListView
    form_class = SettingSearchForm
    filter_class = SettingsFilter

    def get_queryset(self):
        object_list = Setting.objects.filter(tester = self.request.user.id)
        return object_list


def ski_details(request, id):
    ski = Ski.objects.get(id= id)
    ski_test = SkiTest.objects.filter(ski=ski)
    details_setting = Setting.objects.filter(skis=ski)
    return render(request,"skis/ski_details.html", {'ski': ski, 'skitest': ski_test, 'setting': details_setting})
    #return render(request,"skis/ski_details.html", {'ski': ski})

class SkiCreateView(CreateView):
    model = Ski
    fields = ('color_tag','ski_number', 'technique', 'grind', 'brand', 'img', 'notes')
    success_url = reverse_lazy('addski')

    def form_valid(self, form):
        form.instance.ski_owner = self.request.user
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        form.fields['color_tag'].widget = forms.TextInput(attrs={'type': 'color'})
        return form

class SkiUpdateView(UpdateView):
    model = Ski
    fields = ('color_tag', 'ski_number', 'technique', 'grind', 'brand', 'img', 'notes' )
    success_url = reverse_lazy("index")

    def get_form(self):
        form = super().get_form()
        form.fields['color_tag'].widget = forms.TextInput(attrs={'type': 'color'})
        return form

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

class SettingUpdateView(UpdateView):
    model = Setting
    fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')
    success_url = reverse_lazy("setting")

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form

class SettingDeleteView(DeleteView):
    model = Setting
    success_url = reverse_lazy("setting")

def setting_details(request, id):
    setting = Setting.objects.get(id= id)
    ski_test = SkiTest.objects.filter(setting=setting)
    return render(request,"skis/setting_details.html", {'setting': setting, 'skitest':ski_test})

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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry" 
            body = {
			'name': form.cleaned_data['first_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 'webmaster@localhost', ['webmaster@localhost']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()
        return render(request, 'skis/contact.html', {'form':form})

def thanks(request):
    return render(request, 'skis/thanks.html')



