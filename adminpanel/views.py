from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.contrib import auth,messages
from django.contrib.auth.models import User

from core.models import *

# Create your views here.


def index(request):
    template = loader.get_template('admin/dashboard.html')
    context = {
        'unreadmessages' : len(ContactUs.objects.filter(isRead=False))
    }
    return HttpResponse(template.render(context,request))

class Gather(generic.View):
    template = loader.get_template('admin/gather.html')
    def get(self, *args, **kwargs ):
        context = {
            'unreadmessages' : len(ContactUs.objects.filter(isRead=False))
        }
        return HttpResponse(self.template.render(context,self.request))

class Result(generic.View):
    template = loader.get_template('admin/result.html')
    def get(self,*args,**kwargs) :
        context = {
            'unreadmessages' : len(ContactUs.objects.filter(isRead=False)),
            'categories' : Category.objects.all(),
        }
        return HttpResponse(self.template.render(context,self.request))

class Contact(generic.View):
    template = loader.get_template('admin/contact.html')
    def get(self,*args,**kwargs):
        page = kwargs['page']
        messages = ContactUs.objects.all()
        unit = 15
        total = len(messages)
        pageCount = total / unit 
        if total % unit > 0 :
            pageCount = pageCount+1
        context = {
            'messages' : messages,
            'page' : page,
            'pagecount' : pageCount,
            'unreadmessages' : len(ContactUs.objects.filter(isRead=False))
        }
        return HttpResponse(self.template.render(context,self.request))

class TemplateSetting(generic.View):
    template = loader.get_template('admin/templatesetting.html')
    def get(self,*args,**kwargs):
        context = {
            'unreadmessages' : len(ContactUs.objects.filter(isRead=False))
        }
        return HttpResponse(self.template.render(context,self.request))