from django import forms
from .models import ServiceObject


class ServiceObjectForm(forms.Form):
    name = forms.CharField(label='姓名',
                           max_length=16,
                           error_messages={'required': '名字不能为空'}
                           )
    tel = forms.CharField(max_length=11,
                          min_length=11,
                          label='电话',
                          error_messages={'required': '电话号码不能为空',
                                          'max_length': '电话号码为11位',
                                          'min_length': '电话号码为11位'}
                          )
    computer_model = forms.CharField(required=False,
                                     label='电脑品牌/型号(选填)'
                                     )
    problem = forms.CharField(widget=forms.Textarea(),
                              label='电脑故障',
                              error_messages={'required': '把故障告诉我们啊,亲'}
                              )
