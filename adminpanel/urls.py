from django.urls import path,include
from . import views

urlpatterns = [
    path( 'dashboard/', views.index, name='dashboard' ),
    path( 'gather/', views.Gather.as_view(), name='gather'),
    path( 'result/', views.Result.as_view(), name = 'result'),
    path( 'contact/page-<int:page>', views.Contact.as_view(), name = 'contact' ),
    path( 'template/', views.TemplateSetting.as_view(), name = 'template' ),
]