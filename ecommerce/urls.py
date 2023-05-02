from django.urls import path,include
from . import views

urlpatterns = [
    path('parent-category/', views.ParentCategoryView.as_view(), name='parent-category'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category-meta-data/', views.CategoryMetaDataFieldView.as_view(), name='category-meta-data'),
    path('category-meta-data-value/', views.CategoryMetaDataValueView.as_view(), name='category-meta-data-value'),
    path('category-meta-data-value/<int:id>/', views.CategoryMetaDataValueDetailView.as_view(), name='category-meta-data-value-detail'),
]
