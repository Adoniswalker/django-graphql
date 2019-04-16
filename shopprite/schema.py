import graphene

from users.schema import Query as user_query


class Query(user_query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
