from rest_framework import serializers

from apps.admin.models import ServiceOrder, Project
from apps.admin.views.pay_channel import PayChannelSerializer
from apps.admin.views.pay_order import PayOrderSerializer
from apps.admin.views.project import ProjectSerializer
from apps.admin.views.user import UserSerializer
from apps.admin.views.userAddr import UserAddrSerializer
from apps.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class ServiceOrderSerializer(CustomModelSerializer):
    """
    ServiceOrder-序列化器
    """
    user = UserSerializer()
    project = ProjectSerializer()
    master = UserSerializer()
    payOrder = PayOrderSerializer()
    addr = UserAddrSerializer()

    class Meta:
        model = ServiceOrder
        read_only_fields = ["id"]
        fields = "__all__"


class ServiceOrderCreateSerializer(CustomModelSerializer):
    """
    ServiceOrder新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=ServiceOrder.objects.all(), message="名称必须唯一")
        ],
    )

    # def save(self, **kwargs):
    #     data = super().save(**kwargs)
    #     # data.dept_belong_id = data.dept_id
    #     data.save()
    #     # data.post.set(self.initial_data.get("post", []))
    #     return data

    class Meta:
        model = ServiceOrder
        fields = "__all__"
        read_only_fields = ["id"]


class ServiceOrderUpdateSerializer(CustomModelSerializer):
    """
    修改ServiceOrder-序列化器
    """

    # name = serializers.CharField(
    #     max_length=20,
    #     validators=[
    #         CustomUniqueValidator(queryset=Banners.objects.all(), message="商品已存在")
    #     ],
    # )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = ServiceOrder
        read_only_fields = ["id"]
        fields = "__all__"


class ServiceOrderInfoUpdateSerializer(CustomModelSerializer):
    """
    ServiceOrder修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = ServiceOrder
        fields = "__all__"


class ServiceOrderViewSet(CustomModelViewSet):
    """
    ServiceOrder接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = ServiceOrder.objects.exclude(is_deleted=1).all()
    serializer_class = ServiceOrderSerializer
    create_serializer_class = ServiceOrderCreateSerializer
    update_serializer_class = ServiceOrderUpdateSerializer

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     try:
    #         user = Users.objects.filter(mobile=data.get('mobile')).first()
    #     except Exception as e:
    #         return ErrorResponse(msg='参数错误')
    #     if data.get('name') != user.name:
    #         return ErrorResponse(msg='真实姓名错误')
    #     if user:
    #         try:
    #             serializer = self.get_serializer(data=request.data, request=request)
    #             serializer.is_valid(raise_exception=True)
    #             self.perform_create(serializer)
    #
    #             return DetailResponse(data=serializer.data, msg="新增成功")
    #         except Exception as e:
    #             return ErrorResponse(msg='参数错误')
    #     return ErrorResponse(msg='技师不存在')
    #
    # def update(self, request, *args, **kwargs):
    #     data = request.data
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     if data.get('reviewStatus') == 1:
    #         instance = Users.objects.filter(mobile=data.get('mobile')).first()
    #         instance.isCheckIn = 1
    #         instance.save()
    #     self.perform_update(serializer)
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #     return DetailResponse(data=serializer.data, msg="更新成功")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")
