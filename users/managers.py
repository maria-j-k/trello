from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        """Creates and saves a User with email as identifier"""

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Creates and saves a Superuser with email as identifier"""

        user = self.create_user(email, password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
