from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.models import Group

UserModel = get_user_model()


class UserEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        # field_classes = {'email': auth_forms.UsernameField}


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, request, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['password'].widget.attrs['placeholder'] = "Password"


class UserCreateForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['password1'].widget.attrs['placeholder'] = "Password"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm password"

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture')


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=UserModel.objects.all(),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance
