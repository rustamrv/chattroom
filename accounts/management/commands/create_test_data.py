from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from room.models import Room, MembersRoom

class Command(BaseCommand):
    help = 'Creates test data: an admin, two users, and a test room.'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # 1. Create Superuser
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser('admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser "admin@example.com" with password "admin"'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin@example.com" already exists.'))

        # 2. Create regular users
        user1, created1 = User.objects.get_or_create(email='user1@example.com')
        if created1:
            user1.set_password('user1')
            user1.save()
            self.stdout.write(self.style.SUCCESS('Successfully created user "user1@example.com" with password "user1"'))
        else:
             self.stdout.write(self.style.WARNING('User "user1@example.com" already exists.'))

        user2, created2 = User.objects.get_or_create(email='user2@example.com')
        if created2:
            user2.set_password('user2')
            user2.save()
            self.stdout.write(self.style.SUCCESS('Successfully created user "user2@example.com" with password "user2"'))
        else:
            self.stdout.write(self.style.WARNING('User "user2@example.com" already exists.'))
            
        # 3. Create a test room
        admin_user = User.objects.get(email='admin@example.com')
        room, room_created = Room.objects.get_or_create(name='Test Room', defaults={'author': admin_user})
        if room_created:
            self.stdout.write(self.style.SUCCESS('Successfully created room "Test Room" with author "admin"'))
        else:
            self.stdout.write(self.style.WARNING('Room "Test Room" already exists.'))
            
        # 4. Add users to the room
        users_to_add = [admin_user, user1, user2]
        
        for user in users_to_add:
            _, member_created = MembersRoom.objects.get_or_create(user=user, room=room)
            if member_created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added user "{user.email}" to the room.'))
            else:
                self.stdout.write(self.style.WARNING(f'User "{user.email}" is already in the room.')) 