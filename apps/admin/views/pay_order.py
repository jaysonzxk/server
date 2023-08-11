from rest_framework import serializers

from apps.admin.models import PayOrder
from apps.admin.views.master_project import MasterProjectSerializer
from apps.admin.views.pay_channel import PayChannelSerializer
from apps.admin.views.user import UserSerializer
from apps.utils.json_response import DetailResponse, ErrorResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class PayOrderSerializer(CustomModelSerializer):
    """
    PayOrder-序列化器
    """
    masterProject = MasterProjectSerializer()
    payChannel = PayChannelSerializer()

    class Meta:
        model = PayOrder
        read_only_fields = ["id"]
        fields = "__all__"


class PayOrderCreateSerializer(CustomModelSerializer):
    """
    PayOrder新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=PayOrder.objects.all(), message="名称必须唯一")
        ],
    )

    # def save(self, **kwargs):
    #     data = super().save(**kwargs)
    #     # data.dept_belong_id = data.dept_id
    #     data.save()
    #     # data.post.set(self.initial_data.get("post", []))
    #     return data

    class Meta:
        model = PayOrder
        fields = "__all__"
        read_only_fields = ["id"]


class PayOrderUpdateSerializer(CustomModelSerializer):
    """
    修改PayOrder-序列化器
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
        model = PayOrder
        read_only_fields = ["id"]
        fields = "__all__"


class PayOrderInfoUpdateSerializer(CustomModelSerializer):
    """
    MasterCheckIn修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = PayOrder
        fields = "__all__"


class PayOrderViewSet(CustomModelViewSet):
    """
    PayOrder接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = PayOrder.objects.exclude(is_deleted=1).all()
    serializer_class = PayOrderSerializer
    create_serializer_class = PayOrderCreateSerializer
    update_serializer_class = PayOrderUpdateSerializer
