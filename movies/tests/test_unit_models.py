from django.test import TestCase
from movies.models import Movie, Person


class MovieModelTest(TestCase):
    def setUp(self):
        self.director = Person.objects.create(name="George Lucas", gender="male", birthday="1944-05-14")
        self.movie = Movie.objects.create(
            title="A New Hope",
            release_date="1977-05-25",
            opening_crawl="It is a period of civil war...",
            director=self.director
        )

    def test_movie_str_returns_title(self):
        self.assertEqual(str(self.movie), "A New Hope")

    def test_director_relationship(self):
        self.assertEqual(self.movie.director.name, "George Lucas")
