from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Users
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password再入力', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    picture = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'picture' ,'is_superuser')

        def clean_password(self):
            return self.initial['password']
        




class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    phone_number = forms.IntegerField(label='電話番号')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())   



    class Meta():
        model = Users
        fields = ('username', 'age', 'email', 'phone_number', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが違います')
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'],user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード",widget=forms.PasswordInput())

class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢',min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真',required=False)

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture')

class PasswordChangeForm(forms.ModelForm):

    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput()) 

    class Meta:
        model = Users
        fields = ('password',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが違います')
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'],user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user 


