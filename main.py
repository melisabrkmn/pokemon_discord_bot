import discord
import random
from discord.ext import commands
from config import TOKEN as token
from logic import Pokemon
from logic import Wizard
from logic import Fighter

# Bot için yetkileri/intents ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

# '!go' komutu
@bot.command()
async def go(ctx):
    # Kullanıcı adları aynı olabilir; Discord kullanıcı kimliği her kullanıcı için eşsizdir.
    # Komutu çağıran kullanıcının kimliğini alır
    author_id = ctx.author.id

    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    # Bu kullanıcı için zaten bir Pokémon olup olmadığını kontrol ederiz
    if author_id not in Pokemon.pokemons:
        chance = (
            random.randint(1, 3)  # 1 ile 3 arasında rastgele bir sayı oluştururuz
        )

        # Rastgele sayıya göre bir Pokémon nesnesi oluştururuz (Yeni Pokémon oluşturma)
        if chance == 1:
            pokemon = Pokemon(author_id) 
        elif chance == 2:
            pokemon = Wizard(author_id)  # Wizard türünde bir Pokémon oluştururuz
            await ctx.send("Wizard türünde bir Pokémon oluşturuldu.")
        elif chance == 3:
            pokemon = Fighter(author_id)  # Fighter türünde bir Pokémon oluştururuz
            await ctx.send("Fighter türünde bir Pokémon oluşturuldu.")

        await pokemon.load_data()  # API verileri çekiliyor

        # Gömülü bir mesaj (embed) oluştururuz ve Pokémon hakkında bilgi ekleriz
        embed = discord.Embed(
            title=f"Your new Pokémon: {pokemon.get_name()}",
            color=discord.Color.blurple(),
            description="Great choice! Here are the details of your Pokemon.",
        )

        # Eğer Pokémon nadir (Shiny) ise özel alan ekleriz
        if getattr(pokemon, "is_shiny", False):
            embed.add_field(
                name="LUCKY PULL!",
                value="**You have caught a shiny Pokémon!**",
                inline=False,
            )

        embed.add_field(name="Type", value=pokemon.get_types(), inline=True)
        embed.add_field(name="Height", value=pokemon.get_height(), inline=True)
        embed.add_field(name="Weight", value=pokemon.get_weight(), inline=True)
        embed.add_field(name="Attack", value=pokemon.attack, inline=True)
        embed.add_field(name="HP", value=pokemon.hp, inline=True)
        embed.add_field(name="Number", value=pokemon.get_number(), inline=True)

        # Pokémon görüntüsünün URL'sini alırız
        image_url = pokemon.get_sprite()
        if image_url:
            embed.set_image(url=image_url)  # Gömülü mesaja görüntüyü ekleriz
            await ctx.send(
                embed=embed
            )  # Görüntülü gömülü mesajı (Pokémon hakkında bilgi) göndeririz
        else:
            await ctx.send(
                "Pokémon görüntüsü yüklenemedi."
            )  # Görüntü yüklenemezse hata mesajı veririz

    else:
        # Kullanıcıya zaten bir Pokémon oluşturduğunu bildiririz
        # Kullanıcının zaten bir pokemon'u varsa mevcut olanı gösterme
        pokemon = Pokemon.pokemons[author_id]
        await pokemon.load_data()

        embed = discord.Embed(
            title=f"You already own a Pokémon: {pokemon.get_name()}",
            color=discord.Color.blurple(),
            description="Here are the details of your companion:",
        )
        embed.add_field(name="Type", value=pokemon.get_types(), inline=True)
        embed.add_field(name="Height", value=pokemon.get_height(), inline=True)
        embed.add_field(name="Weight", value=pokemon.get_weight(), inline=True)
        embed.add_field(name="Attack", value=pokemon.get_attack(), inline=True)
        embed.add_field(name="HP", value=pokemon.get_hp(), inline=True)
        embed.add_field(name="Number", value=pokemon.get_number(), inline=True)

        image_url = pokemon.get_sprite()
        if image_url:
            embed.set_image(url=image_url)

        # Bir Pokémon'un daha önce oluşturulup oluşturulmadığını gösteren bir mesaj göndeririz
        await ctx.send(
            content="You can't create another Pokémon!", embed=embed
        )

# '!info' komutu
@bot.command()
async def info(ctx):
    # Komutu kullanan kullanıcının kimliğini alırız
    author_id = ctx.author.id

    # Kullanıcının bir Pokémon'a sahip olup olmadığını kontrol ederiz
    if author_id in Pokemon.pokemons:
        # Kullanıcının Pokémon'unu pokemons sözlüğünden alırız
        pok = Pokemon.pokemons[author_id]
        await ctx.send(pok.info())
    else:
        await ctx.send("You don't have a Pokémon yet! Catch one by typing `!go`.")

@bot.command()
async def heal(ctx):
    author_id = ctx.author.id
    if author_id in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author_id]
        response = await pokemon.heal()
        await ctx.send(response)
    else:
        await ctx.send("You don't have a Pokémon yet! Catch one by typing `!go`.")

#feed
@bot.command()
async def feed(ctx):
    author_id = ctx.author.id
    
    if author_id in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author_id]
        leveled_up = await pokemon.feed()
        
        if leveled_up:
            embed = discord.Embed(
                title=f"CONGRATS! {pokemon.get_name()} leveled up!",
                description=f"New Level: **{pokemon.level}**\n **HP:** {pokemon.hp} (+5)\n **Attack:** {pokemon.attack} (+3)",
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url=pokemon.get_sprite())
            await ctx.send(embed=embed)
        else:
            bonus_text = "(Shiny Bonus: +20 EXP)" if pokemon.is_shiny else "(+10 EXP)"
            await ctx.send(f"**{pokemon.get_name()}** has been fed! {bonus_text}\nCurrent EXP: **{pokemon.exp}/30** | Level: **{pokemon.level}**")
    else:
        await ctx.send("You don't have a Pokémon yet! Catch one by typing `!go`.")

# '!attack' komutu
@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.id in Pokemon.pokemons and ctx.author.id in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.id]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.id]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack_enemy(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz
    
# Botun çalıştırılması
bot.run(token)
