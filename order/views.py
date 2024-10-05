import json
import random
from django.http import HttpResponse
import faker

order_history = []
# Create your views here.
def index(request, order_id):
    result = {"items": [], "total": 0}
    fake = faker.Faker()
    n_items = random.randint(1, 5)
    total = 0
    for i in range(n_items):
        item = fake.word()
        price = float(fake.pricetag().replace('$', '').replace(',', ''))
        quantity = random.randint(1, 10)
        item_total = price*quantity

        result["items"].append({"item": item,
                                "price": price,
                                "quantity": quantity,
                                "total": item_total})
        total += item_total
    result["total"] = total
    order_history.append(result)
    return HttpResponse(json.dumps(result))


def history(request):
    return HttpResponse(json.dumps(order_history))
