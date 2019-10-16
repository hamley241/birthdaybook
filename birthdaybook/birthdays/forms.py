from django.forms import ModelForm
from .models import Book

class CustomUserCreationForm(ModelForm):

    class Meta:
        model = Book
        fields = ('name', 'birthday')