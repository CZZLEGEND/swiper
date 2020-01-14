from django import forms

from user.models import User
from user.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        cleaned_data = super().clean()  # 通过父类的 clean() 方法进行数据清洗
        if cleaned_data['max_distance'] < cleaned_data['min_distance']:
            raise forms.ValidationError('max_distance 必须大于 min_distance')
        else:
            return cleaned_data['max_distance']  # 如果数据没有问题，直接返回清洗后的 max_distance

    def clean_max_dating_age(self):
        cleaned_data = super().clean()
        if cleaned_data['max_dating_age'] < cleaned_data['min_dating_age']:
            raise forms.ValidationError('max_dating_age 必须大于 min_dating_age')
        else:
            return cleaned_data['max_dating_age']  # 如果数据没有问题，直接返回清洗后的 max_dating_age
