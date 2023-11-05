import discord
import asyncio
import pymysql
from discord.ext import commands
from datetime import datetime


db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'przypomnienia'


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')

  
    await send_messages()

async def send_messages():
    while True:
  
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)
        cursor = conn.cursor()

   
        cursor.execute("SELECT id, godzina, tekst FROM wpisy")
        rows = cursor.fetchall()

        current_time = datetime.now().strftime('%H:%M')
        for row in rows:
            id_wiersza, godzina, tekst = row

            if current_time == godzina:
                channel = bot.get_channel(1170709894924611596) #ID kanału discord na którym ma się pojawić wiadomość
                await channel.send(f"<@&1170711411383619698> {tekst}") #Treść wiadomości
                
         
                cursor.execute("DELETE FROM wpisy WHERE id = %s", (id_wiersza,))
                conn.commit()

        cursor.close()
        conn.close()

        await asyncio.sleep(60) 

bot.run("MTE2Njc5MDE2ODEwODM0MzM0Ng.GvCe-K.KcvwmYKAUy2zvjyVx6EtEr7lUrbE2wrg4PrHZE") #Token bota discord
