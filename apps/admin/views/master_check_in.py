from rest_framework import serializers

from apps.admin.models import MasterCheckIn, Users
from apps.admin.views.user import UserSerializer
from apps.utils.json_response import DetailResponse, ErrorResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomUniqueValidator
from apps.utils.viewset import CustomModelViewSet


class MasterCheckInSerializer(CustomModelSerializer):
    """
    MasterCheckIn-序列化器
    """
    # user = UserSerializer()

    class Meta:
        model = MasterCheckIn
        read_only_fields = ["id"]
        fields = "__all__"


class MasterCheckInCreateSerializer(CustomModelSerializer):
    """
    MasterCheckIn新增-序列化器
    """
    name = serializers.CharField(
        max_length=20,
        validators=[
            CustomUniqueValidator(queryset=MasterCheckIn.objects.all(), message="名称必须唯一")
        ],
    )

    # def save(self, **kwargs):
    #     data = super().save(**kwargs)
    #     # data.dept_belong_id = data.dept_id
    #     data.save()
    #     # data.post.set(self.initial_data.get("post", []))
    #     return data

    class Meta:
        model = MasterCheckIn
        fields = "__all__"
        read_only_fields = ["id"]


class MasterCheckInUpdateSerializer(CustomModelSerializer):
    """
    修改MasterCheckIn-序列化器
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
        model = MasterCheckIn
        read_only_fields = ["id"]
        fields = "__all__"


class MasterCheckInInfoUpdateSerializer(CustomModelSerializer):
    """
    MasterCheckIn修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = MasterCheckIn
        fields = "__all__"


class MasterCheckInViewSet(CustomModelViewSet):
    """
    MasterCheckIn接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = MasterCheckIn.objects.exclude(is_deleted=1).all()
    serializer_class = MasterCheckInSerializer
    create_serializer_class = MasterCheckInCreateSerializer
    update_serializer_class = MasterCheckInUpdateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            user = Users.objects.filter(mobile=data.get('mobile')).first()
        except Exception as e:
            return ErrorResponse(msg='参数错误')
        if data.get('name') != user.name:
            return ErrorResponse(msg='真实姓名错误')
        if user:
            try:
                serializer = self.get_serializer(data=request.data, request=request)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                return DetailResponse(data=serializer.data, msg="新增成功")
            except Exception as e:
                print(e)
                return ErrorResponse(msg='参数错误')
        return ErrorResponse(msg='技师不存在')
