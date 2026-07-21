import aiohttp  # Eşzamansız HTTP istekleri için kütüphane
import random

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)

        #sınıf nitelikleri
        self.name = None
        self.sprite = None
        self.weight = None
        self.height = None
        self.types = []
        
        self.level = 1
        self.exp = 0
        self.hp = 0
        self.attack = 0
        self.is_shiny = random.random() < 0.10 

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self

    async def load_data(self):
        if self.name is not None:  #veriler zaten yüklendiyse tekrar istek atma 
            return
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  # HTTP oturumu açma
            async with session.get(url) as response:     # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()

                    # API'dan gelen verileri niteliklerle eşleştirme
                    self.name = data['name'].capitalize()
                    # Shiny (nadir) pokemonlar için
                    if self.is_shiny:
                        self.name = f"Shiny {self.name}"
                        self.sprite = data['sprites']['front_shiny'] or data['sprites']['front_default']
                    else:
                        self.sprite = data['sprites']['front_default'] or "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUybWlxaXMzcWptem90bXBldXd1dG9kd3FidHMyZnFiNzVvazQzZW54aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hJ7qjPQk4V5w0aGihs/source.gif"

                    # m ve kg cinsinden boyut ve ağırlık
                    self.weight = data['weight'] / 10
                    self.height = data['height'] / 10
                    # pokemon'un sahip olduğu türleri listeleme
                    self.types = [t['type']['name'].capitalize() for t in data['types']]

                    for stat in data['stats']:
                        if stat['stat']['name'] == 'hp':
                            self.hp = stat['base_stat']
                        elif stat['stat']['name'] == 'attack':
                            self.attack = stat['base_stat']
                else:
                    # İstek başarısız olursa varsayılan adı döndürür
                    self.name = "IT'S PICACHU!!!!"
                    self.sprite = "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUybWlxaXMzcWptem90bXBldXd1dG9kd3FidHMyZnFiNzVvazQzZW54aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hJ7qjPQk4V5w0aGihs/source.gif"
                    self.weight = 0
                    self.height = 0
                    self.types = ["Unknown"]

    def feed(self):
        # Shiny ise 20 EXP, normal ise 10 EXP kazanma
        exp_gained = 20 if self.is_shiny else 10
        self.exp += exp_gained
        
        # her 30 EXP'de bir seviye atlar
        if self.exp >= 30:
            self.level += 1
            self.exp -= 30
            self.hp += 5      # HP artar
            self.attack += 3  # saldırı artar
            return True   # seviye atladı
        return False      # sadece beslendi (seviye atlamadı)

    def get_name(self): return self.name
    def get_sprite(self): return self.sprite
    def get_weight(self): return f"{self.weight} kg"
    def get_height(self): return f"{self.height} m"
    def get_types(self): return ", ".join(self.types)