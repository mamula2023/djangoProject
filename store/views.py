from curses.ascii import isblank

from django.http import HttpResponse, JsonResponse
import faker
import json

from django.shortcuts import render

from store.models import Category, Product


# Create your views here.
def categories(request):
    cats = list(Category.objects.all().values())

    result = []

    for cat in cats:
        category = {'name': cat['name'], 'id': cat['id']}
        parent_id = cat['parent_category_id']
        try:
            parent = Category.objects.get(id=parent_id)
            category['parent'] = parent.name
        except Category.DoesNotExist:
            category['parent'] = None

        result.append(category)
    return JsonResponse(
        {
            'categories': result
        })


def products(request):
    prods = list(Product.objects.all().values())
    result = []
    for prod in prods:
        prod_obj = Product.objects.get(id=prod['id'])
        cats = prod_obj.categories.all()

        prod['categories'] = list(cats.values())
        result.append(prod)

    return JsonResponse({'products': result})


def category(request):
    cats = Category.objects.select_related()

    return render(request, 'category_listing.html', {'categories': cats.values()})
