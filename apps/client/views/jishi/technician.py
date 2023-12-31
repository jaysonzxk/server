import time

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.request import Request

from apps.admin.models import Users, MasterProject
from apps.admin.views.master_project import MasterProjectSerializer
from apps.utils.authentication import RedisOpAuthJwtAuthentication, OpAuthJwtAuthentication
from apps.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from apps.utils.serializers import CustomModelSerializer
from apps.utils.viewset import CustomModelViewSet


class TechnicianSerializer(CustomModelSerializer):
    """
    Technician-序列化器
    """

    class Meta:
        model = Users
        read_only_fields = ["id"]
        exclude = ["password"]
        # fields = "__all__"


class TechnicianViewSet(CustomModelViewSet):
    """
    技师接口
    list:查询
    """

    queryset = Users.objects.exclude(is_deleted=1).filter(user_type=2).all()
    serializer_class = TechnicianSerializer
    authentication_classes = []
    permission_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[], authentication_classes=[])
    def getRecommend(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.filter(isRecommend=1).all()
            serializer = self.get_serializer(queryset, many=True, request=request)
        except Exception as e:
            return ErrorResponse(msg='参数错误')
        return DetailResponse(data=serializer.data)

    # @action(methods=["GET"], detail=False, permission_classes=[], authentication_classes=[])
    def get_master_goods(self, request: Request, *args, **kwargs):
        self.authentication_classes = [RedisOpAuthJwtAuthentication().authenticate(request=request)]
        data = request.query_params
        try:
            goods = MasterProject.objects.filter(user_id=data.get('userId')).filter(is_deleted=0).all()
            serializer = MasterProjectSerializer(goods, many=True, request=request)
        except Exception as e:
            return ErrorResponse(msg='参数错误')
        # print(serializer.data)
        return DetailResponse(data=serializer.data)

    @action(methods=["GET"], detail=False, permission_classes=[], authentication_classes=[])
    def getMasterInfo(self, request: Request, *args, **kwargs):
        """技师详情信息"""
        masterGoodsList = []
        userId = request.query_params.get('userId')
        userObj = self.queryset.filter(id=userId).first()
        masterGoodsObj = MasterProject.objects.filter(user_id=userId).all()
        for i in masterGoodsObj:
            goods = {'id': i.project.id, 'name': i.project.name, 'price': i.project.price,
                     'duration': i.project.duration, 'img': i.project.img}
            masterGoodsList.append(goods)
        result = {
            "id": userObj.id,
            "name": userObj.name,
            "user_type": userObj.user_type,
            "gender": userObj.gender,
            "age": userObj.age,
            "starLevel": userObj.starLevel,
            "avatar": userObj.avatar,
            "orderNum": userObj.orderNum,
            "masterGoods": masterGoodsList
        }

        return DetailResponse(data=result)
