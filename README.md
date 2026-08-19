<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png" alt="Pikachu" width="180">
  <h1>⚡ Pokémon Discord Bot</h1>
  <p>Catch and train Pokémon in your Discord server, then battle other trainers!</p>

  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/discord.py-2.6.4-5865F2?logo=discord&logoColor=white" alt="discord.py 2.6.4">
  <img src="https://img.shields.io/badge/API-PokéAPI-EF5350" alt="PokéAPI">
</div>

## 🎮 About the project

This project is a fun Discord bot that allows users to catch a random Pokémon and interact with it. Pokémon data is retrieved from [PokéAPI](https://pokeapi.co/).

Each trainer can own only one Pokémon. A caught Pokémon can belong to the normal, **Wizard**, or **Fighter** class. Every Pokémon also has a `10%` chance of being shiny. ✨

## ✨ Features

- Catch a random Pokémon
- Chance to discover a shiny Pokémon
- Wizard and Fighter classes
- Feeding and EXP system
- Leveling with HP and attack increases
- Pokémon healing system
- Battles against other trainers' Pokémon
- Pokémon information display
- Pokémon images provided by PokéAPI

## 🤖 Commands

| Command | Description |
| --- | --- |
| `!go` | Catches a random Pokémon or displays your existing Pokémon. |
| `!info` | Displays your Pokémon's current information. |
| `!feed` | Gives your Pokémon EXP and allows it to level up. |
| `!heal` | Restores your Pokémon's HP after the cooldown expires. |
| `!attack @user` | Attacks the mentioned user's Pokémon. |

## 💬 Usage examples

### Catching a Pokémon

```text
Trainer: !go
Bot: Your new Pokémon: Pikachu
Type: Electric
Height: 0.4 m
Weight: 6.0 kg
```

### Viewing Pokémon information

```text
Trainer: !info
Bot: Pokémon: Pikachu
Type: Electric
Height: 0.4 m
Weight: 6.0 kg
Attack: 55
HP: 35
Level: 1
EXP: 0/30
Number: 25
```

### Pokémon battle

```text
Trainer: !attack @opponent
Bot: Pokémon trainer has attacked the enemy Pokémon!
```

## 🚀 Installation

### 1. Open the project directory

```bash
cd TUR-PythonLVL3-M1L4
```

### 2. Install the required packages

```bash
python3 -m pip install discord.py aiohttp
```

### 3. Set the Discord bot token

Store the token in the `DISCORD_TOKEN` environment variable instead of writing it directly in the source code:

```bash
export DISCORD_TOKEN="your-new-discord-bot-token"
```

> [!IMPORTANT]
> Never upload your Discord bot token to GitHub or share it with anyone.

### 4. Run the bot

```bash
python3 main.py
```

The **Message Content Intent** option must be enabled in your Discord application settings so the bot can read message commands.

## 🗂️ Project structure

```text
TUR-PythonLVL3-M1L4/
├── main.py      # Discord bot and command handlers
├── logic.py     # Pokémon classes and game mechanics
├── config.py    # Token loading from an environment variable
└── README.md    # Project documentation
```

## 📸 Screenshots

After running the bot in Discord, you can add screenshots of the `!go`, `!info`, and `!attack` commands to this section.

Example Markdown:

```markdown
![Catching a Pokémon](assets/catching-a-pokemon.png)
![Pokémon information](assets/pokemon-information.png)
```

## ℹ️ Things to know

- Pokémon data is kept in memory while the bot is running.
- Caught Pokémon are reset whenever the bot restarts.
- An internet connection is required to retrieve Pokémon information.
- This project was created for educational purposes.

## 🙌 Credits

- Pokémon data: [PokéAPI](https://pokeapi.co/)
- Discord library: [discord.py](https://discordpy.readthedocs.io/)

Good luck on your Pokémon adventure! ⚡
