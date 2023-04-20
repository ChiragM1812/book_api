from django.db import models
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    min_age = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.book.title