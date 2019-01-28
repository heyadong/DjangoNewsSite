from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, username,telephone,password,**kwargs):
        if not telephone:
            raise ValueError("请输入手机号码")
        if not username:
            raise ValueError("请输入用户名")
        if not password:
            raise ValueError("请输入密码")
        user = self.model(username=username,telephone=telephone,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,username,password,telephone,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone, password=password,username=username,**kwargs)

    def create_superuser(self,username,password,telephone,**kwargs):
        kwargs['is_superuser'] = True
        kwargs["is_staff"] = True
        return self._create_user(telephone=telephone,password=password,username=username,**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 重写user模型
    # 重写User模型前不能进行数据库的迁移。
    uuid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=100)
    telephone = models.CharField(max_length=11,unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'  # 验证字段改为telephone 验证
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    object = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


