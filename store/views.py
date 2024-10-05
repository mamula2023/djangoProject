import random

from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaulttags import lorem
import faker
import json

categories = ["electronics", "home accessories", "clothing", "books", "groceries"]


# Create your views here.
def index(request):
    result = {"count": 245,
              "categories": categories
              }

    return HttpResponse(json.dumps(result))


def item(request, item_id):
    result = {}
    fake = faker.Faker()
    result["price"] = fake.pricetag()
    result["category"] = random.choice(categories)
    result["item"] = fake.word()
    return HttpResponse(json.dumps(result))
