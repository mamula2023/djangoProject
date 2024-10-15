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
    """
    displays all categories that have no parent category -> are top level categories

    First, all category objects are loaded here and then
    categories with parents are filtered in template file (category_listing.html)
    """
    cats = Category.objects.all()

    return render(request, 'category_listing.html', {'categories': cats.values()})


def category_products(request, category_id):
    """
    list all products in category and its subcategories

    does it job by
    1. fetching all categories with prefetched products
    2. in bfs-like algorithm getting all categories that are descendants category_id
    3. for each category in bfs, all unique products are processed

    Because products are not in single dataset, I could not use aggregators and annotations and
    calculated statistics manually
    """
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
            prods = child.products.all()
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

    if len(result) <= 0:
        most_expensive = "NaN"
        cheapest = "NaN"
        total_price = "NaN"
        total_value = "NaN"
    else:
        total_price = total_price / len(result)

    return render(request, 'category_products.html',
                  {'products': result,
                   'most_expensive': most_expensive,
                   'cheapest': cheapest,
                   'total_value': total_value,
                   'avg_price': total_price
                   }

                  )


def product(request, product_id):
    """
    displays all data for particular product
    if product does not have image, default no-image.jpg is shown
    """
    prod = Product.objects.get(id=product_id)
    return render(request, 'product_page.html', {'product': prod})
