from django import forms
from apps.forms import FormsMxin
from django.core.cache import cache


class LoginForm(forms.Form):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': '密码最大长度不能超过20', 'min_length': '密码最小长度不能小于6'})
    remember = forms.BooleanField(required=False)

    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        return {}


class RegisterForm(forms.Form, FormsMxin):
    username = forms.CharField(min_length=3, max_length=20)
    telephone = forms.CharField(max_length=11)
    # email = forms.EmailField()
    password1 = forms.CharField(min_length=6, max_length=20, error_messages={'min_length': '密码最小长度不小于6',
                                                                             'max_length': '密码最大长度不大于20'})
    password2 = forms.CharField(min_length=6, max_length=20, error_messages={'min_length': '密码最小长度不小于6',
                                                                             'max_length': '密码最大长度不大于20'})
    sms_captcha = forms.CharField(max_length=4)
    img_captcha = forms.CharField(max_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        print(cleaned_data)
        pw1 = cleaned_data.get('password1')
        print(pw1)
        pw2 = cleaned_data.get('password2')
        if pw1 != pw2:
            raise forms.ValidationError("两次密码输入不一致")

        img_captcha = cleaned_data.get('img_captcha').lower()
        true_img = cache.get('image_text')
        print("获取的图形验证码" + str(img_captcha))

        if str(img_captcha) != true_img:
            raise forms.ValidationError('请输入正确的图形验证码')

        sms_code = cache.get('sms_code')
        sms_captcha = cleaned_data.get('sms_captcha')
        print("====", sms_captcha)
        if sms_code != int(sms_captcha):
            raise forms.ValidationError('输入的短信验证码不正确')
