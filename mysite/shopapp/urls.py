from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ShopIndexView,
                    GroupsListView,
                    ProductDetailsView,
                    ProductListView,
                    ProductListAPIView,
                    OrderListAPIView,
                    OrderViewSet,
                    OrdersListView,
                    OrderDetailsView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    ProductViewSet,
                    OrderCreateView,
                    OrderUpdateView,
                    OrderDeleteView,
                    TestingView,
                    OrderDataExport,
                    LatestProductsFeed,
                    UserOrdersListView,
                    UserOrdersDataExportJSON)

app_name = "shopapp"

routers = DefaultRouter()
routers.register('products', ProductViewSet)

routers2 = DefaultRouter()
routers2.register('orders', OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/api", ProductListAPIView.as_view(), name="products_api"),
    path("products/api2", include(routers.urls)),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived/", ProductDeleteView.as_view(), name="product_archived"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/api", OrderListAPIView.as_view(), name="orders_api"),
    path("orders/api2", include(routers2.urls)),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_detail"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/orders-export/", OrderDataExport.as_view(), name="orders_export"),
    path("users/<int:user_id>/orders/export/", UserOrdersDataExportJSON.as_view(), name="user_orders"),
    path("test", TestingView.as_view(), name="test"),
    path("products/latest/feed", LatestProductsFeed(), name="blogs_feed"),

]
#handler404 = "django_404_project.views.page_not_found_view"
