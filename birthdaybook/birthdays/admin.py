# from django.contrib import admin
#
# from .models import Book
#
# admin.site.register(Book)

from django.contrib import admin
from .models import Book
class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MyModelAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)



admin.site.register(Book, MyModelAdmin)