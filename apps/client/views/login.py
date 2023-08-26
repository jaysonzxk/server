import base64
import binascii
import datetime
import hashlib
import json
import logging
import os
import re
import string
from random import choice
from uuid import uuid4
import calendar
import time

from captcha.models import CaptchaStore
from captcha.views import captcha_image
from channels.auth import login
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_simplejwt.views import TokenRefreshView

from application.settings import REGEX_MOBILE
from apps.admin.views.vip import UserVipSerializer
from apps.client.views.member import MemberCreateSerializer, MemberSerializer
from apps.utils.jwt_util import jwt_get_session_id, jwt_response_payload_handler
from rest_framework_simplejwt.tokens import RefreshToken

from application import dispatch, redis_connect
from apps.admin.models import Users, UserVipCard
from apps.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from apps.utils.request_util import save_login_log
from apps.utils.serializers import CustomModelSerializer
from apps.utils.validator import CustomValidationError
from apps.utils.viewset import CustomModelViewSet

logger = logging.getLogger(__name__)

User = get_user_model()


class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={"200": openapi.Response("获取成功")},
        security=[],
        operation_id="captcha-get",
        operation_description="验证码获取",
    )
    def get(self, request):
        data = {}
        if dispatch.get_system_config_values("base.captcha_state"):
            hashkey = CaptchaStore.generate_key()
            id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
            imgage = captcha_image(request, hashkey)
            # 将图片转换为base64
            image_base = base64.b64encode(imgage.content)
            data = {
                "key": id,
                "image_base": "data:image/png;base64," + image_base.decode("utf-8"),
            }
        return DetailResponse(data=data)


class LogoutView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT')

    def post(self, request):
        user = request.user
        res = Users.objects.filter(username=user.username, password=user.password).first()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(res)
        token = jwt_encode_handler(payload)
        session_id = jwt_get_session_id(token)
        key = f"{self.prefix}_{session_id}_{res.username}"
        cache.delete(key)
        # user.user_secret = uuid4()
        # user.save()
        # key = f"{self.prefix}_{user.username}"
        # if getattr(settings, "REDIS_ENABLE", False):
        #     cache.delete(key)
        return SuccessResponse()


class AppLoginView(ObtainJSONWebToken):
    JWT_AUTH_COOKIE = ''
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX')
    ex = settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        user = Users.objects.filter(mobile=data.get('mobile')).first()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        key = None
        token = None
        _dict = {}
        if cache.get(data.get('mobile')) is None:
            return ErrorResponse(msg='验证码已失效')
        if data.get('code') != json.loads(cache.get(data.get('mobile'))).get('code'):
            return ErrorResponse(msg='验证码错误')
        if user is None:
            del data['code']
            data['user_type'] = 1
            data['username'] = data.get('mobile')
            import random
            data['name'] = 'DD' + data.get('mobile')[3:]
            inviteCode = ''.join(random.sample(string.ascii_letters + string.digits, 6))
            data['inviteCode'] = inviteCode.upper()  # 邀请码
            serializer = MemberSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            try:
                userObj = Users.objects.filter(mobile=data.get('mobile')).first()
                data["name"] = userObj.name
                data["userId"] = userObj.id
                data["avatar"] = userObj.avatar
                data['user_type'] = userObj.user_type
                data['mobile'] = userObj.mobile
                data['email'] = userObj.email
            except Exception as e:
                return ErrorResponse(msg='参数错误')
            payload = jwt_payload_handler(userObj)
            token = jwt_encode_handler(payload)
            _dict = {'id': userObj.id, 'mobile': userObj.mobile, 'email': userObj.email, 'token': token}
            session_id = jwt_get_session_id(token)
            key = f"{self.prefix}_{session_id}_{userObj.username}"
            # 是否开启单点登录
            if dispatch.get_system_config_values("base.single_login"):
                # 将之前登录用户的token加入黑名单
                # user = Users.objects.filter(id=user.id).values('last_token').first()
                last_token = cache.get(key)
                if last_token:
                    try:
                        token = RefreshToken(last_token)
                        token.blacklist()
                    except:
                        pass
                    # 将最新的token保存到用户表
                cache.set(key, json.dumps(_dict), 2592000)
            cache.set(key, json.dumps(_dict), 2592000)  # 一个月到期
            # response_data = jwt_response_payload_handler(token, user, request)
            res = {'access': token, **data}
            save_login_log(request)
            return DetailResponse(data=res)
        else:
            try:
                userObj = Users.objects.filter(mobile=data.get('mobile')).first()
                data["name"] = userObj.name
                data["userId"] = userObj.id
                data["avatar"] = userObj.avatar
                data['user_type'] = userObj.user_type
                data['mobile'] = userObj.mobile
                data['email'] = userObj.email
            except Exception as e:
                return ErrorResponse(msg='参数错误')
            payload = jwt_payload_handler(userObj)
            token = jwt_encode_handler(payload)
            _dict = {'id': userObj.id, 'mobile': userObj.mobile, 'email': userObj.email, 'token': token}
            session_id = jwt_get_session_id(token)
            key = f"{self.prefix}_{session_id}_{userObj.username}"
            # 是否开启单点登录
            if dispatch.get_system_config_values("base.single_login"):
                # 将之前登录用户的token加入黑名单
                # user = Users.objects.filter(id=user.id).values('last_token').first()
                last_token = cache.get(key)
                if last_token:
                    try:
                        token = RefreshToken(last_token)
                        token.blacklist()
                    except:
                        pass
                    # 将最新的token保存到用户表
                cache.set(key, json.dumps(_dict), 2592000)
            cache.set(key, json.dumps(_dict), 2592000)  # 一个月到期
            # response_data = jwt_response_payload_handler(token, user, request)
            res = {'access': token, **data}
            save_login_log(request)
            return DetailResponse(data=res)


class CustomTokenRefreshView(TokenRefreshView):
    """
    自定义token刷新
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            data = {
                "access": str(token.access_token),
                "refresh": str(token)
            }
        except:
            return ErrorResponse(status=HTTP_401_UNAUTHORIZED)
        return DetailResponse(data=data)


class ApiLoginSerializer(CustomModelSerializer):
    """接口文档登录-序列化器"""

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Users
        fields = ["username", "password"]


class ApiLogin(APIView):
    """接口文档的登录接口"""

    serializer_class = ApiLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user_obj = auth.authenticate(
            request,
            username=username,
            password=hashlib.md5(password.encode(encoding="UTF-8")).hexdigest(),
        )
        if user_obj:
            login(request, user_obj)
            return redirect("/")
        else:
            return ErrorResponse(msg="账号/密码错误")


class GetPhoneCode(APIView):
    """
    获取验证码
    """
    authentication_classes = []
    permission_classes = []

    # 生成随机验证码的函数
    def generate_code(self):
        seeds = "1234567890"
        code_lst = []
        for i in range(4):
            code_lst.append(choice(seeds))
        return "".join(code_lst)

    def verify_phone(self, mobile):
        return re.match(REGEX_MOBILE, mobile)

    def verify_times(self, mobile):
        now_time = calendar.timegm(time.gmtime())
        if cache.get(mobile):
            if now_time - json.loads(cache.get(mobile)).get('utc_time') <= 60:
                return False

    def get(self, request: Request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        key = mobile
        utc_time = calendar.timegm(time.gmtime())
        code = {
            'code': self.generate_code(),
            'utc_time': utc_time
        }
        if mobile:
            if self.verify_times(mobile) is False:
                return ErrorResponse(msg='请求频繁,请稍后重试')
            if self.verify_phone(mobile) is None:
                return ErrorResponse(msg='手机号格式不正确')
            else:
                cache.set(key, json.dumps(code), 300)
        else:
            return ErrorResponse(msg='参数错误')
        return DetailResponse(data=code)
