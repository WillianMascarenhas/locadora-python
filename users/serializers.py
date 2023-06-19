from rest_framework import serializers
from users.models import User


class UserBusterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(max_length=50, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data) -> User:
        email = validated_data["email"]
        # get_email= User.objects.get(email=email)
        if validated_data["is_employee"] == True:
            validated_data["is_superuser"] = True

        return User.objects.create_user(**validated_data)
    
    def update(self, instance: User, validated_data:dict) -> User:

        for key, value in validated_data.items():
            # caso o campo sejá de password deve fazer ess condicional para transformar a str vindo do resquest eu um hash
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

            instance.save()
 
        return instance
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)
