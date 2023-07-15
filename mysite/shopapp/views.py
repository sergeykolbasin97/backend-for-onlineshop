import logging
from csv import DictWriter
from timeit import default_timer

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.decorators import action

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from .forms import OrderForm, GroupForm
from .models import Product, Order
from .serializers import ProductSerialize, OrderSerialize

log = logging.getLogger(__name__)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            'items': 1,
        }
        # log.info('Тестовый лог %s', products)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "groups": Group.objects.prefetch_related('permissions').all(),
            'form': GroupForm()
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialize


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerialize
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]
    search_fields = [
        "name",
        "price",
        "description",
        "discount",
        "created_at",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "description",
        "discount",
        "created_at",
        "archived",
    ]

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount'
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'created_by', 'preview'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerialize


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerialize
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]
    filterset_fields = [
        'delivery_address',
        'promocode',
        'created_at',
        'user',
        'products'
    ]


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    context_object_name = 'order'


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    context_object_name = 'orders'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_detail',
            kwargs={'pk': self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class TestingView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'я': 'мыслю', 'следовательно': 'существую'})


class OrderDataExport(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.id,
                'products': [
                    [
                        product.id,
                        product.name
                    ]
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})

class LatestProductsFeed(Feed):
    title = 'Последние продукты'
    description = 'Последние 5 продуктов, добавленных на сайте'
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return (
            Product.objects
            .filter(archived__isnull=False)
            .order_by('-created_at')
            .select_related("created_by")
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:100]

class UserOrdersListView(UserPassesTestMixin, ListView):

    def test_func(self):
        return self.request.user.is_authenticated

    model = Order
    template_name = 'shopapp/user_orders.html'
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    context_object_name = 'user_orders'

    def get_queryset(self):
        self.owner = User.objects.get(pk=self.kwargs['user_id'])
        return Order.objects.filter(user=self.owner)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context

class UserOrdersDataExportJSON(View):
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request: HttpRequest, user_id: int) -> JsonResponse:
        user = get_object_or_404(User, pk=request.user.id)

        if user_id != request.user.id:
            raise Http404("No MyModel matches the given query.")

        cache_key = f'orders_data_export{user.id}'
        orders_data = cache.get(cache_key)

        if orders_data is None:
            orders = Order.objects.order_by('pk').filter(user=user)
            orders_data = [
                {
                    'pk': order.pk,
                    'delivery_address': order.delivery_address,
                    'promocode': order.promocode,
                    'user': order.user.id,
                    'products': [
                        [
                            product.id,
                            product.name
                        ]
                        for product in order.products.all()
                    ]
                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 300)
        return JsonResponse({'orders': orders_data})