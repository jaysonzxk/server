import hashlib
import os
from pathlib import PurePath, PureWindowsPath, PurePosixPath
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

from application import dispatch
from apps.utils.models import CoreModel, table_prefix

STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)


class Users(CoreModel, AbstractUser):
    username = models.CharField(max_length=150, null=True, unique=True, db_index=True, verbose_name="用户账号",
                                help_text="用户账号")
    employee_no = models.CharField(max_length=150, unique=True, db_index=True, null=True, blank=True,
                                   verbose_name="工号", help_text="工号")
    secret = models.CharField(max_length=255, default=uuid4, verbose_name='加密秘钥')
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    city = models.CharField(max_length=100, verbose_name='入住城市', null=True, blank=True, help_text='入住城市')
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    USER_TYPE = (
        (0, "管理员"),
        (1, "会员"),
        (2, "技师"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=0, verbose_name="用户类型", null=True, blank=True, help_text="用户类型"
    )
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True, help_text='年龄')
    balance = models.DecimalField(max_length=10, verbose_name='余额', null=True, blank=True, help_text='余额',
                                  decimal_places=2,
                                  max_digits=5,
                                  default=0)
    isCheckIn = models.IntegerField(verbose_name='是否已入住', null=True, blank=True, help_text='是否已入住', default=0)
    isRecommend = models.IntegerField(verbose_name='是否推荐', null=True, blank=True, help_text='是否推荐', default=0)
    collectNum = models.IntegerField(verbose_name='被收藏数', null=True, blank=True, help_text='被收藏数', default=0)
    orderNum = models.IntegerField(verbose_name='已完成订单数', null=True, blank=True, help_text='已完成订单数',
                                   default=0)
    starLevel = models.IntegerField(verbose_name='级别', null=True, blank=True, help_text='级别', default=5)
    commissionRate = models.DecimalField(max_length=10, verbose_name='抽点比例', null=True, blank=True,
                                         help_text='抽点比例',
                                         decimal_places=2,
                                         max_digits=5,
                                         default=0.7)
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    parent = models.ForeignKey(to='admin.Users', verbose_name="上级", on_delete=models.PROTECT,
                               db_constraint=False,
                               null=True,
                               blank=True,
                               help_text="上级",
                               related_name='parentId')
    inviteCode = models.CharField(max_length=225, verbose_name="邀请码", null=True, blank=True, help_text="邀请码")
    points = models.IntegerField(verbose_name="积分", null=True, blank=True, default=0, help_text="积分")
    post = models.ManyToManyField(to="Post", blank=True, verbose_name="关联岗位", db_constraint=False,
                                  help_text="关联岗位")
    role = models.ManyToManyField(to="Role", blank=True, verbose_name="关联角色", db_constraint=False,
                                  help_text="关联角色")
    dept = models.ForeignKey(
        to="Dept",
        verbose_name="所属部门",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联部门",
    )
    last_token = models.CharField(max_length=255, null=True, blank=True, verbose_name="最后一次登录Token",
                                  help_text="最后一次登录Token")

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Post(CoreModel):
    name = models.CharField(null=False, max_length=64, verbose_name="岗位名称", help_text="岗位名称")
    code = models.CharField(max_length=32, verbose_name="岗位编码", help_text="岗位编码")
    sort = models.IntegerField(default=1, verbose_name="岗位顺序", help_text="岗位顺序")
    STATUS_CHOICES = (
        (0, "离职"),
        (1, "在职"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="岗位状态", help_text="岗位状态")

    class Meta:
        db_table = table_prefix + "system_post"
        verbose_name = "岗位表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="角色名称", help_text="角色名称")
    key = models.CharField(max_length=64, unique=True, verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    status = models.BooleanField(default=True, verbose_name="角色状态", help_text="角色状态")
    admin = models.BooleanField(default=False, verbose_name="是否为admin", help_text="是否为admin")
    DATASCOPE_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门及以下数据权限"),
        (2, "本部门数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    data_range = models.IntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="数据权限范围",
                                     help_text="数据权限范围")
    remark = models.TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    dept = models.ManyToManyField(to="Dept", verbose_name="数据权限-关联部门", db_constraint=False,
                                  help_text="数据权限-关联部门")
    menu = models.ManyToManyField(to="Menu", verbose_name="关联菜单", db_constraint=False, help_text="关联菜单")
    permission = models.ManyToManyField(
        to="MenuButton", verbose_name="关联菜单的接口按钮", db_constraint=False, help_text="关联菜单的接口按钮"
    )

    class Meta:
        db_table = table_prefix + "system_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Dept(CoreModel):
    name = models.CharField(max_length=64, verbose_name="部门名称", help_text="部门名称")
    key = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name="关联字符",
                           help_text="关联字符")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    status = models.BooleanField(default=True, verbose_name="部门状态", null=True, blank=True, help_text="部门状态")
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级部门",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级部门",
    )

    @classmethod
    def recursion_dept_info(cls, dept_id: int, dept_all_list=None, dept_list=None):
        """
        递归获取部门的所有下级部门
        :param dept_id: 需要获取的id
        :param dept_all_list: 所有列表
        :param dept_list: 递归list
        :return:
        """
        if not dept_all_list:
            dept_all_list = Dept.objects.values("id", "parent")
        if dept_list is None:
            dept_list = [dept_id]
        for ele in dept_all_list:
            if ele.get("parent") == dept_id:
                dept_list.append(ele.get("id"))
                cls.recursion_dept_info(ele.get("id"), dept_all_list, dept_list)
        return list(set(dept_list))

    class Meta:
        db_table = table_prefix + "system_dept"
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Menu(CoreModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.PROTECT,
        verbose_name="上级菜单",
        null=True,
        blank=True,
        db_constraint=False,
        help_text="上级菜单",
    )
    icon = models.CharField(max_length=64, verbose_name="菜单图标", null=True, blank=True, help_text="菜单图标")
    name = models.CharField(max_length=64, verbose_name="菜单名称", help_text="菜单名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.BooleanField(default=False, verbose_name="是否外链", help_text="是否外链")
    is_catalog = models.BooleanField(default=False, verbose_name="是否目录", help_text="是否目录")
    web_path = models.CharField(max_length=128, verbose_name="路由地址", null=True, blank=True, help_text="路由地址")
    component = models.CharField(max_length=128, verbose_name="组件地址", null=True, blank=True, help_text="组件地址")
    component_name = models.CharField(max_length=50, verbose_name="组件名称", null=True, blank=True,
                                      help_text="组件名称")
    status = models.BooleanField(default=True, blank=True, verbose_name="菜单状态", help_text="菜单状态")
    cache = models.BooleanField(default=False, blank=True, verbose_name="是否页面缓存", help_text="是否页面缓存")
    visible = models.BooleanField(default=True, blank=True, verbose_name="侧边栏中是否显示",
                                  help_text="侧边栏中是否显示")

    class Meta:
        db_table = table_prefix + "system_menu"
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class MenuButton(CoreModel):
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="menuPermission",
        on_delete=models.PROTECT,
        verbose_name="关联菜单",
        help_text="关联菜单",
    )
    name = models.CharField(max_length=64, verbose_name="名称", help_text="名称")
    value = models.CharField(max_length=64, verbose_name="权限值", help_text="权限值")
    api = models.CharField(max_length=200, verbose_name="接口地址", help_text="接口地址")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True,
                                 help_text="接口请求方法")

    class Meta:
        db_table = table_prefix + "system_menu_button"
        verbose_name = "菜单权限表"
        verbose_name_plural = verbose_name
        ordering = ("-name",)


class Dictionary(CoreModel):
    TYPE_LIST = (
        (0, "text"),
        (1, "number"),
        (2, "date"),
        (3, "datetime"),
        (4, "time"),
        (5, "files"),
        (6, "boolean"),
        (7, "images"),
    )
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="字典名称", help_text="字典名称")
    value = models.CharField(max_length=200, blank=True, null=True, verbose_name="字典编号",
                             help_text="字典编号/实际值")
    parent = models.ForeignKey(
        to="self",
        related_name="sublist",
        db_constraint=False,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="父级",
        help_text="父级",
    )
    type = models.IntegerField(choices=TYPE_LIST, default=0, verbose_name="数据值类型", help_text="数据值类型")
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name="颜色", help_text="颜色")
    is_value = models.BooleanField(default=False, verbose_name="是否为value值",
                                   help_text="是否为value值,用来做具体值存放")
    status = models.BooleanField(default=True, verbose_name="状态", help_text="状态")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    remark = models.CharField(max_length=2000, blank=True, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + "system_dictionary"
        verbose_name = "字典表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_dictionary()  # 有更新则刷新字典配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_dictionary()
        return res


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True,
                                       help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True,
                                    help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True,
                                      help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True,
                                  help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True,
                                       help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True,
                                     help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + "system_operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return PurePosixPath("files", h[:1], h[1:2], h + ext.lower())


class FileList(CoreModel):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.FileField(upload_to=media_file_name, null=True, blank=True, )
    file_url = models.CharField(max_length=255, blank=True, verbose_name="文件地址", help_text="文件地址")
    engine = models.CharField(max_length=100, default='local', blank=True, verbose_name="引擎", help_text="引擎")
    mime_type = models.CharField(max_length=100, blank=True, verbose_name="Mime类型", help_text="Mime类型")
    size = models.CharField(max_length=36, blank=True, verbose_name="文件大小", help_text="文件大小")
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        if not self.size:
            self.size = self.url.size
        if not self.file_url:
            url = media_file_name(self, self.name)
            self.file_url = f'media/{url}'
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + "system_file_list"
        verbose_name = "文件管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Area(CoreModel):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称")
    code = models.CharField(max_length=20, verbose_name="地区编码", help_text="地区编码", unique=True, db_index=True)
    level = models.BigIntegerField(verbose_name="地区层级(1省份 2城市 3区县 4乡级)",
                                   help_text="地区层级(1省份 2城市 3区县 4乡级)")
    pinyin = models.CharField(max_length=255, verbose_name="拼音", help_text="拼音")
    initials = models.CharField(max_length=20, verbose_name="首字母", help_text="首字母")
    enable = models.BooleanField(default=True, verbose_name="是否启用", help_text="是否启用")
    pcode = models.ForeignKey(
        to="self",
        verbose_name="父地区编码",
        to_field="code",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父地区编码",
    )

    class Meta:
        db_table = table_prefix + "system_area"
        verbose_name = "地区表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return f"{self.name}"


class ApiWhiteList(CoreModel):
    url = models.CharField(max_length=200, help_text="url地址", verbose_name="url")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True,
                                 help_text="接口请求方法")
    enable_datasource = models.BooleanField(default=True, verbose_name="激活数据权限", help_text="激活数据权限",
                                            blank=True)

    class Meta:
        db_table = table_prefix + "api_white_list"
        verbose_name = "接口白名单"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class SystemConfig(CoreModel):
    parent = models.ForeignKey(
        to="self",
        verbose_name="父级",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父级",
    )
    title = models.CharField(max_length=50, verbose_name="标题", help_text="标题")
    key = models.CharField(max_length=200, verbose_name="键", help_text="键", db_index=True)
    value = models.JSONField(max_length=500, verbose_name="值", help_text="值", null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name="排序", help_text="排序", blank=True)
    status = models.BooleanField(default=True, verbose_name="启用状态", help_text="启用状态")
    data_options = models.JSONField(verbose_name="数据options", help_text="数据options", null=True, blank=True)
    FORM_ITEM_TYPE_LIST = (
        (0, "text"),
        (1, "datetime"),
        (2, "date"),
        (3, "textarea"),
        (4, "select"),
        (5, "checkbox"),
        (6, "radio"),
        (7, "img"),
        (8, "file"),
        (9, "switch"),
        (10, "number"),
        (11, "array"),
        (12, "imgs"),
        (13, "foreignkey"),
        (14, "manytomany"),
        (15, "time"),
    )
    form_item_type = models.IntegerField(
        choices=FORM_ITEM_TYPE_LIST, verbose_name="表单类型", help_text="表单类型", default=0, blank=True
    )
    rule = models.JSONField(null=True, blank=True, verbose_name="校验规则", help_text="校验规则")
    placeholder = models.CharField(max_length=100, null=True, blank=True, verbose_name="提示信息", help_text="提示信息")
    setting = models.JSONField(null=True, blank=True, verbose_name="配置", help_text="配置")

    class Meta:
        db_table = table_prefix + "system_config"
        verbose_name = "系统配置表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)
        unique_together = (("key", "parent_id"),)

    def __str__(self):
        return f"{self.title}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # from application.websocketConfig import websocket_push
        # websocket_push("apps", message={"sender": 'admin', "contentType": 'SYSTEM',
        #                                    "content": '系统配置有变化~', "systemConfig": True})

        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_system_config()  # 有更新则刷新系统配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_system_config()
        from application.websocketConfig import websocket_push
        websocket_push("apps", message={"sender": 'admin', "contentType": 'SYSTEM',
                                        "content": '系统配置有变化~', "systemConfig": True})

        return res


class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = (
        (1, "普通登录"),
        (2, "普通扫码登录"),
        (3, "微信扫码登录"),
        (4, "飞书扫码登录"),
        (5, "钉钉扫码登录"),
        (6, "短信登录")
    )
    username = models.CharField(max_length=150, verbose_name="登录用户名", null=True, blank=True,
                                help_text="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True, help_text="登录ip")
    agent = models.TextField(verbose_name="agent信息", null=True, blank=True, help_text="agent信息")
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True, help_text="浏览器名")
    os = models.CharField(max_length=200, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    continent = models.CharField(max_length=50, verbose_name="州", null=True, blank=True, help_text="州")
    country = models.CharField(max_length=50, verbose_name="国家", null=True, blank=True, help_text="国家")
    province = models.CharField(max_length=50, verbose_name="省份", null=True, blank=True, help_text="省份")
    city = models.CharField(max_length=50, verbose_name="城市", null=True, blank=True, help_text="城市")
    district = models.CharField(max_length=50, verbose_name="县区", null=True, blank=True, help_text="县区")
    isp = models.CharField(max_length=50, verbose_name="运营商", null=True, blank=True, help_text="运营商")
    area_code = models.CharField(max_length=50, verbose_name="区域代码", null=True, blank=True, help_text="区域代码")
    country_english = models.CharField(max_length=50, verbose_name="英文全称", null=True, blank=True,
                                       help_text="英文全称")
    country_code = models.CharField(max_length=50, verbose_name="简称", null=True, blank=True, help_text="简称")
    longitude = models.CharField(max_length=50, verbose_name="经度", null=True, blank=True, help_text="经度")
    latitude = models.CharField(max_length=50, verbose_name="纬度", null=True, blank=True, help_text="纬度")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型",
                                     help_text="登录类型")

    class Meta:
        db_table = table_prefix + "system_login_log"
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenter(CoreModel):
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    content = models.TextField(verbose_name="内容", help_text="内容")
    target_type = models.IntegerField(default=0, verbose_name="目标类型", help_text="目标类型")
    target_user = models.ManyToManyField(to=Users, related_name='user', through='MessageCenterTargetUser',
                                         through_fields=('messagecenter', 'users'), blank=True, verbose_name="目标用户",
                                         help_text="目标用户")
    target_dept = models.ManyToManyField(to=Dept, blank=True, db_constraint=False,
                                         verbose_name="目标部门", help_text="目标部门")
    target_role = models.ManyToManyField(to=Role, blank=True, db_constraint=False,
                                         verbose_name="目标角色", help_text="目标角色")

    class Meta:
        db_table = table_prefix + "message_center"
        verbose_name = "消息中心"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenterTargetUser(CoreModel):
    users = models.ForeignKey(Users, related_name="target_user", on_delete=models.CASCADE, db_constraint=False,
                              verbose_name="关联用户表", help_text="关联用户表")
    messagecenter = models.ForeignKey(MessageCenter, on_delete=models.CASCADE, db_constraint=False,
                                      verbose_name="关联消息中心表", help_text="关联消息中心表")
    is_read = models.BooleanField(default=False, blank=True, null=True, verbose_name="是否已读", help_text="是否已读")

    class Meta:
        db_table = table_prefix + "message_center_target_user"
        verbose_name = "消息中心目标用户表"
        verbose_name_plural = verbose_name


class VipCard(CoreModel):
    """ 会员卡配置 """
    name = models.CharField(max_length=20, verbose_name='会员卡名称', blank=True, null=True, help_text='会员卡名称')
    # rebate = models.IntegerField(verbose_name='折扣', blank=True, null=True, default=0, help_text='折扣')
    vipType = models.CharField(max_length=20, verbose_name='VIP类型', null=True, blank=True, help_text='VIP类型')
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    discount = models.IntegerField(verbose_name='折扣', null=True, blank=True, help_text='折扣', default=0)
    amount = models.DecimalField(max_length=10, verbose_name='购买金额', null=True, blank=True, help_text='购买金额',
                                 decimal_places=2,
                                 max_digits=5,
                                 default=0)
    isRecommend = models.IntegerField(verbose_name='是否推荐', null=True, blank=True, help_text='是否推荐', default=0)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "vip_card"
        verbose_name = "会员卡配置表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.name


class UserVipCard(CoreModel):
    """ 用户会员卡 """
    user = models.ForeignKey(to='admin.Users', verbose_name="关联用户",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="关联用户",
                             related_name='user_vip_card')
    vipCard = models.ForeignKey(to='VipCard', verbose_name="关联会员卡配置",
                                on_delete=models.PROTECT,
                                db_constraint=False,
                                null=True,
                                blank=True,
                                help_text="关联会员卡配置", )
    expiration = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="过期时间",
                                      verbose_name="过期时间")
    isExpired = models.IntegerField(verbose_name='是否到期', null=True, blank=True, help_text='是否到期', default=0)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "user_vip_card"
        verbose_name = "用户会员卡"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.user.username


class UserAddr(CoreModel):
    """ 用户地址 """
    user = models.ForeignKey(to='admin.Users', verbose_name="关联用户",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="关联用户",
                             related_name='user_addr')
    addr = models.CharField(max_length=100, verbose_name='用户地址', null=True, help_text='用户地址')
    isDefault = models.IntegerField(verbose_name='是否默认', null=True, blank=True, help_text='是否默认', default=1)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "user_addr"
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.user.username


class Banners(CoreModel):
    """ 轮播图 """
    name = models.CharField(max_length=100, verbose_name='轮播图名称', null=True, blank=True, help_text='轮播图名称')
    jumpType = models.IntegerField(verbose_name='跳转类型', null=True, blank=True, help_text='跳转类型', default=0)
    jumpUrl = models.CharField(max_length=225, verbose_name='跳转地址', null=True, blank=True, help_text='跳转地址')
    file = models.CharField(max_length=255, verbose_name="图片地址", null=True, blank=True, help_text="图片地址")
    isDefault = models.IntegerField(verbose_name='是否默认', null=True, blank=True, help_text='是否默认', default=1)
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "banners"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def __str__(self):
        return self.name


class Notice(CoreModel):
    """ 公告 """
    name = models.CharField(max_length=100, verbose_name='公告名称', null=True, blank=True, help_text='公告名称')
    content = models.CharField(max_length=1000, verbose_name="内容", null=True, blank=True, help_text="内容")
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "notice"
        verbose_name = "公告"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def __str__(self):
        return self.name


class Marquee(CoreModel):
    """ 跑马灯 """
    name = models.CharField(max_length=100, verbose_name='跑马灯名称', null=True, blank=True, help_text='跑马灯名称')
    content = models.CharField(max_length=1000, verbose_name="内容", null=True, blank=True, help_text="内容")
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    locationId = models.IntegerField(verbose_name='位置ID', null=True, blank=True, help_text='位置ID')
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "marquee"
        verbose_name = "跑马灯"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def __str__(self):
        return self.name


class Project(CoreModel):
    """ 服务项目 """
    name = models.CharField(max_length=100, verbose_name='项目名称', null=True, blank=True, help_text='项目名称')
    img = models.CharField(max_length=255, verbose_name="展示图", null=True, blank=True, help_text="展示图")
    duration = models.IntegerField(verbose_name="时长", null=True, blank=True, help_text="时长")
    price = models.DecimalField(max_length=10, verbose_name='现价', null=True, blank=True, help_text='现价',
                                decimal_places=2,
                                max_digits=5,
                                default=0)
    originPrice = models.DecimalField(max_length=10, verbose_name='原价', null=True, blank=True, help_text='原价',
                                      decimal_places=2,
                                      max_digits=5,
                                      default=0)
    prohibition = models.CharField(max_length=1000, verbose_name='禁忌说明', null=True, blank=True, help_text='禁忌说明')
    orderInstructions = models.CharField(max_length=1000, verbose_name='下单说明', null=True, blank=True, help_text='下单说明')
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    sales = models.IntegerField(verbose_name="销量", null=True, blank=True, help_text="销量")
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "project"
        verbose_name = "服务项目"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def __str__(self):
        return self.name


class MasterCheckIn(CoreModel):
    """ 师傅入住 """
    mobile = models.CharField(max_length=100, verbose_name='手机号', null=True, blank=True, help_text='手机号')
    name = models.CharField(max_length=100, verbose_name='入住城市', null=True, blank=True, help_text='入住城市')
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True, help_text='年龄')
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    city = models.CharField(max_length=100, verbose_name='入住城市', null=True, blank=True, help_text='入住城市')
    reviewStatus = models.IntegerField(verbose_name='审核状态', null=True, blank=True, help_text='审核状态', default=0)
    failureReason = models.CharField(max_length=100, verbose_name='失败原因', null=True, blank=True,
                                     help_text='失败原因')
    store = models.CharField(max_length=100, verbose_name='店面名称', null=True, blank=True, help_text='店面名称')
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "master_check_in"
        verbose_name = "师傅入住"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def __str__(self):
        return self.name


class PayChannel(CoreModel):
    """ 支付渠道 """
    name = models.CharField(max_length=100, verbose_name='渠道名称', null=True, blank=True, help_text='渠道名称')
    minQuota = models.DecimalField(max_length=10, verbose_name='最小限额', null=True, blank=True, help_text='最小限额',
                                   decimal_places=2,
                                   max_digits=5,
                                   default=0)
    maxQuota = models.DecimalField(max_length=10, verbose_name='最大限额', null=True, blank=True, help_text='最大限额',
                                   decimal_places=2,
                                   max_digits=15,
                                   default=0)
    payKey = models.CharField(max_length=100, verbose_name='渠道key', null=True, blank=True, help_text='渠道key')
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "pay_channel"
        verbose_name = "支付渠道"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def __str__(self):
        return self.name


class ServiceOrder(CoreModel):
    """ 服务订单 """
    oderNo = models.CharField(max_length=100, verbose_name='订单编号', null=True, blank=True, help_text='订单编号')
    project = models.ForeignKey(to='admin.Project', verbose_name="关联项目",
                                on_delete=models.PROTECT,
                                db_constraint=False,
                                null=True,
                                blank=True,
                                help_text="关联项目",
                                related_name='server_project')
    user = models.ForeignKey(to='admin.Users', verbose_name="关联用户",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="关联用户",
                             related_name='user_oder')
    master = models.ForeignKey(to='admin.Users', verbose_name="关联技师",
                               on_delete=models.PROTECT,
                               db_constraint=False,
                               null=True,
                               blank=True,
                               help_text="关联技师",
                               related_name='master_order')
    addr = models.ForeignKey(to='admin.UserAddr', verbose_name="关联用户地址",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="关联用户地址",
                             related_name='order_user_addr')
    payOrder = models.ForeignKey(to='admin.PayOrder', verbose_name="关联支付订单",
                                 on_delete=models.PROTECT,
                                 db_constraint=False,
                                 null=True,
                                 blank=True,
                                 help_text="关联支付订单",
                                 related_name='pay_order')
    orderStatus = models.IntegerField(verbose_name='服务订单状态', null=True, blank=True, help_text='服务订单状态',
                                      default=0)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "service_order"
        verbose_name = "服务订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.oderNo


class PayOrder(CoreModel):
    """ 支付订单 """
    oderNo = models.CharField(max_length=100, verbose_name='支付单编号', null=True, blank=True, help_text='支付单编号')
    masterProject = models.ForeignKey(to='admin.MasterProject', verbose_name="关联技师项目",
                                      on_delete=models.PROTECT,
                                      db_constraint=False,
                                      null=True,
                                      blank=True,
                                      help_text="关联技师项目",
                                      related_name='pay_oder_master_project')
    payChannel = models.ForeignKey(to='admin.PayChannel', verbose_name="关联支付渠道",
                                   on_delete=models.PROTECT,
                                   db_constraint=False,
                                   null=True,
                                   blank=True,
                                   help_text="关联支付渠道",
                                   related_name='payChannel_order')
    amount = models.DecimalField(max_length=10, verbose_name='支付金额', null=True, blank=True, help_text='支付金额',
                                 decimal_places=2,
                                 max_digits=5,
                                 default=0)
    orderStatus = models.IntegerField(verbose_name='支付状态', null=True, blank=True, help_text='支付状态',
                                      default=0)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "pay_order"
        verbose_name = "支付订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.oderNo


class MasterProject(CoreModel):
    """ 技师服务项目 """
    user = models.ForeignKey(to='admin.Users', verbose_name="技师",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="技师",
                             related_name='master_project')
    project = models.ForeignKey(to='admin.Project', verbose_name="项目",
                                on_delete=models.PROTECT,
                                db_constraint=False,
                                null=True,
                                blank=True,
                                help_text="项目",
                                related_name='project_master')

    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "master_project"
        verbose_name = "技师服务项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class Collect(CoreModel):
    """ 收藏 """
    user = models.ForeignKey(to='admin.Users', verbose_name="会员",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="会员",
                             related_name='collect_user')
    master = models.ForeignKey(to='admin.Users', verbose_name="技师",
                               on_delete=models.PROTECT,
                               db_constraint=False,
                               null=True,
                               blank=True,
                               help_text="技师",
                               related_name='collect_master')

    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "collect"
        verbose_name = "收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
