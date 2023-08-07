from rest_framework import serializers

from apps.client.models import VipCard
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class VipSerializer(CustomModelSerializer):
    """
    vip商品-序列化器
    """

    class Meta:
        model = VipCard
        read_only_fields = ["id"]
        fields = "__all__"


class VipCreateSerializer(CustomModelSerializer):
    """
    vip商品新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=VipCard.objects.all(), message="名称必须唯一")
        ],
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = VipCard
        fields = "__all__"
        read_only_fields = ["id"]


class VipUpdateSerializer(CustomModelSerializer):
    """
    修改vip商品-序列化器
    """

    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=VipCard.objects.all(), message="商品已存在")
        ],
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = VipCard
        read_only_fields = ["id"]
        fields = "__all__"


class VipInfoUpdateSerializer(CustomModelSerializer):
    """
    会员修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = VipCard
        fields = "__all__"


class VipViewSet(CustomModelViewSet):
    """
    vip商品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = VipCard.objects.exclude(is_deleted=1).all()
    serializer_class = VipSerializer
    create_serializer_class = VipCreateSerializer
    update_serializer_class = VipUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    filter_fields = {
        "name": ["icontains"],
        "sort": ["icontains"],
        "discount": ["icontains"],
        "amount": ["icontains"],
        "status": ["icontains"],
    }
    ordering = "sort"
