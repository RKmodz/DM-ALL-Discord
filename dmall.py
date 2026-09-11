import discord
import logging
import asyncio
import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from colorama import Fore, Style, init

# Initialisation Colorama
init(autoreset=True)

class Color:
    RED = Fore.RED + Style.BRIGHT
    GREEN = Fore.CYAN
    YELLOW = Fore.YELLOW + Style.BRIGHT
    BLUE = Fore.BLUE + Style.BRIGHT
    MAGENTA = Fore.MAGENTA + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

# Réduction des logs Discord
logging.basicConfig(level=logging.CRITICAL)

# Intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = False  # Facultatif, à activer si besoin

class MessageInput:
    def __init__(self):
        self.message = None
        self.window = tk.Tk()
        self.window.title("Message DM All")
        self.window.geometry("500x400")
        self.window.configure(bg='#2C2F33')

        style = ttk.Style()
        style.configure("Custom.TButton", padding=10, background="#7289DA")

        self.text_label = tk.Label(
            self.window,
            text="✉️ Entrez votre message à envoyer :",
            fg='#7289DA',
            bg='#2C2F33',
            font=('Arial', 14, 'bold')
        )
        self.text_label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(
            self.window,
            width=50,
            height=15,
            font=('Arial', 11),
            bg='#36393F',
            fg='#FFFFFF'
        )
        self.text_area.pack(pady=10, padx=10)

        self.submit_button = ttk.Button(
            self.window,
            text="🚀 Lancer le DM All",
            style="Custom.TButton",
            command=self.submit
        )
        self.submit_button.pack(pady=20)

    def submit(self):
        self.message = self.text_area.get("1.0", tk.END).strip()
        self.window.quit()
        self.window.destroy()

    def get_message(self):
        self.window.mainloop()
        return self.message

class BotClient(discord.Client):
    def __init__(self, token, server_id, message, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.token = token
        self.server_id = server_id
        self.message = message
        self.sent_count = 0

    async def on_ready(self):
        print(f'{Color.GREEN}🌟 [{self.user.name}] est connecté avec succès !{Color.RESET}')
        
        guild = self.get_guild(self.server_id)
        if not guild:
            print(f"{Color.RED}❌ Serveur introuvable avec l'ID {self.server_id}.{Color.RESET}")
            await self.close()
            return

        await self.send_messages_to_members(guild)
        print(f"\n{Color.GREEN}✅ Total des messages envoyés : {Color.WHITE}{self.sent_count}{Color.RESET}")
        await self.close()

    async def send_messages_to_members(self, guild):
        print(f"\n{Color.YELLOW}💌 Envoi des messages...{Color.RESET}")
        print(f"{Color.BLUE}🎯 Serveur : {guild.name}{Color.RESET}")
        print(f"{Color.BLUE}👥 Membres : {len(guild.members)}{Color.RESET}\n")

        for member in guild.members:
            if member.bot or member.id == self.user.id:
                continue  # Ignore les bots et soi-même
            try:
                dm = await member.create_dm()
                await dm.send(self.message)
                self.sent_count += 1
                print(f"{Color.MAGENTA}✉️ Envoyé à {member.display_name}{Color.RESET}")
                await asyncio.sleep(1)  # Pause pour éviter le spam trop rapide
            except Exception as e:
                print(f"{Color.RED}❌ Impossible d’envoyer à {member.display_name} : {e}{Color.RESET}")

def main():
    print(f"\n{Color.BLUE}🔐 Configuration du Bot{Color.RESET}")
    print(f"{Color.YELLOW}{'='*50}{Color.RESET}\n")

    token = input(f"{Color.MAGENTA}🔑 Token du bot > {Color.RESET}").strip()
    try:
        server_id = int(input(f"{Color.MAGENTA}🎯 ID du serveur > {Color.RESET}").strip())
    except ValueError:
        print(f"{Color.RED}❌ ID invalide.{Color.RESET}")
        return

    message_input = MessageInput()
    message = message_input.get_message()

    if message:
        client = BotClient(token, server_id, message)
        try:
            client.run(token)
        except discord.LoginFailure:
            print(f"{Color.RED}❌ Token invalide.{Color.RESET}")
    else:
        print(f"{Color.RED}❌ Aucun message entré. Annulé.{Color.RESET}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    TITLE = '''
██████╗ ███╗   ███╗     █████╗ ██╗     ██╗     
██╔══██╗████╗ ████║    ██╔══██╗██║     ██║     
██║  ██║██╔████╔██║    ███████║██║     ██║     
██║  ██║██║╚██╔╝██║    ██╔══██║██║     ██║     
██████╔╝██║ ╚═╝ ██║    ██║  ██║███████╗███████╗
╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝

By RKmodz 🩵
'''
    print(f"{Color.RED}{TITLE}{Color.RESET}")
    main()
