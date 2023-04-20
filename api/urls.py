from django.urls import path
from .views import book_list, book_detail, review_list, review_detail, book_search, review_search, create_reviews

urlpatterns = [
    path('books', book_list, name='book-list'),
    path('books/<int:pk>', book_detail, name='book-detail'),
    path('books/search/<str:title>', book_search, name='book-search'),
    path('reviews', review_list, name='review-list'),
    path('reviews/<int:pk>', review_detail, name='review-detail'),
    path('reviews/search/<str:name>', review_search, name='review-search'),
]