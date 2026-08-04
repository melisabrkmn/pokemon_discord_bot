import random
from datetime import datetime, timedelta

import aiohttp

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
        self.last_heal_time = None  # Pokémonun beslenme zamanı
        
        self.level = 1
        self.exp = 0
        self.hp = None
        self.attack = None
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
                    self.hp = 50
                    self.attack = 10

    async def heal(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if self.last_heal_time is None or (current_time - self.last_heal_time) > delta_time:
            self.hp += hp_increase
            self.last_heal_time = current_time
            return f"Pokémon sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            next_heal_time = self.last_heal_time + delta_time
            return f"Pokémonunuzu şu zaman iyileştirebilirsiniz: {next_heal_time}"

    async def feed(self):
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
    
    async def attack_enemy(self, enemy):
        if enemy.hp > self.attack:
            enemy.hp -= self.attack
            return f"Pokémon trainer@{self.pokemon_trainer} has attacked @{enemy.pokemon_trainer}! \n@{enemy.pokemon_trainer}'s hp: {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon trainer@{self.pokemon_trainer} has defeated @{enemy.pokemon_trainer}!"

    # Pokémon hakkındaki bilgileri metin olarak döndürür
    def info(self):
        return (
            f"Pokémon: {self.get_name()}\n"
            f"Type: {self.get_types()}\n"
            f"Height: {self.get_height()}\n"
            f"Weight: {self.get_weight()}\n"
            f"Attack: {self.get_attack()}\n"
            f"HP: {self.get_hp()}\n"
            f"Level: {self.level}\n"
            f"EXP: {self.exp}/30\n"
            f"Number: {self.get_number()}"
        )

    def get_name(self): return self.name
    def get_sprite(self): return self.sprite
    def get_weight(self): return f"{self.weight} kg"
    def get_height(self): return f"{self.height} m"
    def get_types(self): return ", ".join(self.types)
    def get_attack(self): return self.attack 
    def get_hp(self): return self.hp
    def get_number(self): return self.pokemon_number

class Wizard(Pokemon):
    async def attack_enemy(self, enemy):
        if isinstance(enemy, Wizard):  # Düşmanın Wizard veri tipi olup olmadığının kontrol edilmesi (Sihirbaz sınıfının bir örneği midir?)
            sans = random.randint(1, 5)
            if sans == 1:
                return "Wizard Pokémon used a shield in battle!"
        return await super().attack_enemy(enemy)
    async def heal(self, feed_interval=10, hp_increase=10):
        return await super().heal(feed_interval, hp_increase)

class Fighter(Pokemon):
    async def attack_enemy(self, enemy):
        sans = random.randint(1, 5)
        if sans == 1:
            super_guc = random.randint(5, 15)
            self.attack += super_guc
            sonuc = await super().attack_enemy(enemy)  
            self.attack -= super_guc
            return sonuc + f"\nFighter Pokémon has used super attack. Added attack: {super_guc}"
        return await super().attack_enemy(enemy)
    async def heal(self, feed_interval=10, hp_increase=20):
        return await super().heal(feed_interval, hp_increase)
