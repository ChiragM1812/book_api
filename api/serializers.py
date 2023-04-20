from rest_framework import serializers
from .models import Book, Author, Language, Genre, Publisher,Review

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'address']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    language = LanguageSerializer()
    genre = GenreSerializer()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ['title', 'author', 'language', 'genre', 'publisher', 'min_age', 'price', 'stock', 'description']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        language_data = validated_data.pop('language')
        genre_data = validated_data.pop('genre')
        publisher_data = validated_data.pop('publisher')

        
        author = Author.objects.create(**author_data)
        language = Language.objects.create(**language_data)
        genre = Genre.objects.create(**genre_data)
        publisher = Publisher.objects.create(**publisher_data)

        
        book = Book.objects.create(
            author=author,
            language=language,
            genre=genre,
            publisher=publisher,
            **validated_data
        )
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        instance.author = author

        language_data = validated_data.pop('language')
        language, created = Language.objects.get_or_create(**language_data)
        instance.language = language

        genre_data = validated_data.pop('genre')
        genre, created = Genre.objects.get_or_create(**genre_data)
        instance.genre = genre

        publisher_data = validated_data.pop('publisher')
        publisher, created = Publisher.objects.get_or_create(**publisher_data)
        instance.publisher = publisher

        instance.title = validated_data.get('title', instance.title)
        instance.min_age = validated_data.get('min_age', instance.min_age)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance

# class ReviewSerializer(serializers.ModelSerializer):
#     book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
#     book_name = serializers.StringRelatedField(source='book.title')

#     class Meta:
#         model = Review
#         fields = ['id', 'book', 'book_name', 'name', 'email', 'rating', 'comment', 'date_added']

#     def create(self, validated_data):
#         book = validated_data.pop('book')
#         review = Review.objects.create(book=book, **validated_data)
#         return review

#     def update(self, instance, validated_data):
#         book_data = validated_data.pop('book').pk
#         book = Book.objects.get(pk=book_data)
#         instance.book = book

#         instance.name = validated_data.get('name', instance.name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.rating = validated_data.get('rating', instance.rating)
#         instance.comment = validated_data.get('comment', instance.comment)
#         instance.date_added = validated_data.get('date_added', instance.date_added)

#         instance.save()
#         return instance

class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Review
        fields = ['book','name','email','rating','comment','date_added']

    def create(self, validated_data):
        book_data = validated_data.pop('book')
        book_serializer = BookSerializer(data=book_data)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()
        review = Review.objects.create(book=book, **validated_data)
        return review
    
    def update(self, obj, validated_data):  
        book_data = validated_data.pop('book', None)

        obj.name = validated_data.get('name', obj.name)
        obj.email = validated_data.get('email', obj.email)
        obj.rating = validated_data.get('rating', obj.rating)
        obj.comment = validated_data.get('comment', obj.comment)

        book = obj.book
        book.title = book_data.get('title', book.title)
        book.min_age = book_data.get('min_age', book.min_age)
        book.price = book_data.get('price', book.price)
        book.stock = book_data.get('stock', book.stock)
        book.description = book_data.get('description', book.description)

        author_name = book_data.get('author', {}).get('name')
        if author_name:
            author, _ = Author.objects.get_or_create(name=author_name)
            book.author = author

        genre_name = book_data.get('genre', {}).get('name')
        if genre_name:
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            book.genre = genre

        language_name = book_data.get('language', {}).get('name')
        if language_name:
            language, _ = Language.objects.get_or_create(name=language_name)
            book.language = language

        publisher_data = book_data.get('publisher', {})
        if publisher_data:
            publisher_name = publisher_data.get('name')
            publisher_address = publisher_data.get('address')
            if publisher_name:
                publisher, _ = Publisher.objects.get_or_create(name=publisher_name, address=publisher_address)
                book.publisher = publisher

        book.save()
        obj.save()

        return obj