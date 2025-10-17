from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Character(Person):
    alias = models.CharField(max_length=100, blank=True, null=True)
    specie = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

class Planets(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="directed_movies")
    producers = models.ManyToManyField(Person, related_name="produced_movies")
    characters = models.ManyToManyField(Character, related_name="character_movies")
    planets = models.ManyToManyField(Planets, related_name="planet_movies")
    opening_crawl = models.TextField()

    def __str__(self):
        return self.title
