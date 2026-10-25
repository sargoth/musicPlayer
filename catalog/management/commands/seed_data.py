import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from catalog.models import Genre, Artist, Album
from playlists.models import Playlist
from tracks.models import Track


class Command(BaseCommand):
    help = "Seeds the database with realistic, meaningful music data (20+ records for all tables)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seed..."))

        with transaction.atomic():
            # 1. Clean existing records for a fresh, clean state
            Playlist.objects.all().delete()
            Track.objects.all().delete()
            Album.objects.all().delete()
            Artist.objects.all().delete()
            Genre.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

            # ---------------------------------------------------------
            # 1. GENRES (24 distinct meaningful genres)
            # ---------------------------------------------------------
            genre_names = [
                "rock", "pop", "rap", "hip_hop", "electronic", "jazz",
                "classical", "r_and_b", "indie", "metal", "lo_fi", "blues",
                "soul", "country", "folk", "reggae", "punk", "disco",
                "funk", "house", "techno", "ambient", "soundtrack", "latin"
            ]

            genres = {}
            for g_name in genre_names:
                genre, _ = Genre.objects.get_or_create(name=g_name)
                genres[g_name] = genre

            self.stdout.write(self.style.SUCCESS(f"Created {len(genres)} genres."))

            # ---------------------------------------------------------
            # 2. ARTISTS (24 iconic artists with real biographies & images)
            # ---------------------------------------------------------
            artists_data = [
                {
                    "name": "Queen",
                    "bio": "British rock band formed in London in 1970 by Freddie Mercury, Brian May, Roger Taylor, and John Deacon. Celebrated for theatrical anthems, vocal harmonies, and dynamic live stadium performances.",
                    "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "pop"]
                },
                {
                    "name": "Pink Floyd",
                    "bio": "English rock band formed in London in 1965. Pioneers of psychedelic and progressive rock, renowned for philosophical lyrics, sonic experimentation, and elaborate live spectacles.",
                    "image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "indie"]
                },
                {
                    "name": "The Beatles",
                    "bio": "Formed in Liverpool in 1960, The Beatles revolutionized popular music and culture with their infectious pop melodies, avant-garde studio innovation, and enduring songwriting genius.",
                    "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "pop"]
                },
                {
                    "name": "Michael Jackson",
                    "bio": "Known globally as the 'King of Pop', Michael Jackson was one of the 20th century's most significant cultural figures, famous for revolutionary choreography and timeless crossover hits.",
                    "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80",
                    "genres": ["pop", "r_and_b", "soul"]
                },
                {
                    "name": "Daft Punk",
                    "bio": "Legendary French electronic music duo formed in Paris in 1993 by Thomas Bangalter and Guy-Manuel de Homem-Christo. Pioneers of French touch house music with iconic robot personas.",
                    "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80",
                    "genres": ["electronic", "house", "disco"]
                },
                {
                    "name": "Kendrick Lamar",
                    "bio": "Pulitzer Prize-winning American rapper and songwriter known for cinematic storytelling, sharp social commentary, and boundary-pushing production that reshaped modern hip-hop.",
                    "image_url": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80",
                    "genres": ["hip_hop", "rap"]
                },
                {
                    "name": "Miles Davis",
                    "bio": "American trumpeter and composer among the most influential figures in the history of jazz. Davis continually spearheaded pivotal stylistic developments from bebop to jazz fusion.",
                    "image_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80",
                    "genres": ["jazz"]
                },
                {
                    "name": "Adele",
                    "bio": "English singer-songwriter recognized worldwide for her soulful mezzo-soprano voice and emotionally vulnerable ballads detailing love, heartache, and resilience.",
                    "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80",
                    "genres": ["pop", "soul", "r_and_b"]
                },
                {
                    "name": "Bob Marley",
                    "bio": "Jamaican reggae pioneer, singer, and songwriter who popularized reggae globally, blending spirituality, social consciousness, and message-driven roots music.",
                    "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80",
                    "genres": ["reggae"]
                },
                {
                    "name": "Hans Zimmer",
                    "bio": "German film score composer and music producer who has scored over 150 projects, crafting unforgettable sweeping orchestral and electronic soundscapes for major cinema.",
                    "image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80",
                    "genres": ["soundtrack", "classical"]
                },
                {
                    "name": "Radiohead",
                    "bio": "English rock band formed in Abingdon in 1985. Praised for experimental art rock, seamless electronic integration, and introspective themes reflecting technological modern life.",
                    "image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "indie", "electronic"]
                },
                {
                    "name": "Taylor Swift",
                    "bio": "Critically acclaimed singer-songwriter known for transparent narrative songwriting, narrative world-building, and artistic evolution traversing country, synth-pop, and indie folk.",
                    "image_url": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?auto=format&fit=crop&w=800&q=80",
                    "genres": ["pop", "country", "folk"]
                },
                {
                    "name": "Led Zeppelin",
                    "bio": "English hard rock group formed in 1968. With heavy guitar riffs, blues sensibilities, and mythical folklore themes, they helped forge heavy metal and stadium rock.",
                    "image_url": "https://images.unsplash.com/photo-1517230878791-4d28214057c2?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "metal", "blues"]
                },
                {
                    "name": "Stevie Wonder",
                    "bio": "American singer, songwriter, and multi-instrumentalist whose masterworks defined 1970s soul, funk, and R&B with virtuosic keyboard grooves and joyful messages of unity.",
                    "image_url": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80",
                    "genres": ["soul", "funk", "r_and_b"]
                },
                {
                    "name": "Billie Eilish",
                    "bio": "Grammy and Oscar-winning American singer-songwriter famed for whisper-intimate vocals, dark minimalist basslines, and authentic Gen Z pop innovation.",
                    "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80",
                    "genres": ["pop", "indie", "electronic"]
                },
                {
                    "name": "Nirvana",
                    "bio": "Seattle grunge trio fronted by Kurt Cobain that defined early 1990s alternative rock, channeling raw punk angst and infectious melody into historic cultural anthems.",
                    "image_url": "https://images.unsplash.com/photo-1487180144351-b8472da7d491?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "punk"]
                },
                {
                    "name": "B.B. King",
                    "bio": "The 'King of the Blues', an icon whose stinging vibrato guitar solos on 'Lucille' and impassioned vocal delivery anchored modern electric Chicago blues.",
                    "image_url": "https://images.unsplash.com/photo-1513829596324-4bb2800c5efb?auto=format&fit=crop&w=800&q=80",
                    "genres": ["blues"]
                },
                {
                    "name": "Johnny Cash",
                    "bio": "'The Man in Black', one of country and Americana's greatest storytellers, whose deep bass-baritone voice resonated across themes of redemption, hardship, and rebellion.",
                    "image_url": "https://images.unsplash.com/photo-1526478806334-5fd488fcaabc?auto=format&fit=crop&w=800&q=80",
                    "genres": ["country", "folk", "rock"]
                },
                {
                    "name": "Nina Simone",
                    "bio": "Incomparable singer, pianist, and civil rights icon whose deep vocal resonance united classical counterpoint, blues melancholy, and impassioned soul.",
                    "image_url": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80",
                    "genres": ["jazz", "blues", "soul"]
                },
                {
                    "name": "Metallica",
                    "bio": "Founding fathers of thrash metal formed in Los Angeles in 1981, renowned for lightning speed, technical precision, and enduring global stadium dominance.",
                    "image_url": "https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=800&q=80",
                    "genres": ["metal", "rock"]
                },
                {
                    "name": "Arctic Monkeys",
                    "bio": "Sheffield indie rock band fronted by Alex Turner, acclaimed for razor-sharp observational lyrics, infectious post-punk revival grooves, and suave retro rock.",
                    "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
                    "genres": ["indie", "rock"]
                },
                {
                    "name": "ABBA",
                    "bio": "Swedish pop sensation whose soaring harmonies, sparkling European disco hooks, and immaculate songwriting made them one of history's most beloved pop acts.",
                    "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80",
                    "genres": ["pop", "disco"]
                },
                {
                    "name": "David Bowie",
                    "bio": "The chameleon of rock and roll, David Bowie consistently revolutionized music, fashion, and art through groundbreaking personas like Ziggy Stardust and the Thin White Duke.",
                    "image_url": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80",
                    "genres": ["rock", "pop", "electronic"]
                },
                {
                    "name": "Ludovico Einaudi",
                    "bio": "Italian pianist and contemporary classical composer renowned for meditative, cinematic piano compositions that blend minimalist beauty with evocative strings.",
                    "image_url": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=800&q=80",
                    "genres": ["classical", "ambient"]
                }
            ]

            artists = {}
            for item in artists_data:
                artist = Artist.objects.create(
                    name=item["name"],
                    bio=item["bio"],
                    image_url=item["image_url"]
                )
                genre_objs = [genres[g] for g in item["genres"] if g in genres]
                artist.genres.set(genre_objs)
                artists[item["name"]] = artist

            self.stdout.write(self.style.SUCCESS(f"Created {len(artists)} artists."))

            # ---------------------------------------------------------
            # 3. ALBUMS (28 iconic albums)
            # ---------------------------------------------------------
            albums_data = [
                {
                    "title": "A Night at the Opera",
                    "artist": "Queen",
                    "release_year": 1975,
                    "cover_image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "The Dark Side of the Moon",
                    "artist": "Pink Floyd",
                    "release_year": 1973,
                    "cover_image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Wish You Were Here",
                    "artist": "Pink Floyd",
                    "release_year": 1975,
                    "cover_image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Abbey Road",
                    "artist": "The Beatles",
                    "release_year": 1969,
                    "cover_image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Thriller",
                    "artist": "Michael Jackson",
                    "release_year": 1982,
                    "cover_image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Discovery",
                    "artist": "Daft Punk",
                    "release_year": 2001,
                    "cover_image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Random Access Memories",
                    "artist": "Daft Punk",
                    "release_year": 2013,
                    "cover_image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "To Pimp a Butterfly",
                    "artist": "Kendrick Lamar",
                    "release_year": 2015,
                    "cover_image_url": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "good kid, m.A.A.d city",
                    "artist": "Kendrick Lamar",
                    "release_year": 2012,
                    "cover_image_url": "https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Kind of Blue",
                    "artist": "Miles Davis",
                    "release_year": 1959,
                    "cover_image_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "21",
                    "artist": "Adele",
                    "release_year": 2011,
                    "cover_image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Exodus",
                    "artist": "Bob Marley",
                    "release_year": 1977,
                    "cover_image_url": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Interstellar (Original Motion Picture Soundtrack)",
                    "artist": "Hans Zimmer",
                    "release_year": 2014,
                    "cover_image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "OK Computer",
                    "artist": "Radiohead",
                    "release_year": 1997,
                    "cover_image_url": "https://images.unsplash.com/photo-1487180144351-b8472da7d491?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "1989",
                    "artist": "Taylor Swift",
                    "release_year": 2014,
                    "cover_image_url": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Folklore",
                    "artist": "Taylor Swift",
                    "release_year": 2020,
                    "cover_image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Led Zeppelin IV",
                    "artist": "Led Zeppelin",
                    "release_year": 1971,
                    "cover_image_url": "https://images.unsplash.com/photo-1517230878791-4d28214057c2?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Songs in the Key of Life",
                    "artist": "Stevie Wonder",
                    "release_year": 1976,
                    "cover_image_url": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "When We All Fall Asleep, Where Do We Go?",
                    "artist": "Billie Eilish",
                    "release_year": 2019,
                    "cover_image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Nevermind",
                    "artist": "Nirvana",
                    "release_year": 1991,
                    "cover_image_url": "https://images.unsplash.com/photo-1526478806334-5fd488fcaabc?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Live at the Regal",
                    "artist": "B.B. King",
                    "release_year": 1965,
                    "cover_image_url": "https://images.unsplash.com/photo-1513829596324-4bb2800c5efb?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "At Folsom Prison",
                    "artist": "Johnny Cash",
                    "release_year": 1968,
                    "cover_image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "I Put a Spell on You",
                    "artist": "Nina Simone",
                    "release_year": 1965,
                    "cover_image_url": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Master of Puppets",
                    "artist": "Metallica",
                    "release_year": 1986,
                    "cover_image_url": "https://images.unsplash.com/photo-1517230878791-4d28214057c2?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "AM",
                    "artist": "Arctic Monkeys",
                    "release_year": 2013,
                    "cover_image_url": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Arrival",
                    "artist": "ABBA",
                    "release_year": 1976,
                    "cover_image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "The Rise and Fall of Ziggy Stardust",
                    "artist": "David Bowie",
                    "release_year": 1972,
                    "cover_image_url": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Divenire",
                    "artist": "Ludovico Einaudi",
                    "release_year": 2006,
                    "cover_image_url": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=800&q=80"
                }
            ]

            albums = {}
            for item in albums_data:
                artist_obj = artists[item["artist"]]
                album = Album.objects.create(
                    title=item["title"],
                    artist=artist_obj,
                    release_year=item["release_year"],
                    cover_image_url=item["cover_image_url"]
                )
                albums[item["title"]] = album

            self.stdout.write(self.style.SUCCESS(f"Created {len(albums)} albums."))

            # ---------------------------------------------------------
            # 4. TRACKS (38 tracks with real titles, durations, valid MP3 URLs)
            # ---------------------------------------------------------
            tracks_data = [
                # Queen - A Night at the Opera
                {"title": "Bohemian Rhapsody", "album": "A Night at the Opera", "duration": 354, "times_played": 482, "mp3_id": 1},
                {"title": "Love of My Life", "album": "A Night at the Opera", "duration": 219, "times_played": 195, "mp3_id": 2},
                # Pink Floyd - The Dark Side of the Moon
                {"title": "Time", "album": "The Dark Side of the Moon", "duration": 425, "times_played": 320, "mp3_id": 3},
                {"title": "Money", "album": "The Dark Side of the Moon", "duration": 382, "times_played": 285, "mp3_id": 4},
                # Pink Floyd - Wish You Were Here
                {"title": "Wish You Were Here", "album": "Wish You Were Here", "duration": 334, "times_played": 412, "mp3_id": 5},
                {"title": "Shine On You Crazy Diamond", "album": "Wish You Were Here", "duration": 810, "times_played": 210, "mp3_id": 6},
                # The Beatles - Abbey Road
                {"title": "Come Together", "album": "Abbey Road", "duration": 259, "times_played": 390, "mp3_id": 7},
                {"title": "Here Comes the Sun", "album": "Abbey Road", "duration": 185, "times_played": 520, "mp3_id": 8},
                # Michael Jackson - Thriller
                {"title": "Billie Jean", "album": "Thriller", "duration": 294, "times_played": 630, "mp3_id": 9},
                {"title": "Beat It", "album": "Thriller", "duration": 258, "times_played": 440, "mp3_id": 10},
                # Daft Punk - Discovery
                {"title": "One More Time", "album": "Discovery", "duration": 320, "times_played": 510, "mp3_id": 11},
                {"title": "Harder, Better, Faster, Stronger", "album": "Discovery", "duration": 224, "times_played": 375, "mp3_id": 12},
                # Daft Punk - Random Access Memories
                {"title": "Get Lucky", "album": "Random Access Memories", "duration": 248, "times_played": 580, "mp3_id": 13},
                {"title": "Instant Crush", "album": "Random Access Memories", "duration": 337, "times_played": 290, "mp3_id": 14},
                # Kendrick Lamar - To Pimp a Butterfly
                {"title": "Alright", "album": "To Pimp a Butterfly", "duration": 219, "times_played": 360, "mp3_id": 15},
                {"title": "King Kunta", "album": "To Pimp a Butterfly", "duration": 234, "times_played": 315, "mp3_id": 16},
                # Kendrick Lamar - good kid, m.A.A.d city
                {"title": "Bitch, Don't Kill My Vibe", "album": "good kid, m.A.A.d city", "duration": 310, "times_played": 270, "mp3_id": 1},
                {"title": "Swimming Pools (Drank)", "album": "good kid, m.A.A.d city", "duration": 313, "times_played": 340, "mp3_id": 2},
                # Miles Davis - Kind of Blue
                {"title": "So What", "album": "Kind of Blue", "duration": 562, "times_played": 180, "mp3_id": 3},
                {"title": "Blue in Green", "album": "Kind of Blue", "duration": 337, "times_played": 145, "mp3_id": 4},
                # Adele - 21
                {"title": "Rolling in the Deep", "album": "21", "duration": 228, "times_played": 490, "mp3_id": 5},
                {"title": "Someone Like You", "album": "21", "duration": 285, "times_played": 470, "mp3_id": 6},
                # Bob Marley - Exodus
                {"title": "Jamming", "album": "Exodus", "duration": 211, "times_played": 230, "mp3_id": 7},
                {"title": "One Love / People Get Ready", "album": "Exodus", "duration": 173, "times_played": 380, "mp3_id": 8},
                # Hans Zimmer - Interstellar
                {"title": "Cornfield Chase", "album": "Interstellar (Original Motion Picture Soundtrack)", "duration": 127, "times_played": 410, "mp3_id": 9},
                {"title": "Stay", "album": "Interstellar (Original Motion Picture Soundtrack)", "duration": 412, "times_played": 260, "mp3_id": 10},
                # Radiohead - OK Computer
                {"title": "Paranoid Android", "album": "OK Computer", "duration": 383, "times_played": 295, "mp3_id": 11},
                {"title": "Karma Police", "album": "OK Computer", "duration": 261, "times_played": 365, "mp3_id": 12},
                # Taylor Swift - 1989
                {"title": "Blank Space", "album": "1989", "duration": 231, "times_played": 520, "mp3_id": 13},
                {"title": "Shake It Off", "album": "1989", "duration": 219, "times_played": 460, "mp3_id": 14},
                # Taylor Swift - Folklore
                {"title": "Cardigan", "album": "Folklore", "duration": 239, "times_played": 340, "mp3_id": 15},
                {"title": "Exile", "album": "Folklore", "duration": 285, "times_played": 310, "mp3_id": 16},
                # Led Zeppelin - Led Zeppelin IV
                {"title": "Stairway to Heaven", "album": "Led Zeppelin IV", "duration": 482, "times_played": 605, "mp3_id": 1},
                {"title": "Black Dog", "album": "Led Zeppelin IV", "duration": 296, "times_played": 275, "mp3_id": 2},
                # Stevie Wonder - Songs in the Key of Life
                {"title": "Sir Duke", "album": "Songs in the Key of Life", "duration": 232, "times_played": 330, "mp3_id": 3},
                {"title": "Isn't She Lovely", "album": "Songs in the Key of Life", "duration": 394, "times_played": 350, "mp3_id": 4},
                # Billie Eilish - When We All Fall Asleep
                {"title": "Bad Guy", "album": "When We All Fall Asleep, Where Do We Go?", "duration": 194, "times_played": 560, "mp3_id": 5},
                # Nirvana - Nevermind
                {"title": "Smells Like Teen Spirit", "album": "Nevermind", "duration": 301, "times_played": 620, "mp3_id": 6},
                {"title": "Come as You Are", "album": "Nevermind", "duration": 219, "times_played": 380, "mp3_id": 7},
                # B.B. King - Live at the Regal
                {"title": "Everyday I Have the Blues", "album": "Live at the Regal", "duration": 158, "times_played": 140, "mp3_id": 8},
                # Johnny Cash - At Folsom Prison
                {"title": "Folsom Prison Blues", "album": "At Folsom Prison", "duration": 165, "times_played": 310, "mp3_id": 9},
                # Nina Simone - I Put a Spell on You
                {"title": "Feeling Good", "album": "I Put a Spell on You", "duration": 174, "times_played": 490, "mp3_id": 10},
                # Metallica - Master of Puppets
                {"title": "Master of Puppets", "album": "Master of Puppets", "duration": 515, "times_played": 420, "mp3_id": 11},
                # Arctic Monkeys - AM
                {"title": "Do I Wanna Know?", "album": "AM", "duration": 272, "times_played": 570, "mp3_id": 12},
                {"title": "R U Mine?", "album": "AM", "duration": 201, "times_played": 390, "mp3_id": 13},
                # ABBA - Arrival
                {"title": "Dancing Queen", "album": "Arrival", "duration": 231, "times_played": 540, "mp3_id": 14},
                # David Bowie - Ziggy Stardust
                {"title": "Starman", "album": "The Rise and Fall of Ziggy Stardust", "duration": 253, "times_played": 380, "mp3_id": 15},
                # Ludovico Einaudi - Divenire
                {"title": "Nuvole Bianche", "album": "Divenire", "duration": 358, "times_played": 430, "mp3_id": 16}
            ]

            tracks = []
            for item in tracks_data:
                album_obj = albums[item["album"]]
                track_url = f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{item['mp3_id']}.mp3"
                track = Track.objects.create(
                    title=item["title"],
                    album=album_obj,
                    duration_in_seconds=item["duration"],
                    track_url=track_url,
                    times_played=item["times_played"]
                )
                tracks.append(track)

            self.stdout.write(self.style.SUCCESS(f"Created {len(tracks)} tracks."))

            # ---------------------------------------------------------
            # 5. PLAYLISTS (22 diverse, thematic playlists)
            # ---------------------------------------------------------
            playlists_data = [
                {
                    "title": "Classic Rock Legends",
                    "description": "Timeless rock and roll anthems from the golden age of guitar riffs, iconic vocals, and stadium power.",
                    "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Bohemian Rhapsody", "Time", "Stairway to Heaven", "Black Dog", "Come Together"]
                },
                {
                    "title": "90s Alternative & Grunge",
                    "description": "Distorted guitars, raw emotional vocals, and anthems that defined the generation of flannel and rebellion.",
                    "cover": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Smells Like Teen Spirit", "Come as You Are", "Paranoid Android", "Karma Police"]
                },
                {
                    "title": "Late Night Deep Focus",
                    "description": "Immersive, distraction-free soundscapes for coding, writing, studying, and deep contemplative thought.",
                    "cover": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Cornfield Chase", "Stay", "Nuvole Bianche", "Blue in Green", "So What"]
                },
                {
                    "title": "Electronic Dance Journey",
                    "description": "Pulsating French touch, vintage house grooves, and synth mastery built for the dancefloor.",
                    "cover": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["One More Time", "Harder, Better, Faster, Stronger", "Get Lucky", "Instant Crush"]
                },
                {
                    "title": "Hip-Hop Lyricism & Flow",
                    "description": "Top-tier storytelling, intricate rhyme schemes, and legendary beats from modern masters.",
                    "cover": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Alright", "King Kunta", "Bitch, Don't Kill My Vibe", "Swimming Pools (Drank)"]
                },
                {
                    "title": "Soul & Motown Treasures",
                    "description": "Rich brass horns, infectious joy, and heartfelt soul singing from the icons who set the standard.",
                    "cover": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Sir Duke", "Isn't She Lovely", "Feeling Good", "Billie Jean"]
                },
                {
                    "title": "Sunday Morning Acoustic",
                    "description": "Warm acoustic guitars, gentle voices, and serene melodies to ease into a tranquil morning.",
                    "cover": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Here Comes the Sun", "Wish You Were Here", "Love of My Life", "Cardigan"]
                },
                {
                    "title": "Pop Anthems & Chart Toppers",
                    "description": "Irresistible hooks, stadium sing-alongs, and chart-dominating global pop megahits.",
                    "cover": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Billie Jean", "Beat It", "Blank Space", "Shake It Off", "Bad Guy", "Dancing Queen"]
                },
                {
                    "title": "Cinema & Orchestral Magic",
                    "description": "Breathtaking orchestral arrangements that transport you straight into epic cinematic worlds.",
                    "cover": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Cornfield Chase", "Stay", "Nuvole Bianche"]
                },
                {
                    "title": "Legends of Blues & Roots",
                    "description": "Expressive bend solos, smoky upright bass, and authentic American roots music.",
                    "cover": "https://images.unsplash.com/photo-1513829596324-4bb2800c5efb?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Everyday I Have the Blues", "Folsom Prison Blues", "Feeling Good"]
                },
                {
                    "title": "Indie Rock Discovery",
                    "description": "Sharp hooks, nocturnal grooves, and captivating songwriting from the forefront of alternative indie.",
                    "cover": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Do I Wanna Know?", "R U Mine?", "Paranoid Android", "Starman"]
                },
                {
                    "title": "Heartbreak & Emotional Ballads",
                    "description": "Poignant lyrics, cathartic crescendos, and soulful vocals for reflective moments.",
                    "cover": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Someone Like You", "Rolling in the Deep", "Exile", "Love of My Life"]
                },
                {
                    "title": "Reggae & Island Sunshine",
                    "description": "Positive vibrations, one-drop drum rhythms, and uplifting messages of peace and harmony.",
                    "cover": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Jamming", "One Love / People Get Ready"]
                },
                {
                    "title": "Heavy Metal Riff Haven",
                    "description": "Blistering dual guitars, thunderous double-bass drumming, and iconic heavy metal anthems.",
                    "cover": "https://images.unsplash.com/photo-1517230878791-4d28214057c2?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Master of Puppets", "Black Dog", "Smells Like Teen Spirit"]
                },
                {
                    "title": "Coffeehouse Singer-Songwriters",
                    "description": "Intimate acoustic storytelling, fingerpicked guitars, and poetic lyrics perfect for your favorite cafe.",
                    "cover": "https://images.unsplash.com/photo-1526478806334-5fd488fcaabc?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Cardigan", "Exile", "Wish You Were Here", "Love of My Life"]
                },
                {
                    "title": "All-Time Greatest Hits",
                    "description": "The quintessential songs that shaped music history across six decades of greatness.",
                    "cover": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Bohemian Rhapsody", "Billie Jean", "Come Together", "Dancing Queen", "Starman"]
                },
                {
                    "title": "Jazz Club After Hours",
                    "description": "Dimmed lights, muted trumpets, and sophisticated modal improvisation for late evening relaxation.",
                    "cover": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["So What", "Blue in Green", "Feeling Good"]
                },
                {
                    "title": "Road Trip Sing-Alongs",
                    "description": "Windows rolled down, open highway ahead, and unforgettable tracks everyone knows all the words to.",
                    "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Shake It Off", "Dancing Queen", "One More Time", "Get Lucky", "Bohemian Rhapsody"]
                },
                {
                    "title": "Midnight Drive & Synthwave",
                    "description": "Neon reflections in the rain, analog synths, and driving basslines for nocturnal journeys.",
                    "cover": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Instant Crush", "Harder, Better, Faster, Stronger", "Bad Guy", "Starman"]
                },
                {
                    "title": "Peaceful Piano & Strings",
                    "description": "Gentle acoustic piano motifs and sweeping orchestral strings designed to soothe the spirit.",
                    "cover": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Nuvole Bianche", "Cornfield Chase", "Blue in Green"]
                },
                {
                    "title": "70s Vinyl Classics",
                    "description": "Warm analog master recordings, gatefold sleeves, and the pinnacle decade of album rock and disco.",
                    "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Money", "Sir Duke", "Dancing Queen", "Stairway to Heaven", "Starman"]
                },
                {
                    "title": "High Energy Workout Motivation",
                    "description": "Fast tempos, driving beats, and relentless intensity to push through your hardest training sessions.",
                    "cover": "https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=800&q=80",
                    "song_keywords": ["Master of Puppets", "Beat It", "Harder, Better, Faster, Stronger", "Do I Wanna Know?", "Bad Guy"]
                }
            ]

            track_by_title = {t.title: t for t in tracks}

            playlists = []
            for item in playlists_data:
                playlist = Playlist.objects.create(
                    title=item["title"],
                    description=item["description"],
                    cover_img_url=item["cover"]
                )
                selected_tracks = [track_by_title[k] for k in item["song_keywords"] if k in track_by_title]
                if len(selected_tracks) < 3:
                    extra_tracks = random.sample(tracks, 4)
                    selected_tracks.extend(extra_tracks)
                playlist.tracks.set(selected_tracks)
                playlists.append(playlist)

            self.stdout.write(self.style.SUCCESS(f"Created {len(playlists)} playlists."))

            # ---------------------------------------------------------
            # 6. USERS (20 real-like users)
            # ---------------------------------------------------------
            users_data = [
                ("alice_johnson", "alice.johnson@musicflow.com", "Alice", "Johnson"),
                ("bob_miller", "bob.miller@soundwave.org", "Bob", "Miller"),
                ("clara_oswald", "clara.oswald@melodybox.com", "Clara", "Oswald"),
                ("david_clark", "david.clark@audiovault.net", "David", "Clark"),
                ("elena_rostova", "elena.rostova@rhythmhive.com", "Elena", "Rostova"),
                ("fiona_gallagher", "fiona.g@sonicpulse.io", "Fiona", "Gallagher"),
                ("george_lucas", "george.l@tunespace.com", "George", "Lucas"),
                ("hannah_abbott", "hannah.a@harmonyhub.org", "Hannah", "Abbott"),
                ("ian_malcolm", "ian.malcolm@groovebyte.com", "Ian", "Malcolm"),
                ("julia_roberts", "julia.r@musicnest.com", "Julia", "Roberts"),
                ("kevin_bacon", "kevin.bacon@beatstream.io", "Kevin", "Bacon"),
                ("laura_croft", "laura.croft@soundatlas.net", "Laura", "Croft"),
                ("michael_scott", "michael.scott@dunderbeats.com", "Michael", "Scott"),
                ("nora_jones", "nora.jones@acousticvibe.org", "Nora", "Jones"),
                ("oliver_queen", "oliver.queen@starbeats.com", "Oliver", "Queen"),
                ("peter_parker", "peter.parker@dailybeats.nyc", "Peter", "Parker"),
                ("rachel_green", "rachel.green@centralperk.fm", "Rachel", "Green"),
                ("sam_winchester", "sam.w@hunteraudio.org", "Sam", "Winchester"),
                ("tina_turner", "tina.turner@rollinaudio.com", "Tina", "Turner"),
                ("victor_stone", "victor.stone@cybersound.io", "Victor", "Stone"),
            ]

            created_users = []
            for username, email, first_name, last_name in users_data:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password="MusicPlayerPassword2026!"
                )
                created_users.append(user)

            self.stdout.write(self.style.SUCCESS(f"Created {len(created_users)} users."))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with 20+ records in all tables!"))
