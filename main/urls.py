from django.urls import path
from . import views
from .views import *
from django.urls import path
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('address', views.address, name='address'),
    path('admin/main', views.index, name='admin'),
    path('item/<slug:item_slug>/', ShowItem.as_view(), name='detail'),
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
    path('cart/', CartView.as_view(), name="cart"),
    path('saveorder/', saveorder, name="saveorder"),
    path('payment/', payment, name='payment')

]
