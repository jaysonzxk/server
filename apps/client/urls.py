from django.urls import path
from rest_framework import routers

from apps.client.views.dept import DeptViewSet
from apps.admin.views.menu import MenuViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)

urlpatterns = [
    # path('system_config/save_content/', SystemConfigViewSet.as_view({'put': 'save_content'})),
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