from rest_framework import serializers

from rest_framework.serializers import ValidationError

from api.models import User


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField(allow_blank=False)
    dob = serializers.DateField(required=True, format="%d-%m-%Y", input_formats=['%d-%m-%Y'])
    password = serializers.CharField(min_length=6, required=True, allow_null=False)
    confirm_password = serializers.CharField(min_length=6, required=True, allow_null=False)
    is_admin = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        validated_data['is_staff'] = validated_data.pop('is_admin')
        user_instance = User.objects.create(**validated_data)

        user_instance.set_password(confirm_password)

        user_instance.save()
        return user_instance

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not email:
            raise ValidationError('add `email`')

        if not password:
            raise ValidationError('set password')

        if email:
            email = email.strip(' ')
            user_queryset = User.objects.filter(email=email)
            if user_queryset.exists():
                raise ValidationError('User already exist!')
            if '@' not in email:
                raise ValidationError('Use valid `email`')

        if password != confirm_password:
            raise ValidationError('Password and Confirm password not match.Please enter valid correct password!.')

        return data

    def to_representation(self, instance):
        user_dict = instance.json()
        return user_dict
