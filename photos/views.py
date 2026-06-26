from django.shortcuts import render, redirect 
from .models import Category, Photo 

# Create your views here.
def gallery(request):
    category = request.GET.get('category')
    
    if category == None:
       photos = Photo.objects.all()
    else:
       photos = Photo.objects.filter(category__name__iexact=category)
       
    categories = Category.objects.all()   
    
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)
    
def viewPhoto(request, pk):
    photo = Photo.objects.get(id = pk)
    return render(request, 'photos/photo.html', {'photo': photo})
    
def addPhoto(request):
    categories = Category.objects.all()

    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist('images')

        category = None

        if data.get('category') and data.get('category') != 'none':
            category = Category.objects.get(id=data.get('category'))

        elif data.get('category_new'):
            category_name = data.get('category_new').strip()
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)

        for img in images:
            Photo.objects.create(
                category=category,
                description=data.get('description', ''),
                image=img,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)