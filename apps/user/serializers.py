from django.contrib.auth.models import User
from rest_framework import serializers

from .base_category import base_categories
from .models import Category, Transaction, UserProfile


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs) -> User:
        """
        Save user to db and validate password

        :return: New created User
        """
        if self.is_valid():
            user = User(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
            )
            password1 = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password1 != password2:
                raise serializers.ValidationError({'password': 'Passwords must match.'})

            user.set_password(password1)
            user.save()

            self.create_base_categories(base_categories, user)

            UserProfile.objects.create(user=user, balance=0)

            return user
        else:
            return self.errors

    @staticmethod
    def create_base_categories(categories: tuple, user: User) -> None:
        """
        Create base categories for new user.

        :param categories: Base categories
        :param user: Created user

        """
        for base_category in categories:
            new_base_category = Category(name=base_category, user=user)
            new_base_category.save()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def save(self, **kwargs):
        """
        Save new category to db

        :return: Created category
        """
        if self.is_valid():
            user = User.objects.get(pk=self.context['user_id'])
            if self.instance is not None:
                self.instance = self.update(self.instance, self.validated_data)
                return self.instance

            category = Category.objects.create(**self.validated_data, user=user)
            return category
        else:
            return self.errors


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['sum', 'category', 'organization', 'description', 'time', 'type']

    def save(self, **kwargs):
        if self.is_valid():
            user: User = User.objects.get(pk=self.context['user_id'])
            category: Category = Category.objects.get(name=self.validated_data['category'], user=user)
            user_pofile: UserProfile = UserProfile.objects.get(user=user)
            if self.instance is not None:
                self.instance = self.update(self.instance, self.validated_data)
                return self.instance

            transaction = Transaction.objects.create(**self.validated_data, user=user)

            if transaction.type == 'top up':
                user_pofile.balance += transaction.sum
            else:
                user_pofile.balance -= transaction.sum
            user_pofile.save()
            return transaction
        else:
            return self.errors
