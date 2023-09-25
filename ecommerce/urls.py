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

    path('wishlist-products/', views.WishlistProductsView.as_view(), name='wishlist-products'),
    path('cart-products/', views.CartView.as_view(), name='cart-products'),
    path('order/', views.OrderCartView.as_view(), name='order-cart'),
    path('order/individual/', views.OrderView.as_view(), name='order-individual'),
]
