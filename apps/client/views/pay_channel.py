from rest_framework import serializers

from apps.admin.models import PayChannel
from apps.admin.views.user import UserSerializer
from apps.utils.json_response import DetailResponse, ErrorResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class PayChannelSerializer(CustomModelSerializer):
    """
    PayChannel-序列化器
    """
    # user = UserSerializer()

    class Meta:
        model = PayChannel
        read_only_fields = ["id"]
        fields = "__all__"


class PayChannelCreateSerializer(CustomModelSerializer):
    """
    PayChannel新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=PayChannel.objects.all(), message="名称必须唯一")
        ],
    )

    # def save(self, **kwargs):
    #     data = super().save(**kwargs)
    #     # data.dept_belong_id = data.dept_id
    #     data.save()
    #     # data.post.set(self.initial_data.get("post", []))
    #     return data

    class Meta:
        model = PayChannel
        fields = "__all__"
        read_only_fields = ["id"]


class PayChannelUpdateSerializer(CustomModelSerializer):
    """
    修改PayChannel-序列化器
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
        model = PayChannel
        read_only_fields = ["id"]
        fields = "__all__"


class PayChannelInfoUpdateSerializer(CustomModelSerializer):
    """
    PayChannel修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = PayChannel
        fields = "__all__"


class PayChannelViewSet(CustomModelViewSet):
    """
    PayChannel接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = PayChannel.objects.exclude(is_deleted=1).exclude(status=1).all()
    serializer_class = PayChannelSerializer
    create_serializer_class = PayChannelCreateSerializer
    update_serializer_class = PayChannelUpdateSerializer
    authentication_classes = []
    permission_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return DetailResponse(data=serializer.data, msg="获取成功")

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
