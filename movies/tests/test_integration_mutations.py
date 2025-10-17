from django.test import TestCase
from graphene.test import Client
from graphene.relay import Node
from core.schema import schema
from movies.models import Movie, Person

class MovieMutationIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.director = Person.objects.create(name="George Lucas", gender="male", birthday="1944-05-14")

    def test_create_movie_mutation(self):
        mutation = '''
        mutation CreateMovie($input: CreateMovieInput!) {
          createMovie(input: $input) {
            movie {
              title
              director {
                name
              }
            }
          }
        }
        '''
        variables = {
            "input": {
                "title": "A New Hope",
                "releaseDate": "1977-05-25",
                "openingCrawl": "It is a period of civil war...",
                "directorId": Node.to_global_id("PersonNode", self.director.id)
            }
        }
        response = self.client.execute(mutation, variables=variables)
        movie_data = response["data"]["createMovie"]["movie"]

        self.assertEqual(movie_data["title"], "A New Hope")
        self.assertEqual(movie_data["director"]["name"], "George Lucas")

    def test_delete_movie_mutation(self):
        movie = Movie.objects.create(title="To Delete", release_date="1983-05-25", director=self.director)
        global_id = Node.to_global_id("MovieNode", movie.id)

        mutation = '''
        mutation DeleteMovie($input: DeleteMovieInput!) {
          deleteMovie(input: $input) {
            ok
            message
          }
        }
        '''
        variables = {"input": {"id": global_id}}
        response = self.client.execute(mutation, variables=variables)
        data = response["data"]["deleteMovie"]

        self.assertTrue(data["ok"])
        self.assertEqual(data["message"], "Movie deleted successfully")
        self.assertFalse(Movie.objects.filter(id=movie.id).exists())
