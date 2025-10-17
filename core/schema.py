import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from movies.models import Person, Character, Planets, Movie

class PersonNode(DjangoObjectType):
    class Meta:
        model = Person
        interfaces = (relay.Node,)
        fields = ("id", "name", "birthday", "gender")
        filter_fields = ["name", "gender"]


class PlanetNode(DjangoObjectType):
    class Meta:
        model = Planets
        interfaces = (relay.Node,)
        fields = ("id", "name")
        filter_fields = ["name"]


class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        interfaces = (relay.Node,)
        fields = (
            "id",
            "title",
            "release_date",
            "opening_crawl",
            "director",
            "producers",
            "characters",
            "planets",
        )
        filter_fields = ["title", "director__name", "planets__name"]


class CharacterNode(DjangoObjectType):
    class Meta:
        model = Character
        interfaces = (relay.Node,)
        fields = ("id", "name", "alias", "specie", "birthday", "gender", "character_movies")
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "specie": ["exact", "icontains"],
            "gender": ["exact"],
        }               

    character_movies = DjangoFilterConnectionField(MovieNode)

    def resolve_character_movies(self, info, **kwargs):
        return self.character_movies.all()

class Query(graphene.ObjectType):
    node = relay.Node.Field() 

    all_characters = DjangoFilterConnectionField(CharacterNode)
    all_movies = DjangoFilterConnectionField(MovieNode)
    all_planets = DjangoFilterConnectionField(PlanetNode)
    all_people = DjangoFilterConnectionField(PersonNode)

class CreatePlanet(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    planet = graphene.Field(PlanetNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name):
        planet = Planets.objects.create(name=name)
        return CreatePlanet(planet=planet)


class CreateCharacter(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        alias = graphene.String(required=False)
        specie = graphene.String(required=False)
        birthday = graphene.Date(required=False)
        gender = graphene.String(required=True)

    character = graphene.Field(CharacterNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        character = Character.objects.create(
            name=input["name"],
            alias=input.get("alias"),
            specie=input.get("specie"),
            birthday=input.get("birthday") or "1900-01-01",
            gender=input["gender"],
        )
        return CreateCharacter(character=character)


class CreateMovie(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        release_date = graphene.Date(required=False)
        opening_crawl = graphene.String(required=False)
        director_id = graphene.ID(required=True)
        producer_ids = graphene.List(graphene.ID, required=False)
        planet_ids = graphene.List(graphene.ID, required=False)
        character_ids = graphene.List(graphene.ID, required=False)

    movie = graphene.Field(MovieNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        director = relay.Node.get_node_from_global_id(info, input["director_id"], only_type=PersonNode)

        movie = Movie.objects.create(
            title=input["title"],
            release_date=input.get("release_date"),
            opening_crawl=input.get("opening_crawl") or "",
            director=director,
        )

        if input.get("producer_ids"):
            producers = [
                relay.Node.get_node_from_global_id(info, pid, only_type=PersonNode)
                for pid in input["producer_ids"]
            ]
            movie.producers.set(producers)

        if input.get("planet_ids"):
            planets = [
                relay.Node.get_node_from_global_id(info, pid, only_type=PlanetNode)
                for pid in input["planet_ids"]
            ]
            movie.planets.set(planets)

        if input.get("character_ids"):
            characters = [
                relay.Node.get_node_from_global_id(info, cid, only_type=CharacterNode)
                for cid in input["character_ids"]
            ]
            movie.characters.set(characters)

        movie.save()
        return CreateMovie(movie=movie)


class UpdateMovie(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        title = graphene.String(required=False)
        release_date = graphene.Date(required=False)
        opening_crawl = graphene.String(required=False)
        director_id = graphene.ID(required=False)
        producer_ids = graphene.List(graphene.ID, required=False)
        planet_ids = graphene.List(graphene.ID, required=False)
        character_ids = graphene.List(graphene.ID, required=False)

    movie = graphene.Field(MovieNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        movie = relay.Node.get_node_from_global_id(info, input["id"], only_type=MovieNode)
        if not movie:
            raise Exception("Movie not found")

        if input.get("title"):
            movie.title = input["title"]
        if input.get("release_date"):
            movie.release_date = input["release_date"]
        if input.get("opening_crawl"):
            movie.opening_crawl = input["opening_crawl"]
        if input.get("director_id"):
            movie.director = relay.Node.get_node_from_global_id(info, input["director_id"], only_type=PersonNode)
        if input.get("producer_ids"):
            movie.producers.set([
                relay.Node.get_node_from_global_id(info, pid, only_type=PersonNode)
                for pid in input["producer_ids"]
            ])
        if input.get("planet_ids"):
            movie.planets.set([
                relay.Node.get_node_from_global_id(info, pid, only_type=PlanetNode)
                for pid in input["planet_ids"]
            ])
        if input.get("character_ids"):
            movie.characters.set([
                relay.Node.get_node_from_global_id(info, cid, only_type=CharacterNode)
                for cid in input["character_ids"]
            ])

        movie.save()
        return UpdateMovie(movie=movie)


class DeleteMovie(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        movie = relay.Node.get_node_from_global_id(info, id, only_type=MovieNode)
        if not movie:
            return DeleteMovie(ok=False, message="Movie not found")

        movie.delete()
        return DeleteMovie(ok=True, message="Movie deleted successfully")

class Mutation(graphene.ObjectType):
    create_planet = CreatePlanet.Field()
    create_character = CreateCharacter.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
