from . import views    
from django.urls import path

urlpatterns = [ 
    path('',views.index, name='InterfazPrediccion'),
    path('get_chart/', views.get_chart, name='get_chart')
]