from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from users import views as users_view
from images import views as images_views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
                  path('', users_view.home, name='home'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('signup/', users_view.sign_up, name='sign_up'),
                  path('myprofile/', users_view.profile, name='profile'),
                  path('myprofile/edit/', users_view.edit_profile, name='edit'),
                  path('myprofile/password/', users_view.change_password, name='change_password'),
                  path('myprofile/delete/', users_view.delete_profile, name='delete_profile'),
                  url('admin/', admin.site.urls, name='admin'),
                  path('datasets/new/', images_views.new_dataset, name='create_dataset'),
                  path('datasets/', images_views.dataset_list, name='dataset_list'),
                  path('datasets/<id>/', images_views.dataset, name='dataset'),
                  path('datasets/<id>/edit/', images_views.modify_dataset, name='modify_dataset'),
                  path('datasets/<id_data>/delete/<id>/', images_views.delete_image_dataset,
                       name='delete_image_dataset'),
                  path('datasets/<id>/delete/', images_views.delete_dataset, name='delete_dataset'),
                  path('datasets/<name>/download/', images_views.download_dataset, name='download_dataset'),
                  path('experiments/', images_views.experiment_list, name='experiment_list'),
                  path('experiment/new/', images_views.new_experiment, name='create_experiment'),
                  path('experiment/<id_exp>/delete/<id_annotation_type>/',
                       images_views.delete_annotation_type_experiment,
                       name='delete_annotation_type_experiment'),
                  path('experiment/<id>/delete/', images_views.delete_experiment, name='delete_experiment'),
                  path('experiment/<id>/', images_views.experiment, name='experiment'),
                  path('experiment/<id>/edit/', images_views.modify_experiment, name='modify_experiment'),
                  path('experiment/<id>/images/', images_views.images_experiment, name='images_experiment'),
                  path('annotate/<id_exp>/<id_image>/<id_user>/', images_views.annotate_image, name='annotate_image'),
                  path('annotate/<id_exp>/<id_image>/', images_views.save_tags, name='save_tags'),
                  path('annotate/validate/<id_exp>/<id_image>/<id_user>/', images_views.validate, name='validate'),
                  path('annotate/invalidate/<id_exp>/<id_image>/<id_user>/', images_views.invalidate, name='invalidate'),
                  path('experiment/<id_exp>/download/', images_views.download_tags, name='download'),
                  path('experiment/<id_exp>/download/images/', images_views.download_tagged_images, name='download_tagged_images'),
                  url(r'^i18n/', include('django.conf.urls.i18n')),
                  path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
