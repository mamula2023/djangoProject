from django.db.models import Sum, F, Min, Max, Avg
from django.http import HttpResponse, JsonResponse

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
    cats = Category.objects.all()

    return render(request, 'category_listing.html', {'categories': cats.values()})


def category_products(request, category_id):
    result = {}

    all_categories = Category.objects.prefetch_related('products')

    cats_queue = [category_id]

    most_expensive = 0
    cheapest = -1
    total_price = 0
    total_value = 0
    while len(cats_queue) > 0:
        cat_id = cats_queue.pop(0)

        # children = all_categories.filter(parent_category_id=cat_id).all()
        # using iterations over all_categories instead of filtering resulted in
        # 9 (with similar queries) -> 2 queries on my data
        children = []
        for cat in all_categories:
            if cat.parent_category_id == cat_id:
                children.append(cat)

        for child in children:
            prods = child.products.all() #.annotate(total=F('stock')*F('price'))
            for prod in prods:
                if prod not in result:
                    result[prod] = prod.price * prod.stock
                    most_expensive = max(prod.price, most_expensive)
                    if cheapest == -1:
                        cheapest = prod.price
                    else:
                        cheapest = min(prod.price, cheapest)
                    total_price += prod.price
                    total_value += prod.stock * prod.price
            cats_queue.append(child.id)



    return render(request, 'category_products.html',
                  {'products': result,
                   'most_expensive': most_expensive,
                   'cheapest': cheapest,
                   'total_value': total_value,
                   'avg_price': total_price/len(result)}

                  )








    # prods = (Product.objects.prefetch_related('categories')
    #          .annotate(total=F('stock')*F('price')).values())
    #
    # expensive_price = prods.aggregate(max_price=Max('price'))['max_price']
    # cheap_price = prods.aggregate(min_price=Min('price'))['min_price']
    # avg_price = prods.aggregate(avg_price=Avg('price'))['avg_price']
    # total_price = prods.aggregate(total=Sum(F('stock')*F('price')))['total']

    # print(total_price)
# return render(request, 'category_products.html', {'products': result,
# 'expensive_price': expensive_price,
# 'cheap_price': cheap_price,
# 'avg_price': avg_price,
# 'total_price': total_price
#        })
