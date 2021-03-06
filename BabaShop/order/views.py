from django.contrib import messages
from django.db.models.aggregates import Count, Max, Sum
from django.views.generic import DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
from myuser.auth import LoginRequiredMixin, PhoneVerifyRequiredMixin
from django.views.generic.base import View
from order.Filters import OrderFilter
from order.models import OrderItem
from django.shortcuts import redirect
from shop.models import Shop, Product
from order.models import Order


# Create your views here.


class OrderList(LoginRequiredMixin, PhoneVerifyRequiredMixin, DetailView):
    """
    Render list of orders that are put by customers.
    This list belongs to a specific shop of a supplier.
    """
    template_name = 'order/order_list.html'
    login_url = '/myuser/supplier_login/'
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')          
        context['filter'] = OrderFilter(self.request.GET, queryset=Order.objects.filter(
            orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at'))

        return context


class ProductList(LoginRequiredMixin, PhoneVerifyRequiredMixin, DetailView):
    """
    Render list of products that are defined.
    This list belongs to a specific shop of a supplier.
    """
    template_name = 'order/product_list.html'
    login_url = '/myuser/supplier_login/'
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        context['product_list'] = Product.objects.filter(shop=context['shop'])

        return context


class OrderDetail(LoginRequiredMixin, PhoneVerifyRequiredMixin, DetailView):
    """
    Render list of items of an order and details of that order.
    This list belongs to an order in a specific shop.
    """
    template_name = 'order/order_detail.html'
    login_url = '/myuser/supplier_login/'
    model = Order

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        context['order_list'] = Order.objects.filter(id=self.kwargs['id'], orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at')
        context['orderitem_list'] = OrderItem.objects.filter(order_id=self.kwargs['id'], product__shop__slug=self.kwargs['slug'])
        # check admin order total price bug when change it manualy
        return context


class OrderEditstatus(LoginRequiredMixin, PhoneVerifyRequiredMixin, View):
    login_url = '/myuser/supplier_login/'
    model = Order

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.filter(pk=self.kwargs['pk'])
        obj = Order.objects.filter(pk=self.kwargs['pk']).first()
        if obj.status == 'CHECKING':
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CONFIRMED')
        elif obj.status == 'CANCELED':
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CHECKING')
        else:
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CANCELED')
            messages.error(request, f"The order NO. {obj.id} is Canceled." )
        return redirect('order_list_url', self.kwargs['slug'])


class CustomerList(LoginRequiredMixin, PhoneVerifyRequiredMixin, DetailView):
    """
    Render list of customers and their orders data.
    This customers list belongs to a specific shop.
    """
    template_name = 'order/customer_list.html'
    login_url = '/myuser/supplier_login/'
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        context['customer_order'] = Order.objects.filter(shop=context['shop']
                ).values('customer', 'customer__phone', 'customer__image', 'customer__username').annotate(
                                                                        last_order=Max('created_at'),
                                                                        order_count=Count('id'),
                                                                        purchase_price=Sum('total_price'),
                                                                        purchase_quantity=Sum('total_quantity')
                                                                        ).order_by()
        return context


class OrderChart(LoginRequiredMixin, PhoneVerifyRequiredMixin, DetailView):
    template_name = 'order/chart.html'
    login_url = '/myuser/supplier_login/'
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.Undeleted.filter(slug=self.kwargs['slug'], supplier=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.Undeleted.filter(supplier=self.request.user).order_by('id')
        context['chart_data'] = Order.objects.filter(shop=context['shop']
                ).values('customer__username').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by()
        context['barchart_data'] = Order.objects.filter(shop=context['shop']
                ).values('created_at__date').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by('created_at__date')
        context['barchart_data2'] = Order.objects.filter(shop=context['shop']
                ).values('created_at__month').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by('created_at__month')
        context['barchart_data3'] = Order.objects.filter(shop=context['shop']
                ).values('created_at__year').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by('created_at__year')
        return context
