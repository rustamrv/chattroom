from django.db import models
from django.db.models import Q


class RoomQuerySet(models.QuerySet):

    def get_public(self):
        return self.filter(type_room='public')

    def get_myroom(self, author):
        return self.filter(author=author)

    def get_slug(self, slug):
        return self.filter(slug=slug)

    def get_name(self, name):
        return self.filter(name=name)

    def get_id(self, id):
        return self.filter(id=id)


class RoomManager(models.Manager):

    def queryset(self):
        return RoomQuerySet(self.model, using=self._db)

    def get_public(self):
        return self.queryset().get_public()

    def get_myroom(self, author):
        return self.queryset().get_myroom(author)

    def get_slug(self, slug):
        return self.queryset().get_slug(slug)

    def get_name(self, name):
        return self.queryset().get_name(name)

    def get_id(self, id):
        return self.queryset().get_id(id)


class MembersRoomQuerySet(models.QuerySet):

    def get_member_room(self, user, room):
        obj = self.filter(user=user, room=room)
        if obj.exists():
            return True
        return False


class MembersRoomManager(models.Manager):

    def queryset(self):
        return MembersRoomQuerySet(self.model, using=self._db)

    def get_member_room(self, user, room):
        return self.queryset().get_member_room(user, room)


class MessagesQuerySet(models.QuerySet):

    def get_count(self, room_id, id_user):
        obj = self.filter(room__id=room_id, read=False)
        res = obj.filter(~Q(user_id=id_user))
        return res.count()

    def read_msg(self, msg_id):
        return self.filter(id=msg_id)


class MessageManager(models.Manager):

    def queryset(self):
        return MessagesQuerySet(self.model, using=self._db)

    def get_count(self, room_id, id_user):
        return self.queryset().get_count(room_id, id_user)

    def read_msg(self, msg_id):
        return self.queryset().read_msg(msg_id)