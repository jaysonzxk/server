from django.urls import path
from rest_framework import routers

from apps.admin.views.api_white_list import ApiWhiteListViewSet
from apps.admin.views.area import AreaViewSet
from apps.admin.views.banners import BannersViewSet
from apps.admin.views.clause import PrivacyView, TermsServiceView
from apps.admin.views.datav import DataVViewSet
from apps.admin.views.dept import DeptViewSet
from apps.admin.views.dictionary import DictionaryViewSet
from apps.admin.views.file_list import FileViewSet
from apps.admin.views.login_log import LoginLogViewSet
from apps.admin.views.marquee import MarqueeViewSet
from apps.admin.views.master import MasterViewSet
from apps.admin.views.master_check_in import MasterCheckInViewSet
from apps.admin.views.master_project import MasterProjectViewSet
from apps.admin.views.menu import MenuViewSet
from apps.admin.views.menu_button import MenuButtonViewSet
from apps.admin.views.message_center import MessageCenterViewSet
from apps.admin.views.notice import NoticeViewSet
from apps.admin.views.operation_log import OperationLogViewSet
from apps.admin.views.pay_channel import PayChannelViewSet
from apps.admin.views.pay_order import PayOrderViewSet
from apps.admin.views.project import ProjectViewSet
from apps.admin.views.role import RoleViewSet
from apps.admin.views.service_order import ServiceOrderViewSet
from apps.admin.views.system_config import SystemConfigViewSet
from apps.admin.views.user import UserViewSet
from apps.admin.views.member import MemberViewSet
from apps.admin.views.vip import VipViewSet, UserVipViewSet
from apps.admin.views.userAddr import UserAddrViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'member', MemberViewSet)
system_url.register(r'master', MasterViewSet)
system_url.register(r'masterProject', MasterProjectViewSet)
system_url.register(r'vip', VipViewSet)
system_url.register(r'user_vip', UserVipViewSet)
system_url.register(r'user_addr', UserAddrViewSet)
system_url.register(r'banners', BannersViewSet)
system_url.register(r'notice', NoticeViewSet)
system_url.register(r'marquee', MarqueeViewSet)
system_url.register(r'project', ProjectViewSet)
system_url.register(r'masterCheckIn', MasterCheckInViewSet)
system_url.register(r'payChannel', PayChannelViewSet)
system_url.register(r'payOrder', PayOrderViewSet)
system_url.register(r'serviceOrder', ServiceOrderViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'area', AreaViewSet)
system_url.register(r'file', FileViewSet)
system_url.register(r'api_white_list', ApiWhiteListViewSet)
system_url.register(r'system_config', SystemConfigViewSet)
system_url.register(r'message_center', MessageCenterViewSet)
system_url.register(r'datav', DataVViewSet)

urlpatterns = [
    path('system_config/save_content/', SystemConfigViewSet.as_view({'put': 'save_content'})),
    path('system_config/get_association_table/', SystemConfigViewSet.as_view({'get': 'get_association_table'})),
    path('system_config/get_table_data/<int:pk>/', SystemConfigViewSet.as_view({'get': 'get_table_data'})),
    path('system_config/get_relation_info/', SystemConfigViewSet.as_view({'get': 'get_relation_info'})),
    path('login_log/', LoginLogViewSet.as_view({'get': 'list'})),
    path('login_log/<int:pk>/', LoginLogViewSet.as_view({'get': 'retrieve'})),
    path('dept_lazy_tree/', DeptViewSet.as_view({'get': 'dept_lazy_tree'})),
    path('clause/privacy.html', PrivacyView.as_view()),
    path('clause/terms_service.html', TermsServiceView.as_view()),
]
urlpatterns += system_url.urls
