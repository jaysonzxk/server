from rest_framework import serializers

from apps.admin.models import Banners
from apps.utils.json_response import DetailResponse
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


class BannersCreateSerializer(CustomModelSerializer):
    """
    Banners新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=Banners.objects.all(), message="名称必须唯一")
        ],
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = Banners
        fields = "__all__"
        read_only_fields = ["id"]


class BannersUpdateSerializer(CustomModelSerializer):
    """
    修改Banners-序列化器
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
        model = Banners
        read_only_fields = ["id"]
        fields = "__all__"


class BannersInfoUpdateSerializer(CustomModelSerializer):
    """
    Banners修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Banners
        fields = "__all__"


class BannersViewSet(CustomModelViewSet):
    """
    Banners接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Banners.objects.exclude(is_deleted=1).all()
    serializer_class = BannersSerializer
    create_serializer_class = BannersCreateSerializer
    update_serializer_class = BannersUpdateSerializer

