from django.urls import path
from .views import FoodsList, FoodsDetail

urlpatterns = [
    path('', FoodsList.as_view(), name='foods_list'),
    path('<int:pk>/', FoodsDetail.as_view(), name='foods_detail'),
]