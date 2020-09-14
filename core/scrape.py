import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import requests
from slugify import slugify
from .models import Category,Forum,Article, Question, Answer, TranslatedArticle, Language
# Ignore SSL certificate errors

def ToSlug(str):
    return slugify(str)
def SiteUrl():
	return "https://forums.tomshardware.com/"

def GetCategory():
    page = requests.get("https://forums.tomshardware.com/")
    soup = BeautifulSoup(page.content, 'html.parser')
    list_of_div = list(soup.find_all(
        'div', class_='block-container th_node--overwriteTextStyling'))
    category_list = []
    URL = 'https://forums.tomshardware.com'

    for category in list_of_div:
        h2 = category.find_all("h2")
        category_link = URL + h2[0].div.a['href']
        newCategory = Category(name=h2[0].div.a.text,origin_url=category_link)
        newCategory.slug = ToSlug(newCategory.name)
        newCategory.save()

        subcategorys = category.find_all("div", class_="node-main js-nodeMain")
        obj ={}
        subcategory_list = []
        for subcategory in subcategorys:
            sub_name = subcategory.h3.a.text
            link = URL + subcategory.h3.a['href']
            newForum = Forum(parent=newCategory)
            newForum.origin_url = link
            newForum.name = sub_name
            newForum.slug = ToSlug(sub_name)
            newForum.save()

#    print(category_list)


def GetAnsweredLink( parentforum, pageid ):
    url = parentforum.origin_url+"page-"+str(pageid)
    req = requests.get(url)
    soup = BeautifulSoup(req.text,"html.parser")
    tags = soup.find_all(class_='structItem-cell structItem-cell--main')
    for tag in tags:
        raw = str(tag)
        if raw.find("Thread Answered") == -1 :
            continue        
        link = SiteUrl()[:-1]+tag.find('div',class_='structItem-title').attrs['uix-data-href']
        GetArticleInfo(link,parentforum)
        print(link)

def GetArticleInfo( url, parent ):
    if Article.objects.filter(origin_url=url).exists() :
        print(url+'already exist')
        return
    blog = Article()
    blog.origin_url = url
    blog.parent = parent

    soup = BeautifulSoup(requests.get(url).text,'html.parser')

    blog.name = soup.find('h1',class_='p-title-value').text[9:]
    blog.save()

    lang = Language.objects.get(langcode='en')
    article = TranslatedArticle(parent=blog)
    article.language = lang 
    article.name = blog.name
    article.slug = ToSlug(article.name)
    article.save()
    
    questionTag = soup.find('article',class_='message--thfeature_firstPost')
    questionTag = questionTag.find('div',class_='bbWrapper')
    question = Question(parentArticle=article)
    question.content = str(questionTag)
    question.save()
    tags = soup('article')
    for tag in tags:
        val = str(tag)
        if val.find('message-inner--bestAnswer') == -1:
            continue
        tag = tag.find('div',class_='bbWrapper')
        answer = Answer(parentArticle=article)
        answer.content = str(tag)
        answer.save()

def TempAction():
    lang = Language(langcode='lv',fullName='latvian')
    lang.save()

    lang = Language(langcode='es',fullName='spanish')
    lang.save()

    lang = Language(langcode='ja',fullName='japanese')
    lang.save()

    lang = Language(langcode='ko',fullName='korean')
    lang.save()
