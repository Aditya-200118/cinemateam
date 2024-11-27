# movie/models/theatre_models.py

from . import *

class Theatre(models.Model):
    theatre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def add_theatre(self, name):
        theatre = Theatre(name=name)
        theatre.save()
        return theatre

    def update_theatre(self, name):
        self.name = name
        self.save()

    def get_theatre_details(self):
        return {
            "theatre_id": self.theatre_id,
            "name": self.name
        }

    def __str__(self):
        return self.name