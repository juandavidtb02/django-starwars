from django.test import TestCase
from graphene.test import Client
from core.schema import schema
from movies.models import Movie, Person


class MovieQueryIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.director = Person.objects.create(name="George Lucas", gender="male", birthday="1944-05-14")
        Movie.objects.create(title="A New Hope", release_date="1977-05-25", director=self.director)

    def test_all_movies_query_returns_results(self):
        query = '''
        {
          allMovies {
            edges {
              node {
                title
                director {
                  name
                }
              }
            }
          }
        }
        '''
        response = self.client.execute(query)
        edges = response["data"]["allMovies"]["edges"]

        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["director"]["name"], "George Lucas")
