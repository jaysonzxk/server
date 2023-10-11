from django.urls import path
from rest_framework import routers

from apps.client.views.home.banners import BannersViewSet
from apps.client.views.home.goods import GoodsViewSet
from apps.client.views.pay.pay import PayMoneyViewSet
from apps.client.views.pay.pay_channel import PayChannelViewSet
from apps.client.views.jishi.technician import TechnicianViewSet
from apps.client.views.mine.user import UserViewSet
from apps.client.views.mine.vip import VipCardViewSet

system_url = routers.SimpleRouter()
system_url.register(r'user', UserViewSet)
system_url.register(r'banners', BannersViewSet)
system_url.register(r'goods', GoodsViewSet)
system_url.register(r'technician', TechnicianViewSet)
system_url.register(r'vipList', VipCardViewSet)
system_url.register(r'payChannel', PayChannelViewSet)
system_url.register(r'pay', PayMoneyViewSet, basename='pay')

urlpatterns = [
    path('technician/getMasterGoods/', TechnicianViewSet.as_view({'get': 'get_master_goods'})),
    path('payMoney/pay/', PayMoneyViewSet.as_view({'post': 'pay'})),
    # path('system_config/get_association_table/', SystemConfigViewSet.as_view({'get': 'get_association_table'})),
    # path('system_config/get_table_data/<int:pk>/', SystemConfigViewSet.as_view({'get': 'get_table_data'})),
    # path('system_config/get_relation_info/', SystemConfigViewSet.as_view({'get': 'get_relation_info'})),
    # path('login_log/', LoginLogViewSet.as_view({'get': 'list'})),
    # path('login_log/<int:pk>/', LoginLogViewSet.as_view({'get': 'retrieve'})),
    # path('dept_lazy_tree/', DeptViewSet.as_view({'get': 'dept_lazy_tree'})),
    # path('clause/privacy.html', PrivacyView.as_view()),
    # path('clause/terms_service.html', TermsServiceView.as_view()),
]
urlpatterns += system_url.urls
