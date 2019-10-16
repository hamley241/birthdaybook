from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:birthday_id>/', views.delete, name='delete'),
    path('<int:birthday_id>/update', views.update, name='update'),
    path('update/', views.detail, name='update1'),
    path('add/', views.add, name='add'),
]
