from rest_framework import serializers

from apps.admin.models import UserAddr
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class UserAddrSerializer(CustomModelSerializer):
    """
    用户地址商品-序列化器
    """
    username = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = UserAddr
        read_only_fields = ["id"]
        fields = "__all__"


class UserAddrCreateSerializer(CustomModelSerializer):
    """
    用户地址商品新增-序列化器
    """
    addr = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=UserAddr.objects.all(), message="地址已存在")
        ],
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = UserAddr
        fields = "__all__"
        read_only_fields = ["id"]


class UserAddrUpdateSerializer(CustomModelSerializer):
    """
    用户地址商品-序列化器
    """

    addr = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=UserAddr.objects.all(), message="地址已存在")
        ],
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = UserAddr
        read_only_fields = ["id"]
        fields = "__all__"


class UserAddrInfoUpdateSerializer(CustomModelSerializer):
    """
    用户地址修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = UserAddr
        fields = "__all__"


class UserAddrViewSet(CustomModelViewSet):
    """
    用户地址接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = UserAddr.objects.exclude(is_deleted=1).all()
    serializer_class = UserAddrSerializer
    create_serializer_class = UserAddrCreateSerializer
    update_serializer_class = UserAddrUpdateSerializer
    filter_fields = '__all__'
