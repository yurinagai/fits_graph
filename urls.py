from django.urls import path

from . import views

app_name = 'graph'
urlpatterns = [
    path('', views.index, name='index'),
    path('calc', views.calc),
    path('del_file', views.del_file)
]
