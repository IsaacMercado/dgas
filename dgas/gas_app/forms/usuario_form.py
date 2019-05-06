# -*- coding: utf-8 -*-
from dgas.users.models import GasUser
from functools import partial
from django import forms

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class GasUserForm(forms.ModelForm):

    class Meta:
        exclude = ('password',
                   'last_login', 'date_joined',
                   'username',
                   'user_permissions', 'is_superuser',
                    'is_staff', 'email',
                   'last_access', 'is_admin')
        model = GasUser


    # Added to validate username as email field
    username = forms.EmailField(
        label='Correo electrónico',
        required=True,
        help_text="Correo electrónico",
        widget=forms.TextInput(
            attrs={'class': 'input-xlarge', 'placeholder': 'Correo electrónico'})
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'input-xlarge', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label='Confirme contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'input-xlarge',
                   'placeholder': 'Confirme contraseña'})
    )

    def clean_email(self):
        email = self.cleaned_data['username']
        return email

    def clean_username(self):
        # Avoid validation in model's definition
        self._meta.exclude += ('username',)
        username = self.cleaned_data['username']
        try:
            # Check if username is already registered
            GasUser.objects.get(username=username)
            # Try to update a username with other already taken?
            if self.instance.username != username:
                raise forms.ValidationError(
                    'Correo electrónico ya esta registrado.')
        except GasUser.DoesNotExist:
            pass
        # User doesn't exist or it's ok to be updated
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contrasenas no son iguales')
        if len(password1) < 7:
            raise forms.ValidationError(
                'La contraseña debe tener mas de 7 caracteres')
        return password2


class GasUserEditForm(forms.ModelForm):

    class Meta:
        exclude = ('username', 'password',
                   'last_login', 'date_joined',
                   'user_permissions', 'is_superuser',
                   'is_staff',
                   'last_access', 'is_admin')
        model = GasUser


class GasUserPasswdForm(forms.ModelForm):

    class Meta:
        '''
        exclude = (
                   'first_name', 'last_name', 'cedula',
                   'carnet_salud_vence', 'fecha_ingreso',
                   'foto',
                   'password', 'last_login',
                   'groups', 'empresa', 'email',
                   'date_joined', 'user_permissions',
                   'is_superuser',
                   'is_active', 'is_staff', 'email', 'last_access', 'is_admin')
        '''
        fields = ['first_name', 'last_name']
        model = GasUser

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'input-xlarge', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label='Confirme contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'input-xlarge',
                   'placeholder': 'Confirme contraseña'})
    )

    def __init__(self, *args, **kwargs):
        user_details = kwargs.pop('user_details', None)
        super(GasUserPasswdForm, self).__init__(*args, **kwargs)
        if user_details:
            self.fields['username'].initial = user_details[0]['username']

    def clean_username(self):
        # Avoid validation in model's definition
        self._meta.exclude += ('username',)
        username = self.cleaned_data['username']
        try:
            # Check if username is already registered
            GasUser.objects.get(username=username)
            # Try to update a username with other already taken?
            if self.instance.username != username:
                raise forms.ValidationError(
                    'Email address is already registered.')
        except GasUser.DoesNotExist:
            pass
        # User doesn't exist or it's ok to be updated
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        if len(password1) < 7:
            raise forms.ValidationError(
                'Password much be at least 7 characters long.')
        return password2
