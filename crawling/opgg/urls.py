from django.urls import path
from . import views

app_name='crawl'

urlpatterns=[
    path('',views.search,name='search'),
    path('info/',views.info,name='info'),
    path('alluser/',views.all_user,name='user')
]