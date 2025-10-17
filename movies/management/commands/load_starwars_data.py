import requests
from django.core.management.base import BaseCommand
from django.db import connection
from movies.models import Person, Character, Planets, Movie


class Command(BaseCommand):
    help = "Carga datos del universo Star Wars desde la API pública SWAPI"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🌍 Cargando datos de Star Wars..."))

        planet_response = requests.get("https://swapi.dev/api/planets/").json()
        planet_data = planet_response["results"]
        planet_map = {}

        for p in planet_data:
            planet, _ = Planets.objects.get_or_create(name=p["name"])
            planet_map[p["url"]] = planet

        self.stdout.write(self.style.SUCCESS(f"✅ {len(planet_map)} planetas cargados."))

        people_response = requests.get("https://swapi.dev/api/people/").json()
        people_data = people_response["results"]
        person_map = {}

        for p in people_data:
            name = p["name"]
            gender = p["gender"] if p["gender"] != "n/a" else "unknown"
            specie = None 
            birthday = "1900-01-01"

            person = Person.objects.create(name=name, birthday=birthday, gender=gender)
            character = Character.objects.create(
                name=name, birthday=birthday, gender=gender, specie=specie, alias=None
            )
            person_map[p["url"]] = character

        self.stdout.write(self.style.SUCCESS(f"✅ {len(person_map)} personajes cargados."))

        movie_response = requests.get("https://swapi.dev/api/films/").json()
        movie_data = movie_response["results"]

        for m in movie_data:
            title = m["title"]
            release_date = m["release_date"]
            opening_crawl = m["opening_crawl"]
            director_name = m["director"]
            producer_names = [p.strip() for p in m["producer"].split(",")]

            director, _ = Person.objects.get_or_create(
                name=director_name,
                defaults={"birthday": "1900-01-01", "gender": "unknown"},
            )

            movie = Movie.objects.create(
                title=title,
                release_date=release_date,
                opening_crawl=opening_crawl,
                director=director,
            )

            for pname in producer_names:
                producer, _ = Person.objects.get_or_create(
                    name=pname, defaults={"birthday": "1900-01-01", "gender": "unknown"}
                )
                movie.producers.add(producer)

            for char_url in m["characters"]:
                if char_url in person_map:
                    movie.characters.add(person_map[char_url])

            for planet_url in m["planets"]:
                if planet_url in planet_map:
                    movie.planets.add(planet_map[planet_url])

        self.stdout.write(self.style.SUCCESS("🎬 Películas de Star Wars cargadas correctamente."))
        self.stdout.write(self.style.SUCCESS("✅ Todo listo."))

