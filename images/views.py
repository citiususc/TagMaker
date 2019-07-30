import hashlib
import json
import os
import shutil
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from images.forms import FormDataset, FormExperiment, TagFormset
from images.models import Dataset, Experiment, Image, IndividualTagBox, IndividualTagPoint, ImageTag, AnnotationType, \
    IndividualTag
from users.models import Team
from PIL import Image as PILImage


@login_required
def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, 'dataset_list.html', {'datasets': datasets})


@login_required
def experiment_list(request):
    experiments = []

    for team in Team.objects.all():
        if request.user in team.users.all():
            if Experiment.objects.filter(team_id=team.id):
                experiment = Experiment.objects.get(team_id=team.id)
                experiments.append(experiment)

    return render(request, 'experiment_list.html', {'experiments': experiments})


def md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


@staff_member_required
@login_required
def new_dataset(request):
    if request.method == 'POST':

        postForm = FormDataset(request.POST)

        if postForm.is_valid():
            path_name = settings.MEDIA_URL + postForm.cleaned_data.get('name')
            if not os.path.exists(path_name):
                os.makedirs(path_name)
            # Creamos dataset solo con el nombre y la descripción
            dataset = Dataset(name=postForm.cleaned_data['name'],
                              description=postForm.cleaned_data['description'])
            dataset.save()

            # para cada una de las imágenes seleccionadas realizamos lo siguiente:
            for file in request.FILES.getlist('files'):

                # Extraemos la extensión de la imagen
                file_name, original_extension = file.name.split(".")
                new_extension = "jpg"

                # generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name = str(uuid.uuid4())
                image_path = "{dir}/{name}.{ext}".format(dir=path_name,
                                                         name=random_name,
                                                         ext=new_extension)

                # guardamos la imagen en la ruta que proporcionamos
                # with open(image_path, 'wb+') as image:
                #     for chunk in file.chunks():
                #         image.write(chunk)
                PILImage.open(file).save(image_path)

                # comprobación de images repetidas
                # generamos el checksum de la imagen a partir de la ruta que antes generamos y comprobamos si existe en la BD.
                checksum = md5(image_path)
                # En caso negativo almacenamos una instancia de Image en la BD y guardamos la imagen en la carpeta del dataset correspondiente.
                if not Image.objects.filter(checksum=checksum):
                    imagen = Image(name=file.name.replace(original_extension, new_extension),
                                   checksum=checksum,
                                   path=path_name,
                                   name_unique="{name}.{ext}".format(name=random_name,
                                                                     ext=new_extension))
                    imagen.save()
                    dataset.images.add(imagen)
                # en caso de que sí exista debemos borrarla de la carpeta puesto que anteriormente la guardamos para poder hacer el checksum
                else:
                    os.remove(image_path)

            messages.success(request, _('The dataset has been created successfully!'))
            return redirect('dataset_list')
    else:
        postForm = FormDataset()
    return render(request, 'create_dataset.html', {'postForm': postForm})


@login_required
def dataset(request, id):
    data = Dataset.objects.get(id=id)
    images = data.images.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(images, 36)  # 6x6 grid
    try:
        data_images = paginator.page(page)
    except PageNotAnInteger:
        data_images = paginator.page(1)
    except EmptyPage:
        data_images = paginator.page(paginator.num_pages)
    return render(request, 'dataset.html', {'data': data, 'data_images': data_images})


@staff_member_required
@login_required
def modify_dataset(request, id):
    dataset = Dataset.objects.get(id=id)
    name_old = dataset.name
    images = Dataset.objects.get(id=id).images.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(images, 36)  # 6x6 grid
    try:
        data_images = paginator.page(page)
    except PageNotAnInteger:
        data_images = paginator.page(1)
    except EmptyPage:
        data_images = paginator.page(paginator.num_pages)

    duplicate_images = 0
    if request.method == 'POST':
        dataForm = FormDataset(request.POST, instance=dataset)
        if dataForm.is_valid():
            path_name = settings.MEDIA_URL + dataForm.cleaned_data.get('name')
            dataForm.save()  # actualizamos el dataset

            # Si el nombre fue cambiado
            if (name_old != dataForm.cleaned_data['name']):
                # actualizamos la carpeta de imágenes
                path_old = settings.MEDIA_URL + name_old
                path_new = settings.MEDIA_URL + dataForm.cleaned_data['name']
                os.rename(path_old, path_new)
                # y actualizamos la ruta de las imágenes de la BD
                Image.objects.filter(path=path_old).update(path=path_new)

            # para cada una de las imágenes seleccionadas realizamos lo siguiente:
            for file in request.FILES.getlist('files'):
                # Extraemos la extensión de la imagen
                file_name, original_extension = file.name.split(".")
                new_extension = "jpg"

                # generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name = str(uuid.uuid4())
                image_path = "{dir}/{name}.{ext}".format(dir=path_name,
                                                         name=random_name,
                                                         ext=new_extension)

                # generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name = str(uuid.uuid4())
                image_path = "{dir}/{name}.{ext}".format(dir=path_name,
                                                         name=random_name,
                                                         ext=new_extension)

                # guardamos la imagen en la ruta que proporcionamos
                # with open(image_path, 'wb+') as image:
                #     for chunk in file.chunks():
                #         image.write(chunk)
                PILImage.open(file).save(image_path)

                    # comprobación de images repetidas
                checksum = md5(
                    image_path)  # generamos el checksum de la imagen a partir de la ruta que antes generamos y comprobamos si existe en la BD.
                # En caso negativo almacenamos una instancia de Image en la BD y guardamos la imagen en la carpeta del dataset correspondiente.
                if not Image.objects.filter(checksum=checksum):
                    imagen = Image(name=file.name,
                                   checksum=checksum,
                                   path=settings.MEDIA_URL + dataForm.cleaned_data['name'],
                                   name_unique="{name}.{ext}".format(name=random_name,
                                                                     ext=new_extension))
                    imagen.save()
                    dataset.images.add(imagen)
                    # en caso de que sí exista debemos borrarla de la carpeta puesto que anteriormente la guardamos para poder hacer el checksum
                else:
                    duplicate_images += 1
                    os.remove(image_path)
        if duplicate_images == 0:
            messages.success(request, _("The dataset has been modified successfully!"))
        else:
            messages.warning(request,
                             _(
                                 "The dataset has been modified, but {} duplicated image(s) have not been uploaded").format(
                                 duplicate_images))
        return redirect('dataset', id=id)
    else:
        dataForm = FormDataset(instance=dataset)
    return render(request, 'modify_dataset.html', {'dataForm': dataForm, 'data_images': data_images, 'id_data': id})


@staff_member_required
@login_required
def delete_dataset(request, id):
    query = Dataset.objects.get(id=id)
    query.images.all().delete()
    query.delete()
    name = query.name
    shutil.rmtree(settings.MEDIA_URL + name)
    messages.success(request, _('Dataset deleted successfully!'))
    return redirect('dataset_list')


@staff_member_required
@login_required
def delete_image_dataset(request, id_data, id):
    query = Image.objects.get(id=id)
    query.delete()
    path = query.path + "/" + query.name_unique
    os.remove(path)
    return redirect('modify_dataset', id=id_data)


@staff_member_required
@login_required
def delete_annotation_type_experiment(request, id_exp, id_annotation_type):
    AnnotationType.objects.filter(id=id_annotation_type).delete()
    IndividualTag.objects.filter(type_id=id_annotation_type).all().delete()

    return redirect('modify_experiment', id_exp)


@staff_member_required
@login_required
def new_experiment(request):
    if request.method == 'POST':
        expForm = FormExperiment(request.POST)
        formset = TagFormset(request.POST)
        if expForm.is_valid():

            experiment = Experiment(name=expForm.cleaned_data['name'],
                                    description=expForm.cleaned_data['description'],
                                    dataset=expForm.cleaned_data['dataset'],
                                    team=expForm.cleaned_data['team'], )
            experiment.save()
            if formset.is_valid():
                for form in formset:
                    annotation_type = AnnotationType(name=form.cleaned_data.get('name'),
                                                     color=form.cleaned_data.get('color'),
                                                     experiment=experiment,
                                                     primitive=form.cleaned_data.get('type'))
                    annotation_type.save()
            messages.success(request, _('Experiment created successfully!'))
            return redirect('experiment_list')
    else:
        formset = TagFormset()
        expForm = FormExperiment()
    return render(request, 'create_experiment.html', {'expForm': expForm, 'formset': formset})


@login_required
def experiment(request, id):
    exp = Experiment.objects.get(id=id)
    annotation_types = AnnotationType.objects.all().filter(experiment_id=id)
    tag_images = ImageTag.objects.all().filter(experiment_id=id)
    return render(request, 'experiment.html',
                  {'exp': exp, 'annotation_types': annotation_types, 'tag_images': tag_images})


@staff_member_required
@login_required
def delete_experiment(request, id):
    query = Experiment.objects.get(id=id)
    query.delete()
    messages.success(request, _('Experiment deleted'))
    return redirect('experiment_list')


@staff_member_required
@login_required
def modify_experiment(request, id):
    experiment = Experiment.objects.get(id=id)
    annotation_types = AnnotationType.objects.all().filter(experiment_id=id)

    if request.method == 'POST':
        expForm = FormExperiment(request.POST, instance=experiment)
        formset = TagFormset(request.POST)
        if expForm.is_valid():
            expForm.save()
            if formset.is_valid():
                for form in formset:
                    annotation_type = AnnotationType(name=form.cleaned_data.get('name'),
                                                     color=form.cleaned_data.get('color'),
                                                     experiment=experiment,
                                                     primitive=form.cleaned_data.get('type'))
                    annotation_type.save()
            messages.success(request, _('The experiment has been modified'))
            return redirect('experiment', id=id)

    else:
        formset = TagFormset()
        expForm = FormExperiment(instance=experiment)
    return render(request, 'modify_experiment.html',
                  {'expForm': expForm, 'id_exp': id, 'formset': formset, 'annotation_types': annotation_types})


@login_required
def images_experiment(request, id):
    exp = Experiment.objects.get(id=id)
    tag_images = None
    if ImageTag.objects.filter(experiment_id=id).exists():
        tag_images = ImageTag.objects.all().filter(experiment_id=id)
    return render(request, 'images_experiment.html', {'exp': exp, 'tag_images': tag_images})


@login_required
def annotate_image(request, id_exp, id_image, id_user):
    image = Image.objects.get(id=id_image)
    exp = Experiment.objects.get(id=id_exp)
    annotation_types = AnnotationType.objects.filter(experiment_id=id_exp).all()
    tag_image = None

    # solo enviamos las anotaciones hechas por el usuario
    if ImageTag.objects.filter(image_id=id_image).filter(user_id=id_user).exists():
        tag_image = ImageTag.objects.get(image_id=id_image, user_id=id_user)
    return render(request, 'annotate.html',
                  {'exp': exp,
                   'image': image,
                   'annotation_types': annotation_types,
                   'tag_image': tag_image})


@login_required
@csrf_exempt
def save_tags(request, id_exp, id_image):
    if request.method == 'POST':
        tag_image = None

        if 'canvas_data' in request.POST:
            data = request.POST['canvas_data']
            decoded = json.loads(data)

            # Si existe un ImageTag para esta imagen donde el usuario corresponde con el actual
            if ImageTag.objects.filter(image_id=id_image).filter(user_id=request.user.id).all():
                # Sobreescribimos las anotaciones

                tag_image = ImageTag.objects.get(image_id=id_image, user_id=request.user.id)
                tag_image.individual_tags.all().delete()

                # si se borran todas las anotaciones tambien borramos el tagimage
                if not decoded['objects']:
                    tag_image.delete()

            else:  # de lo contrario creamos un tagImage nuevo para este usuario

                if request.user.is_staff:  # si el usuario que está realizando la anotación es staff, entendemos que ya está validada
                    tag_image = ImageTag(image_id=id_image,
                                         user_id=request.user.id,
                                         experiment_id=id_exp,
                                         check_by=request.user)
                else:
                    tag_image = ImageTag(image_id=id_image,
                                         user_id=request.user.id,
                                         experiment_id=id_exp)
                tag_image.save()

            for obj in decoded['objects']:
                if obj['type'] == 'circle':
                    annotation_type = AnnotationType.objects.get(name=obj["name"], experiment_id=id_exp)
                    point = IndividualTagPoint(image_tag=tag_image,
                                               type=annotation_type,
                                               x=obj['left'],
                                               y=obj['top'])
                    point.save()
                    annotation_type.state = True
                    annotation_type.save()

                elif obj['type'] == 'rect':
                    annotation_type = AnnotationType.objects.get(name=obj["name"], experiment_id=id_exp)
                    box = IndividualTagBox(image_tag=tag_image,
                                           type=annotation_type,
                                           x_top_left=obj['left'],
                                           y_top_left=obj['top'],
                                           width=obj['width'],
                                           height=obj['height'])
                    box.save()
                    annotation_type.state = True
                    annotation_type.save()

    return redirect('experiment_list')


@login_required
@csrf_exempt
def validate(request, id_exp, id_image, id_user):
    # igual que en la función save_tags repetimos el mismo proceso
    if request.method == 'POST':
        tag_image = ImageTag.objects.get(image_id=id_image, experiment_id=id_exp, user_id=id_user)
        tag_image.individual_tags.all().delete()

        if 'canvas_data' in request.POST:
            data = request.POST['canvas_data']
            decoded = json.loads(data)

            # si se borran todas las anotaciones tambien borramos el tagimage
            if not decoded['objects']:
                tag_image.delete()
            else:
                for obj in decoded['objects']:
                    if obj['type'] == 'circle':
                        annotation_type = AnnotationType.objects.get(name=obj["name"], experiment_id=id_exp)
                        point = IndividualTagPoint(image_tag=tag_image,
                                                   type=annotation_type,
                                                   x=obj['left'],
                                                   y=obj['top'])
                        point.save()
                        annotation_type.state = True
                        annotation_type.save()
                    elif obj['type'] == 'rect':
                        annotation_type = AnnotationType.objects.get(name=obj["name"], experiment_id=id_exp)
                        box = IndividualTagBox(image_tag=tag_image,
                                               type=annotation_type,
                                               x_top_left=obj['left'],
                                               y_top_left=obj['top'],
                                               width=obj['width'],
                                               height=obj['height'])
                        box.save()
                        annotation_type.state = True
                        annotation_type.save()

        # ponemos en check_by al usuario staff que valida la anotación
        if request.user.is_staff:
            tag_image.check_by = request.user
            tag_image.save()
            messages.success(request, 'Anotaciones validadas')

    return redirect('experiment_list')


@login_required
def download_tags(request, id_exp):
    experiment = Experiment.objects.get(id=id_exp)

    experiment_data = {
        "name": experiment.name,
        "description": experiment.description,
        "creation_date": experiment.date.isoformat(),
        "dataset": experiment.dataset.name,
        "team": experiment.team.name,
        "annotations": [],  # contiene todos los TagImage del experimento
    }

    if ImageTag.objects.all().filter(experiment_id=experiment.id):
        tag_images = ImageTag.objects.all().filter(experiment_id=experiment.id)
        for tag in tag_images:
            tag_image = {
                "image": tag.image.name,
                "user": tag.user.username,
                "check_by": tag.check_by.username,
                "individual_annotations": [],
            }

            individual_tags = tag.individual_tags
            for it in individual_tags.all():
                if it.type.primitive == "Point":
                    tag_image["individual_annotations"].append({
                        "type": it.type.name,
                        "color": it.type.color,
                        "coordinate_x": it.individualtagpoint.x,
                        "coordinate_y": it.individualtagpoint.y,
                    })
                elif it.type.primitive == "Box":
                    tag_image["individual_annotations"].append({
                        "type": it.type.name,
                        "primitive": it.type.primitive,
                        "color": it.type.color,
                        "coordinate_x_top_left": it.individualtagbox.x_top_left,
                        "coordinate_y_top_left": it.individualtagbox.y_top_left,
                        "width": it.individualtagbox.width,
                        "height": it.individualtagbox.height,
                    })

            experiment_data["annotations"].append(tag_image)

    data = json.dumps(experiment_data)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=' + experiment.name + '.json'
    return response
