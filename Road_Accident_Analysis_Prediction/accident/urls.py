from django.urls import path
from . import views
urlpatterns = [
    path('', views.analysis,name="analysis"),
    path('prediction/', views.predict,name='prediction'),
    path('evaluation/', views.evaluation,name='evaluation')     
 ]