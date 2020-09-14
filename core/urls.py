from django.urls import path,include
from . import views

urlpatterns = [
    path( '', views.index, name='index' ),
    path( 'scrape/', views.Scrape.as_view(), name='scrape'),
    path( 'forums/<slug:forum>.<int:pk>/page-<int:page>', views.ForumView.as_view(), name='forums' ),
    path('categories/<str:category>.<int:pk>/', views.Categories.as_view(), name='categories'),
    path('thread/<str:slug>.<int:pk>/',views.Thread.as_view(), name='thread'),
    path('lang/<str:langcode>/',views.ChangeLanguage.as_view(), name='viewlanguage'),
    path('login/', views.login, name = 'login' ), 
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('contact-us/', views.contactUs, name = 'contact_us')
]