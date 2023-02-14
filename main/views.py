from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import Addresses, Orders
from .models import ArticleForOrd
from .models import Flows
from .forms import RegisterUserForm, LoginUserForm
from .utils import DataMixin


def index(request):
    return render(request, 'main/index.html')


def address(request):
    addr = Addresses.objects.all()
    return render(request, 'main/address.html', {'title': "Адреса", 'addr': addr})


class IndexView(DataMixin, ListView):
    model = Flows
    template_name = "main/index.html"
    context_object_name = 'flows'

    def get_context_data(self, *, object_list=None, **kwargs):
        price = [0, 0, 0, 0, 0, 0]
        context = super().get_context_data(**kwargs)
        first6 = Flows.objects.filter(quantity__gte=1, is_published=True)
        c_def = self.get_user_context(title="Главная страница", first6=first6, price=price)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Flows.objects.filter(
            quantity__gte=1, is_published=True
        ).order_by('-time_update')


class ShowItem(DataMixin, DetailView):
    model = Flows

    template_name = 'main/item.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница", )
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class CartView(DataMixin, ListView):
    model = Flows
    template_name = 'main/cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ord = Orders.objects.get(user=self.request.user, is_paid=False)
        elements = user_ord.articleforord_set.all()
        money = 0
        for el in elements:
                money += el.flows.price * el.quantity
        c_def = self.get_user_context(title="Авторизация", elements=elements, money=money)
        return dict(list(context.items()) + list(c_def.items()))


def saveorder(request):
    quant = request.POST['quantity']
    prod = Flows.objects.get(slug=request.POST['prod'])
    order = request.user.orders_set.order_by('date').last()

    if not order or order.is_paid:
        order = Orders.objects.create(user=request.user)
    else:
        art = order.articleforord_set.filter(flows__slug=prod.slug).last()
        if art:
            quant1 = int(quant) + art.quantity
            if quant1 > prod.quantity:
                return already(request, "Вы уже добавили в корзину максимальное количество данного товара")
            art.quantity = quant1
            art.save()
            return redirect('detail', item_slug=prod.slug)
    element = ArticleForOrd.objects.create(flows=prod, order=order, quantity=quant)
    element.save()
    return redirect('detail', item_slug=prod.slug)


def payment(request):
    ord = request.user.orders_set.get(user=request.user, is_paid=False)
    flow = ord.articleforord_set.all()
    for cl in flow:
        cl.flows.quantity -= cl.quantity
        cl.flows.save()
    ord.is_paid = True
    ord.save()
    return redirect('home')


def already(request, str):
    context = {'exeption': str, }
    return render(request, 'main/mistake.html', context)


