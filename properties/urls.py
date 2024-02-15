from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('property', views.property),
    path('update_property', views.update_property),
    path('delete_property', views.delete_property),
    path('unit', views.unit),
    path('update_unit', views.update_unit),
    path('delete_unit', views.delete_unit),
    path('tenant', views.tenant),
    path('update_tenant', views.update_tenant),
    path('delete_tenant', views.delete_tenant),
    path('agreement', views.agreement),
    path('delete_agreement', views.delete_agreement),
    path('get_units/<int:property_id>/', views.get_units),
    path('tenant_profile', views.tenant_profile),
]