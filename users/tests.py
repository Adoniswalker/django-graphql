from django.test import TestCase

# Create your tests here.
from graphene.test import Client

from shopprite.schema import schema


def test_user_creation():
    client = Client(schema)
    response = client.execute(
        """
        query {
          allUsers(username_Icontains:"ngeno"){
            edges{
              node{
                    id
                  username
                  firstName
                  lastName
                  email
                  isStaff
                  isActive
                  dateJoined
              }
            }
           
          }
        }
        """
    )
    # import pdb; pdb.set_trace()
    # print(response)

from django.contrib.auth import get_user_model

from graphql_jwt.testcases import JSONWebTokenTestCase


class UsersTests(JSONWebTokenTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_get_user(self):
        query = '''
        query {
          allUsers(username_Icontains:"ngeno"){
            edges{
              node{
                    id
                  username
                  firstName
                  lastName
                  email
                  isStaff
                  isActive
                  dateJoined
              }
            }
           
          }
}'''

        variables = {
          'username': self.user.username,
        }

        result = self.client.execute(query)
        # import pdb; pdb.set_trace()