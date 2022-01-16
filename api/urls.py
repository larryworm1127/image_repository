from django.urls import path

from api import views

urlpatterns = [
    path('images', views.AddImage.as_view(), name="add_image"),
    path('images/<int:image_id>', views.GetImage.as_view(), name="get_image"),
    path('images/tag', views.TagSearch.as_view(), name="tag_search"),
]
