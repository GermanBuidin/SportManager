from django.shortcuts import render
from models import ETennis

q = ETennis.sku.all()
for i in q[:1]:
    print(i)

# Create your views here.
