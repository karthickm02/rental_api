from django.shortcuts import render
from rest_framework import viewsets

from category.models import Category
from category.serializer import CategorySerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
