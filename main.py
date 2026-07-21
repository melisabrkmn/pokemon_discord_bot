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
        if pokemon.is_shiny:
            embed.add_field(name="LUCKY PULL!", value="**You have caught a shiny Pokémon!**", inline=False)

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


# '!besle' komutu
@bot.command()
async def besle(ctx):
    author_id = ctx.author.id
    
    if author_id in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author_id]
        leveled_up = pokemon.feed()
        
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

# Botun çalıştırılması
bot.run(token)