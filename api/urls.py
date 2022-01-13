from django.urls import path

from api import views

urlpatterns = [
    path('images', views.AddImage.as_view()),
    path('images/<int:image_id>', views.ImageDetail.as_view()),
    path('images/search', views.search)
]
