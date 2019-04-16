import graphene
from django.contrib.auth.models import User

from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):
    user = graphene.Field(UserType,
                          id=graphene.Int(),
                          username=graphene.String())
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get("id")
        username = kwargs.get("username")
        if id:
            return User.objects.get(pk=id)
        if username:
            return User.objects.get(username=username)
        return {"status": "error", "message": "Kindly provide a query"}, 400
