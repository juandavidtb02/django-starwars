from django.test import TestCase
from movies.models import Movie, Character, Person


class CharacterCountTest(TestCase):
    def setUp(self):
        director = Person.objects.create(name="George Lucas", gender="male", birthday="1944-05-14")
        self.movie = Movie.objects.create(title="Empire Strikes Back", release_date="1980-05-21", director=director)

        luke = Character.objects.create(name="Luke Skywalker", gender="male", birthday="1900-01-01")
        leia = Character.objects.create(name="Leia Organa", gender="female", birthday="1900-01-01")
        self.movie.characters.add(luke, leia)

    def test_count_characters_in_movie(self):
        self.assertEqual(self.movie.characters.count(), 2)
