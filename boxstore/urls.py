from django.urls import path
from .views import BoxList, BoxDetail, MyBoxList, BoxDelete

urlpatterns = [
    path('boxes/', BoxList.as_view(), name='box-list'),
    path('boxes/<int:pk>', BoxDetail.as_view(), name='box-detail'),
    path('my-boxes/', MyBoxList.as_view(), name='my-box-list'),
    path('boxes/<int:pk>/delete/', BoxDelete.as_view(), name='box-delete'),
]
