from django.contrib.auth.models import Permission, User, Group
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=2)
        group, created = Group.objects.get_or_create(name='test_group')
        permission_profile = Permission.objects.get(codename='view_profile')
        permission_add_user = Permission.objects.get(codename='add_user')
        group.permissions.add(permission_profile)
        user.groups.add(group)
        user.user_permissions.add(permission_add_user)
        group.save()
        user.save()
