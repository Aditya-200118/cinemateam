from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from accounts.models import Customer, Address, Card
from booking.models import Booking, Ticket, TicketType, Promotion, MovieTicketTypeDiscount
from movie.models import Theatre, Showroom, Movie, Screening
from decimal import Decimal
from math import floor
class Command(BaseCommand):
    help = "Populate the database with dummy data for development and testing purposes."

    def handle(self, *args, **kwargs):
        from django.core.management import call_command
        call_command("flush", verbosity=0, interactive=False)
        # Create superuser
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
            superuser.objects.create_superuser(
                email="root@root.com", first_name="root", last_name="root", password="root@root", is_active = True, is_staff = True
        )
        # Create unique addresses for each customer
        addresses = [
            Address.objects.create(
                billing_address="123 Main St", city="Athens", state="GA", zip_code="30601"
            ),
            Address.objects.create(
                billing_address="456 Elm St", city="Atlanta", state="GA", zip_code="30301"
            ),
            Address.objects.create(
                billing_address="789 Oak St", city="Savannah", state="GA", zip_code="31401"
            ),
            Address.objects.create(
                billing_address="321 Pine St", city="Augusta", state="GA", zip_code="30901"
            ),
            Address.objects.create(
                billing_address="654 Cedar St",
                city="Columbus",
                state="GA",
                zip_code="31901",
            ),
        ]
        # Create customers with unique addresses
        customers = [
            Customer.objects.create(
                first_name="Daniel",
                last_name="Smith",
                email="daniel.smith@example.com",
                password=make_password("password123"),
                address=addresses[0],
                promotions=True,
            ),
            Customer.objects.create(
                first_name="Jane",
                middle_name="Lee",
                last_name="Grey",
                email="jane.lee@example.com",
                password=make_password("password123"),
                address=addresses[1],
                promotions=False,
            ),
            Customer.objects.create(
                first_name="Emily",
                last_name="Johnson",
                email="emily.johnson@example.com",
                password=make_password("password123"),
                address=addresses[2],
            ),
            Customer.objects.create(
                first_name="Michael",
                last_name="Brown",
                email="michael.brown@example.com",
                password=make_password("password123"),
                address=addresses[3],
            ),
            Customer.objects.create(
                first_name="Sarah",
                last_name="Davis",
                email="sarah.davis@example.com",
                password=make_password("password123"),
                address=addresses[4],
            ),
        ]
        # Create cards
        cards = [
            Card(
                customer=customers[0],
                card_name="John's Visa",
                card_number="4111111111111111",
                expiry_date="12/25",
                cvv="123",
            ),
            Card(
                customer=customers[1],
                card_name="Jane's Visa",
                card_number="4111111111111112",
                expiry_date="11/24",
                cvv="124",
            ),
            Card(
                customer=customers[2],
                card_name="Emily's MasterCard",
                card_number="5111111111111111",
                expiry_date="10/26",
                cvv="125",
            ),
            Card(
                customer=customers[3],
                card_name="Michael's Amex",
                card_number="371449635398431",
                expiry_date="09/27",
                cvv="126",
            ),
            Card(
                customer=customers[4],
                card_name="Sarah's Discover",
                card_number="6011514433546201",
                expiry_date="08/25",
                cvv="127",
            ),
        ]
        for card in cards:
            card.save()
        # Create Ticket Types
        ticket_types = [
            TicketType.objects.create(type=TicketType.CHILD),
            TicketType.objects.create(type=TicketType.SENIOR),
            TicketType.objects.create(type=TicketType.ADULT),
        ]
        # Create theatres
        theatres = [
            Theatre.objects.create(name="The Grand Theatre"),
            Theatre.objects.create(name="Cinema Paradise"),
            Theatre.objects.create(name="Regal Cinema"),
            Theatre.objects.create(name="Cineplex 21"),
            Theatre.objects.create(name="AMC Deluxe"),
        ]
        # Create showrooms with names
        showroom_names = ["A", "B", "C"]
        for theatre in theatres:
            for name in showroom_names:
                Showroom.objects.create(
                    seat_count=random.randint(80, 200),
                    name=f"{theatre.name} {name}",
                    theatre=theatre,
                )
        # Movie data with real titles
            movies_data = [
            (
                "Avatar: The Way of Water",
                "Action/Adventure/Sci-Fi",
                ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver", "Stephen Lang"],
                "James Cameron",
                "James Cameron",
                "Jake Sully and Ney'tiri, now parents, must leave their home and explore the regions of Pandora to face a renewed threat from the RDA.",
                "https://www.youtube.com/watch?v=d9MyW72ELq0",
                "PG-13",
                "2022-12-16",
                "movie/posters/avatar.jpg",
                192,
            ),
            (
                "Spider-Man: Across the Spider-Verse",
                "Animation/Action/Adventure",
                ["Shameik Moore", "Hailee Steinfeld", "Oscar Isaac", "Jake Johnson"],
                "Joaquim Dos Santos",
                "Amy Pascal",
                "Miles Morales returns for the next chapter of the Spider-Verse saga, facing off against a powerful new villain across multiple dimensions.",
                "https://www.youtube.com/watch?v=cqGjhVJWtEg",
                "PG",
                "2023-06-02",
                "movie/posters/spiderman.jpg",
                140,
            ),
            (
                "Oppenheimer",
                "Drama/History",
                ["Cillian Murphy", "Emily Blunt", "Matt Damon", "Robert Downey Jr."],
                "Christopher Nolan",
                "Emma Thomas",
                "The story of J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
                "https://www.youtube.com/watch?v=bK6ldnjE3Y0",
                "R",
                "2023-07-21",
                "movie/posters/openhimer.jpg",
                180,
            ),
            (
                "The Super Mario Bros. Movie",
                "Animation/Adventure/Comedy",
                ["Chris Pratt", "Anya Taylor-Joy", "Charlie Day", "Jack Black"],
                "Aaron Horvath",
                "Chris Meledandri",
                "The iconic plumber Mario travels through the Mushroom Kingdom with Princess Peach to save his brother, Luigi, from Bowser.",
                "https://www.youtube.com/watch?v=TnGl01FkMMo",
                "PG",
                "2023-04-05",
                "movie/posters/mario.jpg",
                92,
            ),
            (
                "Dune: Part Two",
                "Adventure/Drama/Sci-Fi",
                ["Timothée Chalamet", "Zendaya", "Rebecca Ferguson", "Josh Brolin"],
                "Denis Villeneuve",
                "Denis Villeneuve",
                "Paul Atreides unites with Chani and the Fremen to seek revenge against those who destroyed his family, while confronting a prophecy of a great war.",
                "https://www.youtube.com/watch?v=Way9Dexny3w",
                "PG-13",
                "2024-03-15",
                "movie/posters/dune.jpg",
                165,
            ),
            (
                "Barbie",
                "Comedy/Fantasy",
                ["Margot Robbie", "Ryan Gosling", "Simu Liu", "America Ferrera"],
                "Greta Gerwig",
                "Margot Robbie",
                "Barbie suffers a crisis that leads her to question her world and her existence.",
                "https://www.youtube.com/watch?v=pBk4NYhWNMM",
                "PG-13",
                "2023-07-21",
                "movie/posters/barbie.jpg",
                114,
            ),
            (
                "Guardians of the Galaxy Vol. 3",
                "Action/Adventure/Comedy",
                ["Chris Pratt", "Zoe Saldana", "Dave Bautista", "Bradley Cooper"],
                "James Gunn",
                "Kevin Feige",
                "The Guardians must band together to protect one of their own as they uncover secrets of Rocket's past.",
                "https://www.youtube.com/watch?v=u3V5KDHRQvk",
                "PG-13",
                "2023-05-05",
                "movie/posters/GOG3.jpeg",
                149,
            ),
            (
                "John Wick: Chapter 4",
                "Action/Thriller",
                ["Keanu Reeves", "Laurence Fishburne", "Ian McShane", "Donnie Yen"],
                "Chad Stahelski",
                "Basil Iwanyk",
                "John Wick faces his deadliest adversaries yet as he seeks out a path to defeating the High Table.",
                "https://www.youtube.com/watch?v=qEVUtrk8_B4",
                "R",
                "2023-03-24",
                "movie/posters/jhon wick.jpg",
                169,
            ),
            (
                "Black Panther: Wakanda Forever",
                "Action/Adventure/Drama",
                ["Letitia Wright", "Lupita Nyong'o", "Danai Gurira", "Winston Duke"],
                "Ryan Coogler",
                "Kevin Feige",
                "The people of Wakanda fight to protect their home from intervening world powers as they mourn the death of King T'Challa.",
                "https://www.youtube.com/watch?v=_Z3QKkl1WyM",
                "PG-13",
                "2022-11-11",
                "movie/posters/black panther2.jpg",
                161,
            ),
            (
                "The Marvels",
                "Action/Adventure/Sci-Fi",
                ["Brie Larson", "Teyonah Parris", "Iman Vellani", "Samuel L. Jackson"],
                "Nia DaCosta",
                "Kevin Feige",
                "Carol Danvers, Kamala Khan, and Monica Rambeau join forces to save the universe.",
                "https://www.youtube.com/watch?v=wS_qbDztgVY",
                "PG-13",
                "2023-11-10",
                "movie/posters/the marvels.jpg",
                105,
            ),
            (
                "Mission: Impossible – Dead Reckoning Part One",
                "Action/Adventure/Thriller",
                ["Tom Cruise", "Hayley Atwell", "Ving Rhames", "Simon Pegg"],
                "Christopher McQuarrie",
                "Tom Cruise",
                "Ethan Hunt and his IMF team must track down a terrifying new weapon that threatens all of humanity.",
                "https://www.youtube.com/watch?v=avz06PDqDbM",
                "PG-13",
                "2023-07-12",
                "movie/posters/mission imposible.jpg",
                163,
            ),
            (
                "Fast X",
                "Action/Crime/Thriller",
                ["Vin Diesel", "Michelle Rodriguez", "Jordana Brewster", "Jason Momoa"],
                "Louis Leterrier",
                "Vin Diesel",
                "Dom Toretto and his family confront the most lethal opponent they've ever faced—a vengeful nemesis fueled by blood feud.",
                "https://www.youtube.com/watch?v=aOb15GVFZxU",
                "PG-13",
                "2023-05-19",
                "movie/posters/fast X.jpg",
                141,
            ),
            (
                "Elemental",
                "Animation/Adventure/Comedy",
                ["Leah Lewis", "Mamoudou Athie", "Ronnie del Carmen", "Shila Ommi"],
                "Peter Sohn",
                "Denise Ream",
                "In a city where fire, water, land, and air residents live together, a fiery young woman and a go-with-the-flow guy discover something elemental: how much they actually have in common.",
                "https://www.youtube.com/watch?v=hXzcyx9V0xw",
                "PG",
                "2024-12-16",
                "movie/posters/elemental.jpg",
                109,
            ),
            (
                "The Flash",
                "Action/Adventure/Sci-Fi",
                ["Ezra Miller", "Michael Keaton", "Sasha Calle", "Ben Affleck"],
                "Andy Muschietti",
                "Barbara Muschietti",
                "Barry Allen uses his super speed to change the past, but his attempt to save his family creates a world without heroes, forcing him to race for his life.",
                "https://www.youtube.com/watch?v=hebWYacbdvc",
                "PG-13",
                "2024-12-20",
                "movie/posters/the flash.jpg",
                144,
            ),
            (
                "The Hunger Games: The Ballad of Songbirds and Snakes",
                "Adventure/Drama/Sci-Fi",
                ["Tom Blyth", "Rachel Zegler", "Hunter Schafer", "Jason Schwartzman"],
                "Francis Lawrence",
                "Nina Jacobson",
                "Years before he would become the tyrannical president of Panem, young Coriolanus Snow mentors a tribute in the 10th Hunger Games.",
                "https://www.youtube.com/watch?v=RDE6Uz73A7g",
                "PG-13",
                "2023-12-25",
                "movie/posters/hungergame.jpg",
                157,
            ),
        ]
        today = timezone.now()
        one_year_ago = today - timedelta(days=365)
        # Create movies and discounts
        for (
            title,
            category,
            cast,
            director,
            producer,
            synopsis,
            trailer_url,
            rating,
            release_date,
            poster,
            duration
        ) in movies_data:
            # release_date = one_year_ago + timedelta(days=random.randint(0, 365))
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
                duration=duration,
                price=Decimal(random.uniform(50.0, 70.0)),  # Ensure price is Decimal
            )

            # Define dynamic discounts as a percentage of the movie price
            child_discount = movie.price * Decimal('0.25')  # 25% of the movie price
            senior_discount = movie.price * Decimal('0.50')  # 50% of the movie price
            adult_discount = movie.price * Decimal('0.00')  # 0% of the movie price

            # Ensure no discount exceeds 50% of the movie price
            child_discount = floor(min(child_discount, movie.price * Decimal('0.50')))
            senior_discount = floor(min(senior_discount, movie.price * Decimal('0.50')))
            adult_discount = floor(min(adult_discount, movie.price * Decimal('0.50')))

            # Create MovieTicketTypeDiscount objects with floored discounts
            MovieTicketTypeDiscount.objects.create(
                movie=movie, ticket_type=ticket_types[0], discount=child_discount
            )
            MovieTicketTypeDiscount.objects.create(
                movie=movie, ticket_type=ticket_types[1], discount=senior_discount
            )
            MovieTicketTypeDiscount.objects.create(
                movie=movie, ticket_type=ticket_types[2], discount=adult_discount
            )
            # Create screenings for each showroom
            for showroom in Showroom.objects.filter(theatre__in=theatres):
                for _ in range(3):
                        # Generate a random number of days and hours within the desired range
                    random_days = random.randint(-10, 10)
                    random_hour = random.randint(8, 23)  # Range is 8:00 to 23:00
                    
                    # Generate minutes as a multiple of 5
                    random_minutes = random.randint(0, 11) * 5  # 0, 5, 10, ..., 55
                    
                    # Combine to create the show time
                    show_time = today + timedelta(days=random_days, hours=random_hour, minutes=random_minutes)
                    
                    Screening.objects.create(
                        movie=movie, showroom=showroom, show_time=show_time
                    )
        # Create promotions with title and description
        promotions = [
            # Currently active promotions (start date set to yesterday)
            Promotion.objects.create(
                promo_code="MOVIE10",
                title="Movie Discount",
                description="Enjoy 10% off on any movie ticket.",
                discount=10,
                valid_from=(today - timedelta(days=1)).date(),
                valid_to=(today + timedelta(days=30)).date(),
            ),
            Promotion.objects.create(
                promo_code="CINEMA20",
                title="Cinema Sale",
                description="Get 20% off on tickets this month.",
                discount=20,
                valid_from=(today - timedelta(days=1)).date(),
                valid_to=(today + timedelta(days=60)).date(),
            ),
            Promotion.objects.create(
                promo_code="WELCOME15",
                title="Welcome Offer",
                description="New customers get 15% off on their first ticket.",
                discount=15,
                valid_from=(today - timedelta(days=1)).date(),
                valid_to=(today + timedelta(days=15)).date(),
            ),
            Promotion.objects.create(
                promo_code="FAMILY25",
                title="Family Discount",
                description="Save 25% when booking tickets for your family.",
                discount=25,
                valid_from=(today - timedelta(days=1)).date(),
                valid_to=(today + timedelta(days=45)).date(),
            ),
            Promotion.objects.create(
                promo_code="EVENING10",
                title="Evening Special",
                description="Get 10% off on evening shows after 6 PM.",
                discount=10,
                valid_from=(today - timedelta(days=1)).date(),
                valid_to=(today + timedelta(days=30)).date(),
            ),

            # Future promotions (start date is 5 days or 1 month from today)
            Promotion.objects.create(
                promo_code="WEEKDAY15",
                title="Weekday Special",
                description="Save 15% on tickets for shows Monday to Thursday.",
                discount=15,
                valid_from=(today + timedelta(days=5)).date(),  # Starts in 5 days
                valid_to=(today + timedelta(days=95)).date(),
            ),
            Promotion.objects.create(
                promo_code="FLASH40",
                title="Flash Sale",
                description="Enjoy 40% off on tickets for the next 24 hours.",
                discount=40,
                valid_from=(today + timedelta(days=30)).date(),  # Starts in 1 month
                valid_to=(today + timedelta(days=31)).date(),
            ),
            Promotion.objects.create(
                promo_code="LOYALTY10",
                title="Loyalty Reward",
                description="Regular customers get 10% off on all bookings.",
                discount=10,
                valid_from=(today + timedelta(days=5)).date(),  # Starts in 5 days
                valid_to=(today + timedelta(days=125)).date(),
            ),
            Promotion.objects.create(
                promo_code="WEEKEND20",
                title="Weekend Special",
                description="Enjoy 20% off on weekend movie tickets.",
                discount=20,
                valid_from=(today + timedelta(days=30)).date(),  # Starts in 1 month
                valid_to=(today + timedelta(days=90)).date(),
            ),
            Promotion.objects.create(
                promo_code="SUMMER15",
                title="Summer Blockbuster",
                description="Get 15% off on tickets for this summer’s hits.",
                discount=15,
                valid_from=(today + timedelta(days=5)).date(),  # Starts in 5 days
                valid_to=(today + timedelta(days=95)).date(),
            ),
        ]