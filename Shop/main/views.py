from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from products.models import Product, ProductImage, ProductCategory


def home(request):
    images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    images_tv = images.filter(product__category__id=1)
    images_phone = images.filter(product__category__id=2)
    images_laptop = images.filter(product__category__id=3)
    return render(request, 'main/home.html', locals())


def catalog(request, category_slug=None):
    category = None
    search_query = request.GET.get('search', '')
    categories = ProductCategory.objects.all()
    page_number = request.GET.get('page')

    if search_query:
        images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True,
                                             product__product_name__icontains=search_query)
        paginator = Paginator(images, 8)
        page_obj = paginator.get_page(page_number)
    else:
        images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
        paginator = Paginator(images, 8)
        page_obj = paginator.get_page(page_number)

    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        images = images.filter(product__category=category)
        paginator = Paginator(images, 8)
        page_obj = paginator.get_page(page_number)

    return render(request, 'main/catalog.html', locals())
