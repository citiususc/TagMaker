from imagenes.forms import FormDataset, FormExperimento, TagFormset
from imagenes.models import Dataset, Experimento, Image, TagBox, TagPoint
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os, uuid, shutil, hashlib
from django.contrib import messages
from django.forms import formset_factory


path = "static/images"
if not os.path.exists(path):
    os.makedirs(path)

def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, 'dataset_list.html', {'datasets': datasets})

def experimento_list(request):
    experimentos = Experimento.objects.all()
    return render(request, 'experimento_list.html', {'experimentos': experimentos})

def md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


@login_required
def new_dataset(request):
    if request.method == 'POST':
        postForm = FormDataset(request.POST)
        if postForm.is_valid():
            path_name = "static/images/"+postForm.cleaned_data.get('name')
            if not os.path.exists(path_name):
                os.makedirs(path_name)
            #Creamos dataset solo con el nombre y la descripción
            dataset = Dataset(name=postForm.cleaned_data['name'],
                              description=postForm.cleaned_data['description'])
            dataset.save()


            #para cada una de las imágenes seleccionadas realizamos lo siguiente:
            for file in request.FILES.getlist('files'):
                #generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name=str(uuid.uuid4())
                image_path=path_name+"/"+random_name+".jpg"

                #guardamos la imagen en la ruta que proporcionamos
                with open(image_path, 'wb+') as image:
                    for chunk in file.chunks():
                        image.write(chunk)

                # comprobación de imagenes repetidas
                checksum = md5(image_path)  # generamos el checksum de la imagen a partir de la ruta que antes generamos y comprobamos si existe en la BD.
                #En caso negativo almacenamos una instancia de Image en la BD y guardamos la imagen en la carpeta del dataset correspondiente.
                if not Image.objects.filter(checksum=checksum):
                    imagen = Image(name=file.name,
                               checksum=checksum,
                               path=path_name,
                               name_unique=random_name)
                    imagen.save()
                    dataset.images.add(imagen)
                #en caso de que sí exista debemos borrarla de la carpeta puesto que anteriormente la guardamos para poder hacer el checksum
                else:
                    os.remove(image_path);

            messages.success(request, 'El dataset ha sido creado con éxito')
            return redirect('dataset_list')
    else:
        postForm = FormDataset()
    return render(request, 'createdataset.html', {'postForm': postForm})

def dataset(request, id):
    data=Dataset.objects.get(id=id)
    return render(request, 'dataset.html', {'data': data})


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
                path_old = "static/images/" + name_old
                path_new = "static/images/" + dataForm.cleaned_data['name']
                os.rename(path_old, path_new)
                #y actualizamos la ruta de las imágenes de la BD
                Image.objects.filter(path=path_old).update(path=path_new)

            # para cada una de las imágenes seleccionadas realizamos lo siguiente:
            for file in request.FILES.getlist('files'):
                # generamos un nombre ÚNICO para la imagen y generamos su ruta dentro del proyecto
                random_name=str(uuid.uuid4())
                image_path = "static/images/" + dataForm.cleaned_data['name']+ "/" + random_name + ".jpg"

                # guardamos la imagen en la ruta que proporcionamos
                with open(image_path, 'wb+') as image:
                    for chunk in file.chunks():
                        image.write(chunk)

                    # comprobación de imagenes repetidas
                checksum = md5(image_path)  # generamos el checksum de la imagen a partir de la ruta que antes generamos y comprobamos si existe en la BD.
                    # En caso negativo almacenamos una instancia de Image en la BD y guardamos la imagen en la carpeta del dataset correspondiente.
                if not Image.objects.filter(checksum=checksum):
                    imagen = Image(name=file.name,
                                   checksum=checksum,
                                   path="static/images/" + dataForm.cleaned_data['name'],
                                   name_unique=random_name)
                    imagen.save()
                    dataset.images.add(imagen)
                    # en caso de que sí exista debemos borrarla de la carpeta puesto que anteriormente la guardamos para poder hacer el checksum
                else:
                    os.remove(image_path)
        return redirect('dataset', id=id)
    else:
        dataForm = FormDataset(instance=dataset)
    return render(request, 'modifydataset.html', {'dataForm':dataForm, 'data_images':data_images, 'id_data':id})

def delete_dataset(request, id):
    query = Dataset.objects.get(id=id)
    query.images.all().delete()
    query.delete()
    nombre = query.name
    shutil.rmtree("static/images/"+nombre)
    datasets = Dataset.objects.all()
    return render(request, 'dataset_list.html', {'datasets': datasets})

def delete_image_dataset(request, id_data, id):
    query = Image.objects.get(id=id)
    query.delete()
    path=query.path+"/"+query.name_unique+".jpg"
    os.remove(path)
    return redirect('modify_dataset', id=id_data)




def experimento(request, id):
    exp=Experimento.objects.get(id=id)
    return render(request, 'experimento.html', {'exp': exp})




def new_experimento(request):
    if request.method == 'POST':

        expForm = FormExperimento(request.POST)
        formset = TagFormset(request.POST)

        if expForm.is_valid():
            experimento = Experimento(name=expForm.cleaned_data['name'],
                                      description=expForm.cleaned_data['description'],
                                      dataset=expForm.cleaned_data['dataset'],
                                      equipo=expForm.cleaned_data['equipo'],)
            experimento.save()
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get('type') == 'Caja':
                        box = TagBox(
                            name=form.cleaned_data.get('name')
                        )
                       # box.save()
                       # experimento.tags_box.add(box)
                    elif form.cleaned_data.get('type') == 'Punto':
                        point = TagPoint(
                            name=form.cleaned_data.get('name')
                        )
                       # point.save()
                      #  experimento.tags_box.add(box)


        return redirect('home')
    else:
        formset = TagFormset()
        expForm = FormExperimento()
    return render(request, 'createexperimento.html', {'expForm': expForm, 'formset': formset})

def open_image(request, id):
    img=Image.objects.get(id=id)
    return render(request, 'image_page.html', {'img': img})

