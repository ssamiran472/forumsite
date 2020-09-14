from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib
import json
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
from django.conf import settings

# Custom modules
from .scrape import GetCategory, GetAnsweredLink, ToSlug, TempAction
from .models import Category, Forum, Article, TranslatedArticle, Language, ContactUs, ContactUsForm
#from .translate import TranslateArticle
from .utils import GetCurrentLanguageCode

# Create your views here.

def GetLatestPosts():
    displayNum = 10
    ret = TranslatedArticle.objects.filter().order_by('-id')[:displayNum]
    ret_in_ascending_order = reversed(ret)
    return ret
#############################################

def index(request):
    """
    categories = ['HARDWARE','SOFTWARE','NETWORKING']
    for category in categories:
        cat = Category()
        cat.name = category
        cat.save()
    parent = Category.objects.get(name='NETWORKING')
    forums = ['Networking','Wireless Networking','Wireless Carriers','Distributed Computing']
    forums = ['Windows 10','Windows Legacy',"Windows 7","Windows Vista","Windows XP"]
    forums = ['CPUs','Cooling','Components','Overclocking','Motherboards','Memory','Power Supplies']
    for forum in forums :
        parent.forum_set.create(name=forum)
    print(parent.forum_set.all())
    for category in Category.objects.all():
        category.slug = ToSlug(category.name)
        category.save()
    for model in Forum.objects.all():
        model.slug = ToSlug(model.name)
        model.save()
    """
#    for cur in Forum.objects.all():
#        for page in range(1,5):
#            print( str(cur.id) + ' ' + str(page) )
#            GetAnsweredLink(cur,page)

    template = loader.get_template('index.html')
    curLangCode = GetCurrentLanguageCode(request)
    context = {
        'nav':'Home',
        'currentLangCode':curLangCode.capitalize(),
        'language':Language.objects.all(),
        'categories':Category.objects.all(),
        'latestposts':GetLatestPosts(),
        'form':ContactUsForm(),
    }
    return HttpResponse(template.render(context, request))

class Scrape(generic.View):
    template = loader.get_template('scrape.html')
    context = {
        'language':Language.objects.all(),
        'nav':'Scrape'
    }
    def get(self,*args,**kwargs):
        return HttpResponse(self.template.render(self.context, self.request))

class ForumView(generic.View):
    template = loader.get_template('forum.html')
    def get(self,*args,**kwargs):
        langcode = GetCurrentLanguageCode(self.request)
        lang = Language.objects.get(langcode=langcode)
        page = kwargs['page']
        curForum = Forum.objects.get(id=kwargs['pk'])
        articleList = []
        trLang = Language.objects.all().get(id=8)
        for art in curForum.article_set.all() :
#            TranslateArticle(art,trLang)
            articleList += art.translatedarticle_set.filter(language=lang)
#        articleList += lang.translatedarticle_set.all()[page*10:(page+1)*10]
#        for page in range(1,10):
#            GetAnsweredLink(curForum,page)
        articlePerPage = 20 
        totArticleCount = len(articleList)
        pageCount = totArticleCount / articlePerPage 
        if totArticleCount % articlePerPage > 0 :
            pageCount = pageCount+1
        context = {
            'language':Language.objects.all(),
            'forum' : curForum,
            'currentLangCode':langcode.capitalize(),
            'pageCount' : pageCount,
            'currentPage' : page, 
            'latestposts':GetLatestPosts(),
            'articleList' : articleList[(page-1)*articlePerPage:page*articlePerPage],
        }
        return HttpResponse(self.template.render(context, self.request))

class Categories(generic.View):
    template = loader.get_template('categories.html')
    def get(self,*args,**kwargs):
        curLangCode = GetCurrentLanguageCode(self.request)
        context = {
            'language':Language.objects.all(),
            'currentLangCode':curLangCode.capitalize(),
            'category':Category.objects.get(id=kwargs['pk']),
            'latestposts':GetLatestPosts(),
        }
        return HttpResponse(self.template.render(context, self.request))

class Thread(generic.View):
    template = loader.get_template('thread.html')
    def get(self,*args,**kwargs):
        lang = Language.objects.get(langcode='ru')
        curTransArticle = TranslatedArticle.objects.get(id=kwargs['pk'])
        curLangCode = GetCurrentLanguageCode(self.request)

        context = {
            'language':Language.objects.all(),
            'currentLangCode':curLangCode.capitalize(),
            'transArticle':curTransArticle,
            'latestposts':GetLatestPosts(),
        }

#Optimize here...
        if curLangCode != curTransArticle.language.langcode :
            for trans in curTransArticle.parent.translatedarticle_set.all() :
                if trans.language.langcode == curLangCode:
                    return HttpResponseRedirect(reverse('thread', args=(trans.slug,trans.id,)))
            messages.warning(self.request,'This article is not translated in desired language yet.')
        return HttpResponse(self.template.render(context,self.request))

class ChangeLanguage(generic.View):
    def get(self,*args,**kwargs):
#        print(self.request.META.get('HTTP_REFERER'))
        lang = Language.objects.get(langcode=kwargs['langcode'])
#        print(lang.fullName)
        response = HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        response.set_cookie('currentLanguageCode',lang.langcode)
        return response

def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(request,username=name,password=pwd)
        if user is None:
            messages.warning(request, "Email or Password is incorrect." )
            return HttpResponseRedirect(reverse('login'))
        else :
            auth.login(request,user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#        return HttpResponse("I am a post")
    else:
        template = loader.get_template('login.html')
        context = {            
        }
        return HttpResponse(template.render(context,request))

def register(request):
    if request.method == 'POST' :
        name = request.POST['username']
        mail = request.POST['email']
        pwd = request.POST['password']
        if User.objects.filter(email=mail).exists() :
            messages.warning(request,'User with same email address already exists.Try with another email.')
        else :
            if User.objects.filter(username=name).exists() :
                messages.warning(request,'Same user name already exists.')
            else :
                user = User.objects.create_user(username=name,email=mail,password=pwd)
                user.save()
                messages.success(request,'Registered Successfully.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout(request):
    auth.logout(request)
#    return HttpResponseRedirect('/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def contactUs(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            # data = urllib.parse.urlencode(values)
            data = urllib.parse.urlencode(values).encode("utf-8")
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            result = json.load(response)
            ''' End reCAPTCHA validation '''
            print(result)
            if result['success']:
                form.save()

    return redirect('index')