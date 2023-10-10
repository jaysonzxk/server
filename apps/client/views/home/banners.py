from rest_framework import serializers

from apps.admin.models import Banners
from apps.utils.json_response import DetailResponse, SuccessResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class BannersSerializer(CustomModelSerializer):
    """
    Banners-序列化器
    """

    class Meta:
        model = Banners
        read_only_fields = ["id"]
        fields = "__all__"


class BannersViewSet(CustomModelViewSet):
    """
    Banners接口
    list:查询
    """

    queryset = Banners.objects.exclude(is_deleted=1).all()
    serializer_class = BannersSerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

