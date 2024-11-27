from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from accounts.models import Customer, Address, Card
from booking.models import Booking, Ticket, TicketType, Promotion, MovieTicketTypeDiscount
from movie.models import Theatre, Showroom, Movie, Screening

class Command(BaseCommand):
    help = "Populate the database with dummy data for development and testing purposes."

    def handle(self, *args, **kwargs):
        from django.core.management import call_command
        call_command('flush', verbosity=0, interactive=False)
        Address.objects.all().delete()
        Customer.objects.all().delete()
        Card.objects.all().delete()
        TicketType.objects.all().delete()
        Promotion.objects.all().delete()
        MovieTicketTypeDiscount.objects.all().delete()
        Screening.objects.all().delete()
        Showroom.objects.all().delete()
        Theatre.objects.all().delete()
        Movie.objects.all().delete()
        superuser = get_user_model()
        if not superuser.objects.filter(email="root@root.com").exists():
            superuser.objects.create_superuser(email="root@root.com", first_name="root", last_name="root", password="root")
        addresses = [
            Address.objects.create(billing_address="123 Main St", city="Athens", state="GA", zip_code="30601"),
            Address.objects.create(billing_address="456 Elm St", city="Atlanta", state="GA", zip_code="30301"),
            Address.objects.create(billing_address="789 Oak St", city="Savannah", state="GA", zip_code="31401"),
            Address.objects.create(billing_address="321 Pine St", city="Augusta", state="GA", zip_code="30901"),
            Address.objects.create(billing_address="654 Cedar St", city="Columbus", state="GA", zip_code="31901"),
        ]
        customers = [
            Customer.objects.create(first_name="", last_name="", email="", password=make_password("password123"), address=addresses[0], promotions=True),
            Customer.objects.create(first_name="David", last_name="Lee", email="jane.bhargavaaditya200117@gmail.com", password=make_password("password123"), address=addresses[1], promotions=False),
            Customer.objects.create(first_name="Emily", last_name="Johnson", email="emily.johnson@example.com", password=make_password("password123"), address=addresses[2]),
            Customer.objects.create(first_name="Michael", last_name="Brown", email="michael.brown@example.com", password=make_password("password123"), address=addresses[3]),
            Customer.objects.create(first_name="Sarah", last_name="Davis", email="sarah.davis@example.com", password=make_password("password123"), address=addresses[4]),
        ]
        cards = [
            Card(customer=customers[0], card_name="John's Visa", card_number="4111111111111111", expiry_date="12/25", cvv="123"),
            Card(customer=customers[1], card_name="Jane's Visa", card_number="4111111111111112", expiry_date="11/24", cvv="124"),
            Card(customer=customers[2], card_name="Emily's MasterCard", card_number="5111111111111111", expiry_date="10/26", cvv="125"),
            Card(customer=customers[3], card_name="Michael's Amex", card_number="371449635398431", expiry_date="09/27", cvv="126"),
            Card(customer=customers[4], card_name="Sarah's Discover", card_number="6011514433546201", expiry_date="08/25", cvv="127"),
        ]
        for card in cards:
            card.save()
        ticket_types = [
            TicketType.objects.create(type=TicketType.CHILD),
            TicketType.objects.create(type=TicketType.SENIOR),
            TicketType.objects.create(type=TicketType.ADULT),
        ]
        theatres = [
            Theatre.objects.create(name="The Grand Theatre"),
            Theatre.objects.create(name="Cinema Paradise"),
            Theatre.objects.create(name="Regal Cinema"),
            Theatre.objects.create(name="Cineplex 21"),
            Theatre.objects.create(name="AMC Deluxe"),
        ]
        showroom_names = ["A", "B", "C"]
        for theatre in theatres:
            for name in showroom_names:
                Showroom.objects.create(seat_count=random.randint(80, 200), name=f"{theatre.name} {name}", theatre=theatre)
        movies_data = [
            ("Avatar: The Way of Water", "Action/Adventure/Sci-Fi", ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver", "Stephen Lang"], "James Cameron", "James Cameron", "Jake Sully and Ney'tiri, now parents, must leave their home and explore the regions of Pandora to face a renewed threat from the RDA.", "https://www.youtube.com/watch?v=d9MyW72ELq0", "PG-13", "2022-12-16", "movie/posters/avatar.jpg"),
            ("Spider-Man: Across the Spider-Verse", "Animation/Action/Adventure", ["Shameik Moore", "Hailee Steinfeld", "Oscar Isaac", "Jake Johnson"], "Joaquim Dos Santos", "Amy Pascal", "Miles Morales returns for the next chapter of the Spider-Verse saga, facing off against a powerful new villain across multiple dimensions.", "https://www.youtube.com/watch?v=cqGjhVJWtEg", "PG", "2023-06-02", "movie/posters/spiderman.jpg"),
            ("Oppenheimer", "Drama/History", ["Cillian Murphy", "Emily Blunt", "Matt Damon", "Robert Downey Jr."], "Christopher Nolan", "Emma Thomas", "The story of J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.", "https://www.youtube.com/watch?v=bK6ldnjE3Y0", "R", "2023-07-21", "movie/posters/openhimer.jpg"),
            ("The Super Mario Bros. Movie", "Animation/Adventure/Comedy", ["Chris Pratt", "Anya Taylor-Joy", "Charlie Day", "Jack Black"], "Aaron Horvath", "Chris Meledandri", "The iconic plumber Mario travels through the Mushroom Kingdom with Princess Peach to save his brother, Luigi, from Bowser.", "https://www.youtube.com/watch?v=TnGl01FkMMo", "PG", "2023-04-05", "movie/posters/mario.jpg"),
            ("Dune: Part Two", "Adventure/Drama/Sci-Fi", ["Timothée Chalamet", "Zendaya", "Rebecca Ferguson", "Josh Brolin"], "Denis Villeneuve", "Denis Villeneuve", "Paul Atreides unites with Chani and the Fremen to seek revenge against those who destroyed his family, while confronting a prophecy of a great war.", "https://www.youtube.com/watch?v=Way9Dexny3w", "PG-13", "2025-03-15", "movie/posters/dune.jpg"),
        ]
        today = timezone.now()
        for title, category, cast, director, producer, synopsis, trailer_url, rating, release_date, poster in movies_data:
            movie = Movie.objects.create(
                title=title,
                category=category,
                cast=cast,
                director=director,
                producer=producer,
                synopsis=synopsis,
                reviews="Fantastic!",
                trailer_url=trailer_url,
                rating=rating,
                release_date=release_date,
                poster=poster,
                duration=random.uniform(120, 360),
                price=random.uniform(50.0, 70.0),
            )
            MovieTicketTypeDiscount.objects.create(movie=movie, ticket_type=ticket_types[0], discount=15.0)
            MovieTicketTypeDiscount.objects.create(movie=movie, ticket_type=ticket_types[1], discount=30.0)
            MovieTicketTypeDiscount.objects.create(movie=movie, ticket_type=ticket_types[2], discount=0.0)
            for showroom in Showroom.objects.filter(theatre__in=theatres):
                for _ in range(3):
                    show_time = today + timedelta(days=random.randint(-10, 10), hours=random.randint(8, 22))
                    Screening.objects.create(movie=movie, showroom=showroom, show_time=show_time)
        promotions = [
            Promotion.objects.create(promo_code="SAVE10", title="Save 10%", description="Get 10% off on your purchase.", discount=10, valid_from=today.date(), valid_to=(today + timedelta(days=30)).date()),
            Promotion.objects.create(promo_code="SUMMER20", title="Summer Sale", description="Enjoy 20% off this summer.", discount=20, valid_from=today.date(), valid_to=(today + timedelta(days=60)).date()),
            Promotion.objects.create(promo_code="WELCOME5", title="Welcome Discount", description="Get 5% off on your first purchase.", discount=5, valid_from=today.date(), valid_to=(today + timedelta(days=15)).date()),
        ]