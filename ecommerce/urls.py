from django.urls import path,include
from . import views

urlpatterns = [
    path('parent-category/', views.ParentCategoryView.as_view(), name='parent-category'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category-meta-data/', views.CategoryMetaDataFieldView.as_view(), name='category-meta-data'),
    path('category-meta-data-value/', views.CategoryMetaDataValueView.as_view(), name='category-meta-data-value'),
    path('category-meta-data-value/<int:id>/', views.CategoryMetaDataValueDetailView.as_view(), name='category-meta-data-value-detail'),

    path('product/', views.ProductView.as_view(), name='product'),
    path('product/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product-variation/', views.ProductVariationView.as_view(), name='product-variation'),
    path('product-variation/<int:id>/', views.ProductVariationDetailView.as_view(), name='product-variation-detail'),
    path('product-review/', views.ProductReviewView.as_view(), name='product-review'),
    path('product-review/<int:id>/', views.ProductReviewDetailView.as_view(), name='product-review'),
]
