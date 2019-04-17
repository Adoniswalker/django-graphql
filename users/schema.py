import graphene
from django.contrib.auth.models import User
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'username': ['exact', 'icontains', 'istartswith'],
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)


class CreateUser(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()


    user = graphene.Field(UserType)

    def mutate_and_get_payload(root, info, **input):
        user = User(**input)
        password = input.pop("password")
        user.set_password(password)
        user.save()
        return CreateUser(user)


class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(object):
    user = relay.Node.Field(UserType)
    all_users = DjangoFilterConnectionField(UserType)

    @login_required
    def resolve_all_users(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Kindly login to view")
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get("id")
        username = kwargs.get("username")
        if id:
            return User.objects.get(pk=id)
        if username:
            return User.objects.get(username=username)
        return None
