import datetime

from dateutil.relativedelta import relativedelta

from apps.admin.models import PayChannel, VipCard, Users, UserVipCard
from rest_framework.request import Request

from apps.admin.views.pay_channel import PayChannelSerializer
from apps.admin.views.vip import UserVipSerializer
from apps.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from apps.utils.pay import  Pay
from apps.utils.serializers import CustomModelSerializer
from apps.utils.viewset import CustomModelViewSet
from rest_framework.views import APIView


class PayMoneyViewSet(CustomModelViewSet, Pay):
    # queryset = PayChannel.objects.filter(is_deleted=0).all()
    serializer_class = PayChannelSerializer
    permission_classes = []

    def pay(self, request: Request, *args, **kwargs):
        data = request.data
        months = None
        payChannelObj = PayChannel.objects.filter(id=data.get('pId')).first()
        user = Users.objects.filter(id=request.user.id).first()
        vipObj = VipCard.objects.filter(id=data.get('vId')).first()
        res = self.payVip(vipObj, payChannelObj, user)
        if res:
            return DetailResponse(msg='支付成功')
        return ErrorResponse(msg='支付失败')
        # if vipObj.vipType == 'month':
        #     months = 1
        # if vipObj.vipType == 'quarter':
        #     months = 3
        # if vipObj.vipType == 'halfYear':
        #     months = 6
        # if vipObj.vipType == 'year':
        #     months = 12
        # if payChannelObj and user:
        #     # 余额支付
        #     if payChannelObj.payCode == 'balance':
        #         if user.balance < vipObj.currentPrice:
        #             return ErrorResponse(msg='余额不足')
        #         else:
        #             userVip = UserVipCard.objects.filter(user_id=user.id).first()
        #             if userVip and userVip.isExpired is True:
        #                 now = datetime.datetime.today()
        #                 times = relativedelta(months=months)
        #                 expiration = now + times
        #                 userVip.update(expiration=expiration)
        #             elif userVip is None:
        #                 now = datetime.datetime.today()
        #                 times = relativedelta(months=months)
        #                 expiration = now + times
        #                 data = {'user_id': user.id,
        #                         'vipCard_id': vipObj.id,
        #                         'expiration': expiration,
        #                         'isExpired': 0,
        #                         'status': 0,
        #                         'is_delete': 0
        #                         }
        #                 serializer = UserVipSerializer(data=data)
        #                 if serializer.is_valid(raise_exception=True):
        #                     serializer.save()
        #                 instance = UserVipCard.objects.filter(id=serializer.data.get('id')).first()
        #                 instance.user_id = user.id
        #                 instance.vipCard_id = vipObj.id
        #                 instance.save()
        #             else:
        #                 # 续费
        #                 expiration = userVip.expiration
        #                 times = relativedelta(months=months)
        #                 expiration = expiration + times
        #                 userVip.expiration = expiration
        #                 userVip.save()
        #             balance = float(user.balance) - float(vipObj.currentPrice)
        #             user.balance = balance
        #             user.save()
        #     # 三方支付
        #     else:
        #         pass
        #     return DetailResponse(msg='支付成功')
        # return ErrorResponse(msg='未知异常')
