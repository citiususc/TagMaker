from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from usuarios import views as usuarios_views
from imagenes import views as imagenes_views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('', usuarios_views.home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', usuarios_views.signup, name='signup'),
    path('micuenta/', usuarios_views.profile, name='profile'),
    path('micuenta/editar/', usuarios_views.editprofile, name='edit'),
    path('micuenta/editar/password/', usuarios_views.changepassword, name='changepassword'),
    path('admin/', admin.site.urls),
    path('dataset/nuevo/', imagenes_views.new_dataset, name='create_dataset'),
    path('datasets/', imagenes_views.dataset_list, name='dataset_list'),
    path('datasets/<id>/', imagenes_views.dataset, name='dataset'),
    path('datasets/<id>/modificar/', imagenes_views.modify_dataset, name='modify_dataset'),
    path('datasets/<id_data>/borrarimagen/<id>/', imagenes_views.delete_image_dataset, name='delete_image_dataset'),
    path('datasets/<id>/borrar/', imagenes_views.delete_dataset, name='delete_dataset'),
    path('experimentos/', imagenes_views.experimento_list, name='experimento_list'),
    path('experimentos/nuevo/',imagenes_views.new_experimento, name='create_experimento'),
    path('experimentos/<int:id>', imagenes_views.experimento, name='experimento'),
    path('anotarimagen/<int:id>', imagenes_views.open_image, name='open_image'),
]