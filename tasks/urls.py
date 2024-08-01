from . import views    
from django.urls import path

urlpatterns = [ 
    path('',views.index, name='InterfazPrediccion'),
    path('',views.index1, name='InterfazCiclos'),
    path('get_chart/', views.get_chart, name='get_chart'),
    path('get_chart1/', views.get_chart1, name='get_chart1'),
    path('get_chart2/', views.get_chart2, name='get_chart2'),
    path('get_chart3/', views.get_chart1, name='get_chart3'),
    path('get_chart4/', views.get_chart2, name='get_chart4'),
    path('get_chart5/', views.get_chart1, name='get_chart5'),
    path('get_chart6/', views.get_chart2, name='get_chart6'),
    path('get_chart7/', views.get_chart1, name='get_chart7'),
    path('get_chart8/', views.get_chart2, name='get_chart8'),
    path('get_chart9/', views.get_chart1, name='get_chart9')
]