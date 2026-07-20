import discord
from discord.ext import commands
from config import TOKEN as token
from logic import Pokemon

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
    author_id = ctx.author.id
    
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author_id not in Pokemon.pokemons:
        pokemon = Pokemon(author_id)  # Yeni Pokémon oluşturma
        await pokemon.load_data()     # API verileri çekiliyor
        
        embed = discord.Embed(
            title=f"Your new Pokémon: {pokemon.get_name()}",
            color=discord.Color.blurple(),
            description="Great choice! Here are the details of your Pokemon."
        )
        embed.add_field(name="Type", value=pokemon.get_types(), inline=True)
        embed.add_field(name="Height", value=pokemon.get_height(), inline=True)
        embed.add_field(name="Weight", value=pokemon.get_weight(), inline=True)
        embed.set_image(url=pokemon.get_sprite())
        
        await ctx.send(embed=embed)
        
    else:
        # kullanıcının zaten bir pokemon'u varsa mevcut olanı gösterme
        pokemon = Pokemon.pokemons[author_id]
        await pokemon.load_data()
        
        embed = discord.Embed(
            title=f"You already own a Pokémon: {pokemon.get_name()}",
            color=discord.Color.blurple(),
            description="Here are the details of your companion:"
        )
        embed.add_field(name="Type", value=pokemon.get_types(), inline=True)
        embed.add_field(name="Height", value=pokemon.get_height(), inline=True)
        embed.add_field(name="Weight", value=pokemon.get_weight(), inline=True)
        embed.set_image(url=pokemon.get_sprite())

        await ctx.send(content="You can't create another Pokémon!", embed=embed) # Bir Pokémon'un daha önce oluşturulup oluşturulmadığını gösteren bir mesaj

# Botun çalıştırılması
bot.run(token)