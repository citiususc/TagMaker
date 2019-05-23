from imagenes.forms import FormDataset, FormExperimento, FormTag
from imagenes.models import Dataset, Experimento, Image
from anotaciones.forms import FormAnotacion
from anotaciones.models import TagPoint, TagBox
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os, uuid, shutil, hashlib


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
            #Creamos dataset
            dataset = Dataset(name=postForm.cleaned_data['name'],
                              description=postForm.cleaned_data['description'])
            dataset.save()
            for file in request.FILES.getlist('files'):
                image_path=path_name+"/"+str(uuid.uuid4())+".jpg" #generamos un nombre

                with open(image_path, 'wb+') as image:
                    for chunk in file.chunks():
                        image.write(chunk)

                checksum = md5(image_path) #generamos el checksum de la imagen

                

                imagen = Image(name=file.name,
                           checksum=checksum,
                           path=image_path)
                imagen.save()
                dataset.images.add(imagen)
            return redirect('dataset_list')
    else:
        tagForm = F
        postForm = FormDataset()
    return render(request, 'createdataset.html', {'postForm': postForm})

def dataset(request, id):
    data=Dataset.objects.get(id=id)
    return render(request, 'dataset.html', {'data': data})


def modify_dataset(request, id):
    if request.method == 'POST':
        query = Dataset.objects.get(id=id)
        nombre=query.name
        for file in request.FILES.getlist('files'):
            nombre_imagen="Images/"+nombre+"/"+str(uuid.uuid4())+".jpg"
            with open(nombre_imagen, 'wb+') as image:
                for chunk in file.chunks():
                    image.write(chunk)
        datasets=Dataset.objects.all()
        return render(request, 'dataset_list.html', {'datasets': datasets})
    else:
        postForm = FormDataset()
    return render(request, 'add_images.html')

def delete_dataset(request, id):
    query = Dataset.objects.get(id=id)
    query.delete()
    nombre = query.name
    shutil.rmtree("Images/"+nombre)
    datasets = Dataset.objects.all()
    return render(request, 'dataset_list.html', {'datasets': datasets})

def experimento(request, id):
    exp=Experimento.objects.get(id=id)
    return render(request, 'experimento.html', {'exp': exp})

def create_anotacion(request):
    print("hola")



def new_experimento(request):
    if request.method == 'POST':

        expForm = FormExperimento(request.POST)


        e = Experimento(name=expForm.cleaned_data['name'],
                        description=expForm.cleaned_data['description'],
                        dataset=expForm.cleaned_data['dataset'],
                        equipo=expForm.cleaned_data['equipo'],
                        )
        e.save()

        """
        if expForm.is_valid() and anotForm.is_valid():
            a = Anotacion(anotaciones=anotForm.cleaned_data['anotaciones'],
                          tipo=anotForm.cleaned_data['tipo'])
            a.save()
            
            e.anotaciones.add(a)
            """
        return redirect('home')
    else:

        expForm = FormExperimento()
    return render(request, 'createexperimento.html', {'expForm': expForm})

def open_image(request, id):
    img=Image.objects.get(id=id)
    return render(request, 'image_page.html', {'img': img})

