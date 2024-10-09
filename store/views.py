from django.http import HttpResponse, JsonResponse
import faker
import json

from store.models import Category, Product


# Create your views here.
def categories(request):
    cats = Category.objects.all()
    print(cats)
    return JsonResponse(
        {
            'categories': list(cats.values('id', 'name', 'parent_category_id', 'parent_category__name')),
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
