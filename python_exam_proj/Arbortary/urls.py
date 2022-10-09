from django.urls import path 
from . import views

urlpatterns = [
    path('', views.login),  
    path('register/',views.register),
    path('dashboard/',views.dashboard),
    path('user/account/',views.account),
    path('show/<int:id>/',views.show_it),
    path('edit/<int:id>/',views.edit_it),
    path('new/tree/',views.newtree),
    path('delete/<int:id>/',views.delete_tree),
    path('give_like/<int:id>/',views.give_like)

]