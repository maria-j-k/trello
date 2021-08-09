from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True,
                                     min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
        user.save()

        return user


class EmailValidSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(get_user_model(), pk=data['user_id'])
        if not default_token_generator.check_token(
                user, data['token']):
            raise serializers.ValidationError('''Token is invalid or expired.
            Please request another confirmation email by signing in.''')
        return data

    def create(self, validated_data):
        instance = get_object_or_404(get_user_model(),
                                     pk=validated_data['user_id'])
        instance.is_active = True
        instance.save(update_fields=['is_active'])
        return instance
