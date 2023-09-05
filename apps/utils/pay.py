import datetime

from dateutil.relativedelta import relativedelta

from apps.admin.models import UserVipCard
from apps.admin.views.vip import UserVipSerializer
from apps.utils.json_response import ErrorResponse, DetailResponse


class Pay(object):

    def payVip(self, vipObj, payChannelObj, user):
        months = None
        if vipObj.vipType == 'month':
            months = 1
        if vipObj.vipType == 'quarter':
            months = 3
        if vipObj.vipType == 'halfYear':
            months = 6
        if vipObj.vipType == 'year':
            months = 12
        if payChannelObj and user:
            # 余额支付
            if payChannelObj.payCode == 'balance':
                if user.balance < vipObj.currentPrice:
                    return '余额不足'
                else:
                    userVip = UserVipCard.objects.filter(user_id=user.id).first()
                    if userVip and userVip.isExpired is True:
                        now = datetime.datetime.today()
                        times = relativedelta(months=months)
                        expiration = now + times
                        userVip.update(expiration=expiration)
                    elif userVip is None:
                        now = datetime.datetime.today()
                        times = relativedelta(months=months)
                        expiration = now + times
                        data = {'user': user.id,
                                'vipCard': vipObj.id,
                                'expiration': expiration,
                                'isExpired': 0,
                                'status': 0,
                                'is_delete': 0
                                }
                        serializer = UserVipSerializer(data=data)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                        instance = UserVipCard.objects.filter(id=serializer.data.get('id')).first()
                        instance.user_id = user.id
                        instance.vipCard_id = vipObj.id
                        instance.save()
                    else:
                        # 续费
                        expiration = userVip.expiration
                        times = relativedelta(months=months)
                        expiration = expiration + times
                        userVip.expiration = expiration
                        userVip.save()
                    balance = float(user.balance) - float(vipObj.currentPrice)
                    user.balance = balance
                    user.save()
                return '支付成功'
            # 三方支付
            else:
                pass
            return True
        return False
