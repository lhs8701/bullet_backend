from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    """
    widget=forms.PasswordInput : input type을 password로 바꾸기 위해 사용
    """

    class Meta:
        model = User
        fields = ('username', 'nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    # current_password = forms.CharField(label="현재 패스워드", widget=forms.PasswordInput)
    # new_password = forms.CharField(label="새 패스워드", widget=forms.PasswordInput)
    # new_password2 = forms.CharField(label="패스워드 확인", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password', 'nickname', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'nickname', 'is_staff',)
    list_filter = ('username', 'nickname')
    fieldsets = (
        (None, {'fields': ('username', 'nickname', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'nickname', 'password1', 'password2')}),
    )
    search_fields = ('username', 'nickname')
    ordering = ['-date_joined']


admin.site.register(User, UserAdmin)
