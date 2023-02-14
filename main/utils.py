from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        if self.request.user.is_authenticated:
            orders = self.request.user.orders_set.filter(is_paid=False, is_took=False)
            kolich = 0
            for order in orders:
                for prod in order.articleforord_set.all():
                    kolich += prod.quantity
            context['kolich'] = kolich

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context