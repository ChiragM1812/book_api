from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random, string

from rest_framework.pagination import PageNumberPagination
from django.db import transaction

class BookListPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        paginator = BookListPagination()
        with transaction.atomic():
            books = Book.objects.all()
            result_page = paginator.paginate_queryset(books, request, view=None)
            serializer = BookSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        paginator = BookListPagination()
        
        with transaction.atomic():
            serializer = BookSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            books = serializer.save()
            result_page = paginator.paginate_queryset(books, request, view=None)
            return paginator.get_paginated_response(serializer.data)
    return paginator.get_paginated_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def book_search(request, title):
    books = Book.objects.filter(title__icontains=title)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def review_search(request, name):
    reviews = Review.objects.filter(name__icontains=name)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def create_reviews(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        reviews = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'Invalid request method'})