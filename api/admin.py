from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class BookAdmin(admin.ModelAdmin):
    form = BookForm

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Review, ReviewAdmin)