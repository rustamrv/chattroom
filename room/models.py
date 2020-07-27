from django.db import models
from accounts.models import Profile
from .manager import RoomManager, MembersRoomManager, MessageManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    name = models.CharField(max_length=60)
    created_date = models.DateTimeField("Date created", auto_now=True,
                                        auto_now_add=False)
    author = models.ForeignKey(Profile, verbose_name="Автор",
                               related_name="author", default='',
                               on_delete=models.CASCADE)
    choice_type = [
        ('private', 'Приватный'),
        ('public', 'Публичный'),
        ('channel', 'Канал'),
    ]
    type_room = models.CharField(max_length=12, choices=choice_type,
                                 default='public')
    slug = models.SlugField(default='')

    objects = RoomManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class MembersRoom(models.Model):
    room = models.ForeignKey(Room, verbose_name="Chat",
                             on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, verbose_name="User",
                             related_name="user", on_delete=models.CASCADE)

    objects = MembersRoomManager()

    def __str__(self):
        return self.room.name


class Message(models.Model):
    sender = models.ForeignKey(Profile, verbose_name="Отправитель",
                               related_name="sender", on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField("Date created",
                                        auto_now=True, auto_now_add=False)
    room = models.ForeignKey(Room, verbose_name="Chat",
                             on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, verbose_name="Получатель",
                                  null=True, blank=True,
                                  related_name="recipient",
                                  on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    objects = MessageManager()

    def last_30_message(self):
        return Message.objects.order_by('-created_date').all()[:10]


@receiver(signal=post_save, sender=Room)
def post_save_handler(instance, **kwargs):
    user = instance.author
    MembersRoom.objects.create(user=user, room=instance)
