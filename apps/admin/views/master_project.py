from rest_framework import serializers

from apps.admin.models import MasterProject
from apps.admin.views.project import ProjectSerializer
from apps.admin.views.user import UserSerializer
from apps.utils.json_response import DetailResponse, ErrorResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class MasterProjectSerializer(CustomModelSerializer):
    """
    MasterCheckIn-序列化器
    """
    user = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = MasterProject
        read_only_fields = ["id"]
        fields = "__all__"


class MasterProjectCreateSerializer(CustomModelSerializer):
    """
    MasterProject新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=MasterProject.objects.all(), message="名称必须唯一")
        ],
    )

    # def save(self, **kwargs):
    #     data = super().save(**kwargs)
    #     # data.dept_belong_id = data.dept_id
    #     data.save()
    #     # data.post.set(self.initial_data.get("post", []))
    #     return data

    class Meta:
        model = MasterProject
        fields = "__all__"
        read_only_fields = ["id"]


class MasterProjectUpdateSerializer(CustomModelSerializer):
    """
    修改MasterProject-序列化器
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
        model = MasterProject
        read_only_fields = ["id"]
        fields = "__all__"


class MasterProjectInfoUpdateSerializer(CustomModelSerializer):
    """
    MasterProject修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = MasterProject
        fields = "__all__"


class MasterProjectViewSet(CustomModelViewSet):
    """
    MasterProject接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = MasterProject.objects.exclude(is_deleted=1).all()
    serializer_class = MasterProjectSerializer
    create_serializer_class = MasterProjectCreateSerializer
    update_serializer_class = MasterProjectUpdateSerializer
