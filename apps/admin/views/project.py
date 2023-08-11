from rest_framework import serializers

from apps.admin.models import Project
from apps.utils.json_response import DetailResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class ProjectSerializer(CustomModelSerializer):
    """
    Project-序列化器
    """

    class Meta:
        model = Project
        read_only_fields = ["id"]
        fields = "__all__"


class ProjectCreateSerializer(CustomModelSerializer):
    """
    Project新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=Project.objects.all(), message="名称必须唯一")
        ],
    )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["id"]


class ProjectUpdateSerializer(CustomModelSerializer):
    """
    修改Project-序列化器
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
        model = Project
        read_only_fields = ["id"]
        fields = "__all__"


class ProjectInfoUpdateSerializer(CustomModelSerializer):
    """
    Project修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectViewSet(CustomModelViewSet):
    """
    Banners接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Project.objects.exclude(is_deleted=1).all()
    serializer_class = ProjectSerializer
    create_serializer_class = ProjectCreateSerializer
    update_serializer_class = ProjectUpdateSerializer

