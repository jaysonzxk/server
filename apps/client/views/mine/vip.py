from rest_framework.decorators import action
from rest_framework.request import Request

from apps.admin.models import VipCard
from apps.utils.json_response import DetailResponse, SuccessResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.viewset import CustomModelViewSet


class VipCardSerializer(CustomModelSerializer):
    """
    VipCard-序列化器
    """

    class Meta:
        model = VipCard
        read_only_fields = ["id"]
        fields = "__all__"


class VipCardViewSet(CustomModelViewSet):
    """
    VipCard接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = VipCard.objects.exclude(is_deleted=1).exclude(status=1).all()
    serializer_class = VipCardSerializer
    authentication_classes = []
    permission_classes = []
    ordering = "-create_datetime"

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[])
    def getDetails(self, request: Request, *args, **kwargs):
        """获取商品详情"""
        goodsId = request.query_params
        goodsDetails = self.queryset.filter(id=goodsId).first()
        result = {
            "id": goodsDetails.id,
            "name": goodsDetails.name,
            "duration": goodsDetails.duration,
            "user_type": goodsDetails.user_type,
            "gender": goodsDetails.gender,
            "email": goodsDetails.email,
        }

        return DetailResponse()
