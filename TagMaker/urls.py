from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from users import views as users_view
from images import views as images_views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('', users_view.home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', users_view.sign_up, name='sign_up'),
    path('micuenta/', users_view.profile, name='profile'),
    path('micuenta/editar/', users_view.edit_profile, name='edit'),
    path('micuenta/editar/password/', users_view.change_password, name='change_password'),
    path('micuenta/borrar/', users_view.delete_profile, name='delete_profile'),
    path('admin/', admin.site.urls),
    path('dataset/nuevo/', images_views.new_dataset, name='create_dataset'),
    path('datasets/', images_views.dataset_list, name='dataset_list'),
    path('datasets/<id>/', images_views.dataset, name='dataset'),
    path('datasets/<id>/modificar/', images_views.modify_dataset, name='modify_dataset'),
    path('datasets/<id_data>/borrarimagen/<id>/', images_views.delete_image_dataset, name='delete_image_dataset'),
    path('datasets/<id>/borrar/', images_views.delete_dataset, name='delete_dataset'),
    path('experimentos/', images_views.experiment_list, name='experiment_list'),
    path('experimentos/nuevo/',images_views.new_experiment, name='create_experiment'),
    path('datasets/<id_exp>/borraretiqueta/<id_tag>/<type>/', images_views.delete_tag_experiment, name='delete_tag_experiment'),
    path('experimento/<id>/borrar/',images_views.delete_experiment, name='delete_experiment'),
    path('experimentos/<id>/', images_views.experiment, name='experiment'),
    path('experimentos/<id>/modificar/', images_views.modify_experiment, name='modify_experiment'),
    path('experimentos/<id>/images/', images_views.images_experiment, name='images_experiment'),
    path('anotarimagen/<id_exp>/<id_image>/<id_user>/', images_views.annotate_image, name='annotate_image'),
    path('anotarimagen/<id_exp>/<id_image>/save/', images_views.save_tags, name='save_tags')
 #   path('anotarimagen/<id_exp>/<id_image>/<id_user>/validate/', images_views.validate, name='validate')
]