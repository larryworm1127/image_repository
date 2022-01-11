from django.urls import path

from api import views

urlpatterns = [
    path('images', views.add_image),
    path('images/<int:image_id>', views.ImageDetail.as_view())
]
