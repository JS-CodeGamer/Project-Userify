from rest_framework import serializers
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = MyUser
		exclude = ('is_admin', 'is_staff', 'is_superuser', 'is_active', 'password')