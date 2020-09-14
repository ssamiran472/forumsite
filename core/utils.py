from django.http import HttpResponse

def GetCurrentLanguageCode(request):
    ret = request.COOKIES.get('currentLanguageCode')
    if ret is None:
        ret = 'en'
    return ret