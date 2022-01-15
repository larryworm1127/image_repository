from django.urls import path

from api import views

urlpatterns = [
    path('images', views.AddImage.as_view()),
    path('images/<int:image_id>', views.GetImage.as_view()),
    path('images/tag/<str:tag>', views.TagSearch.as_view()),
]
