from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from usuarios import views as usuarios_views
from imagenes import views as imagenes_views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    url(r'^$', usuarios_views.home, name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^signup/$', usuarios_views.signup, name='signup'),
    url(r'^micuenta/$', usuarios_views.profile, name='profile'),
    url(r'^micuenta/editar/$', usuarios_views.editprofile, name='edit'),
    url(r'^micuenta/password/$', usuarios_views.changepassword, name='changepassword'),
    path('admin/', admin.site.urls),
    url(r'^createdataset/$', imagenes_views.new_dataset, name='create_dataset'),
    url(r'^datasets/$', imagenes_views.dataset_list, name='dataset_list'),
    url(r'^datasets/(?P<id>[0-9]+)$', imagenes_views.dataset, name='dataset'),
    url(r'^datasets_borrar/(?P<id>[0-9]+)$', imagenes_views.delete_dataset, name='delete_dataset'),
    url(r'^datasets/añadirimagenes(?P<id>[0-9]+)$', imagenes_views.modify_dataset, name='modify_dataset'),
    url(r'^createexperimento/$', imagenes_views.new_experimento, name='create_experimento'),
    url(r'^experimentos/$', imagenes_views.experimento_list, name='experimento_list'),
    url(r'^experimentos/(?P<id>[0-9]+)$', imagenes_views.experimento, name='experimento'),
]