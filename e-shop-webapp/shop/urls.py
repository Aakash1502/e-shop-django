from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="shophome"),
    path("about/", views.about, name="aboutus"),
    
    path("Contact/", views.contact, name="contactus"),
    path("Tracker/", views.tracker, name="tracker"),
    path("Checkout/", views.checkout, name="checkout"),
    path("Search/", views.search, name="search"),
    path("products/<int:myid>", views.products, name="prodview"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)