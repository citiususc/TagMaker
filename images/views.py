from images.forms import FormDataset, FormExperiment, TagFormset
from images.models import Dataset, Experiment, Image, TagBox, TagPoint, TagImage
from users.models import Team
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os, uuid, shutil, hashlib, json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse, Http404

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
            path_name = settings.MEDIA_URL+postForm.cleaned_data.get('name')
            if not os.path.exists(path_name):
                os.makedirs(path_name)
            #Creamos dataset solo con el nombre y la descripción
            dataset = Dataset(name=postForm.cleaned_data['name'],
                              description=postForm.cleaned_data['description'])
            dataset.save()

            #para cada una de las imágenes seleccionadas realizamos lo siguiente:
            for file in request.FILES.getlist('files'):

                #Extraemos la extensión de la imagen
                file_name = file.name.split(".")
                extension=(file_name[1])

                #generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name=str(uuid.uuid4())
                image_path=path_name+"/"+random_name+"."+extension

                #guardamos la imagen en la ruta que proporcionamos
                with open(image_path, 'wb+') as image:
                    for chunk in file.chunks():
                        image.write(chunk)

                # comprobación de images repetidas
                checksum = md5(image_path)  # generamos el checksum de la imagen a partir de la ruta que antes generamos y comprobamos si existe en la BD.
                #En caso negativo almacenamos una instancia de Image en la BD y guardamos la imagen en la carpeta del dataset correspondiente.
                if not Image.objects.filter(checksum=checksum):
                    imagen = Image(name=file.name,
                               checksum=checksum,
                               path=path_name,
                               name_unique=random_name+"."+extension)
                    imagen.save()
                    dataset.images.add(imagen)
                #en caso de que sí exista debemos borrarla de la carpeta puesto que anteriormente la guardamos para poder hacer el checksum
                else:
                    os.remove(image_path);

            messages.success(request, '¡Dataset creado!')
            return redirect('dataset_list')
    else:
        postForm = FormDataset()
    return render(request, 'create_dataset.html', {'postForm': postForm})

@login_required
def dataset(request, id):
    data=Dataset.objects.get(id=id)
    return render(request, 'dataset.html', {'data': data})

@staff_member_required
@login_required
def modify_dataset(request, id):
    dataset = Dataset.objects.get(id=id)
    name_old = dataset.name
    data_images = Dataset.objects.get(id=id).images.all()
    if request.method == 'POST':
        dataForm = FormDataset(request.POST, instance=dataset)
        if dataForm.is_valid():
            dataForm.save() #actualizamos el dataset

            #Si el nombre fue cambiado
            if(name_old!=dataForm.cleaned_data['name']):
                #actualizamos la carpeta de imágenes
                path_old = settings.MEDIA_URL + name_old
                path_new = settings.MEDIA_URL + dataForm.cleaned_data['name']
                os.rename(path_old, path_new)
                #y actualizamos la ruta de las imágenes de la BD
                Image.objects.filter(path=path_old).update(path=path_new)

            # para cada una de las imágenes seleccionadas realizamos lo siguiente:
            for file in request.FILES.getlist('files'):
                # Extraemos la extensión de la imagen
                file_name = file.name.split(".")
                extension = (file_name[1])

                # generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name=str(uuid.uuid4())
                image_path = settings.MEDIA_URL + dataForm.cleaned_data['name']+ "/" + random_name +"."+extension

                # guardamos la imagen en la ruta que proporcionamos
                with open(image_path, 'wb+') as image:
                    for chunk in file.chunks():
                        image.write(chunk)

                    # comprobación de images repetidas
                checksum = md5(image_path)  # generamos el checksum de la imagen a partir de la ruta que antes generamos y comprobamos si existe en la BD.
                    # En caso negativo almacenamos una instancia de Image en la BD y guardamos la imagen en la carpeta del dataset correspondiente.
                if not Image.objects.filter(checksum=checksum):
                    imagen = Image(name=file.name,
                                   checksum=checksum,
                                   path=settings.MEDIA_URL + dataForm.cleaned_data['name'],
                                   name_unique=random_name+"."+extension)
                    imagen.save()
                    dataset.images.add(imagen)
                    # en caso de que sí exista debemos borrarla de la carpeta puesto que anteriormente la guardamos para poder hacer el checksum
                else:
                    os.remove(image_path)
        messages.success(request, 'El dataset ha sido modificado')
        return redirect('dataset', id=id)
    else:
        dataForm = FormDataset(instance=dataset)
    return render(request, 'modify_dataset.html', {'dataForm':dataForm, 'data_images':data_images, 'id_data':id})

@staff_member_required
@login_required
def delete_dataset(request, id):
    query = Dataset.objects.get(id=id)
    query.images.all().delete()
    query.delete()
    name = query.name
    shutil.rmtree(settings.MEDIA_URL+name)
    messages.success(request, '¡Dataset eliminado!')
    return redirect('dataset_list')

@staff_member_required
@login_required
def delete_image_dataset(request, id_data, id):
    query = Image.objects.get(id=id)
    query.delete()
    path=query.path+"/"+query.name_unique
    os.remove(path)
    return redirect('modify_dataset', id=id_data)

@staff_member_required
@login_required
def delete_tag_experiment(request, id_exp, id_tag, type):
    if type == 'punto':
        for point in TagPoint.objects.filter(id=id_tag).filter(experiment_id=id_exp):
            point.delete()
        if TagImage.objects.filter(experiment_id=id_exp).exists():
            TagImage.objects.get(experiment_id=id_exp).tags_points.all().delete()
    elif type =='caja':
        for box in TagBox.objects.filter(id=id_tag).filter(experiment_id=id_exp):
            box.delete()
        if TagImage.objects.filter(experiment_id=id_exp).exists():
            TagImage.objects.get(experiment_id=id_exp).tags_boxes.all().delete()
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
                                      team=expForm.cleaned_data['team'],)
            experiment.save()
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get('type') == 'Caja':
                        box = TagBox(
                            name=form.cleaned_data.get('name'),
                            experiment=experiment,
                            color=form.cleaned_data.get('color')
                        )
                        box.save()
                    elif form.cleaned_data.get('type') == 'Punto':
                        point = TagPoint(
                            name=form.cleaned_data.get('name'),
                            experiment=experiment,
                            color=form.cleaned_data.get('color')
                        )
                        point.save()
            messages.success(request, 'Experimento creado!')
            return redirect('experiment_list')
    else:
        formset = TagFormset()
        expForm = FormExperiment()
    return render(request, 'create_experiment.html', {'expForm': expForm, 'formset': formset})

@login_required
def experiment(request, id):
    exp=Experiment.objects.get(id=id)
    points = TagPoint.objects.all().filter(experiment_id=id).filter(x=None).filter(y=None)
    boxes = TagBox.objects.all().filter(experiment_id=id).filter(x_top_left=None).filter(y_top_left=None).filter(width=None).filter(height=None)
    tag_images= TagImage.objects.all().filter(experiment_id=id)
    return render(request, 'experiment.html', {'exp': exp, 'points':points, 'boxes': boxes, 'tag_images': tag_images})

@staff_member_required
@login_required
def delete_experiment(request, id):
    query = Experiment.objects.get(id=id)
    query.delete()
    messages.success(request, 'Experimento eliminado')
    return redirect ('experiment_list')

@staff_member_required
@login_required
def modify_experiment(request, id):
    experiment = Experiment.objects.get(id=id)
    points = TagPoint.objects.all().filter(experiment_id=id).filter(x=None).filter(y=None)
    boxes = TagBox.objects.all().filter(experiment_id=id).filter(x_top_left=None).filter(y_top_left=None).filter(width=None).filter(height=None)

    if request.method == 'POST':
        expForm = FormExperiment(request.POST, instance=experiment)
        formset = TagFormset(request.POST)
        if expForm.is_valid():
            expForm.save()
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get('type') == 'Caja':
                        box = TagBox(
                            name=form.cleaned_data.get('name'),
                            experiment=experiment,
                            color=form.cleaned_data.get('color')
                        )
                        box.save()
                    elif form.cleaned_data.get('type') == 'Punto':
                        point = TagPoint(
                            name=form.cleaned_data.get('name'),
                            experiment=experiment,
                            color=form.cleaned_data.get('color')
                        )
                        point.save()
            messages.success(request, 'El experimento ha sido modificado')
            return redirect('experiment', id=id)

    else:
        formset = TagFormset()
        expForm = FormExperiment(instance=experiment)
    return render(request, 'modify_experiment.html', {'expForm': expForm, 'id_exp':id, 'formset':formset, 'points':points, 'boxes': boxes})

@login_required
def images_experiment(request, id):
    exp = Experiment.objects.get(id=id)
    tag_images = None
    if TagImage.objects.filter(experiment_id=id).exists():
        tag_images = TagImage.objects.all().filter(experiment_id=id)
    return render(request, 'images_experiment.html', {'exp': exp, 'tag_images': tag_images})

@login_required
def annotate_image(request, id_exp, id_image, id_user):
    image = Image.objects.get(id=id_image)
    exp = Experiment.objects.get(id=id_exp)
    points = TagPoint.objects.all().filter(experiment_id=id_exp).filter(x=None).filter(y=None)
    boxes = TagBox.objects.all().filter(experiment_id=id_exp).filter(x_top_left=None).filter(y_top_left=None).filter(width=None).filter(height=None)
    tag_image = None

    #solo enviamos las anotaciones hechas por el usuario
    if TagImage.objects.filter(image_id=id_image).filter(user_id=id_user).exists():
        tag_image = TagImage.objects.get(image_id=id_image, user_id=id_user)
    return render(request, 'annotate.html', {'exp': exp, 'image': image, 'points': points, 'boxes': boxes, 'tag_image': tag_image})

@login_required
@csrf_exempt
def save_tags(request, id_exp, id_image):
    if request.method == 'POST':
        tag_image = None

        if 'canvas_data' in request.POST:
            data = request.POST['canvas_data']
            decoded = json.loads(data)

            # Si existe un TagImage para esta imagen donde el usuario corresponde con el actual
            if TagImage.objects.all().filter(image_id=id_image).filter(user_id=request.user.id):
                # Sobreescribimos las anotaciones

                tag_image = TagImage.objects.get(image_id=id_image, user_id=request.user.id)
                tag_image.tags_boxes.all().delete()
                tag_image.tags_points.all().delete()


            else:  # de lo contrario creamos un tagImage nuevo para este usuario
                if (request.user.is_staff):  # si el usuario que está realizando la anotación es staff, entendemos que ya está validada
                    check_by = request.user
                    tag_image = TagImage(image_id=id_image,
                                         user_id=request.user.id,
                                         experiment_id=id_exp,
                                         check_by=check_by)
                    tag_image.save()
                else:
                    tag_image = TagImage(image_id=id_image,
                                         user_id=request.user.id,
                                         experiment_id=id_exp)
                    tag_image.save()

            for obj in decoded['objects']:
                if (obj['type'] == 'circle'):
                    point = TagPoint(name=obj['name'],
                                     experiment_id=id_exp,
                                     x=obj['left'],
                                     y=obj['top'])
                    point.save()
                    tag_image.tags_points.add(point)
                elif (obj['type'] == 'rect'):
                    box = TagBox(name=obj['name'],
                                 experiment_id=id_exp,
                                 x_top_left=obj['left'],
                                 y_top_left=obj['top'],
                                 width=obj['width'],
                                 height=obj['height'])
                    box.save()
                    tag_image.tags_boxes.add(box)


    return redirect('experiment_list')

@login_required
@csrf_exempt
def validate(request, id_exp, id_image, id_user):
    #igual que en la función save_tags repetimos el mismo proceso
    if request.method == 'POST':
        #tag_image = TagImage.objects.filter(image_id=id_image).filter(experiment_id=id_exp).filter(user_id=id_user)
        tag_image = TagImage.objects.get(image_id=id_image, experiment_id=id_exp, user_id=id_user)
        tag_image.tags_points.all().delete()
        tag_image.tags_boxes.all().delete()

        if 'canvas_data' in request.POST:
            data = request.POST['canvas_data']
            decoded = json.loads(data)
            for obj in decoded['objects']:
                if (obj['type'] == 'circle'):
                    point = TagPoint(name=obj['name'],
                                     experiment_id=id_exp,
                                     x=obj['left'],
                                     y=obj['top'])
                    point.save()
                    tag_image.tags_points.add(point)
                elif (obj['type'] == 'rect'):
                    box = TagBox(name=obj['name'],
                                 experiment_id=id_exp,
                                 x_top_left=obj['left'],
                                 y_top_left=obj['top'],
                                 width=obj['width'],
                                 height=obj['height'])
                    box.save()
                    tag_image.tags_boxes.add(box)

        #ponemos en check_by al usuario staff que valida la anotación
        if(request.user.is_staff):
            tag_image.check_by=request.user
            tag_image.save()
            messages.success(request, 'Anotaciones validadas')

    return redirect('experiment_list')


@login_required
def download_tags(request, id_exp):
    experiment = Experiment.objects.get(id=id_exp)

    experiment_data = {
        "name": experiment.name,
        "description": experiment.description,
        "date": experiment.date.isoformat(),
        "dataset": experiment.dataset.name,
        "team": experiment.team.name,
        "tags_image": [],  #contiene todos los TagImage del experimento
    };

    if TagImage.objects.all().filter(experiment_id=experiment.id):
        tag_images=TagImage.objects.all().filter(experiment_id=experiment.id)
        for tag in tag_images:
            tag_image = {
                "image": tag.image.name,
                "user": tag.user.username,
                "check_by": tag.check_by.username,
                "points": [],
                "boxes": [],
            };

            tag_points = tag.tags_points
            for point in tag_points.all():
                tag_image["points"].append({
                    "name": point.name,
                    "coordinate_x": point.x,
                    "coordinate_y": point.y,
                });

            tag_boxes = tag.tags_boxes
            for box in tag_boxes.all():
                tag_image["boxes"].append({
                    "name": box.name,
                    "coordinate_x_top_left": box.x_top_left,
                    "coordinate_y_top_left": box.y_top_left,
                    "width": box.width,
                    "height": box.height,
                });

            experiment_data["tags_image"].append(tag_image)

    data = json.dumps(experiment_data)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename='+experiment.name+'.json'
    return response