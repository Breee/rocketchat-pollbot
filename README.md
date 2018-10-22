# Rocketchat-pollbot
This repository contains a Pollbot for rocketchat.

# Requirements
- rocketchat-API

# Pollbot Setup
1. Create a bot user on your rocketchat server.
2. Copy `example.config.py` to `config.py` and set the values as shown:
```
BOTNAME = "testman"
PASSWORD = "strong_pw"
SERVER = "https://test.testserver.com" 
```
Where `BOTNAME` is the name of your botuser, 
`PASSWORD` it's password to login onto the server
and `SERVER` your rocketchat server.

3. Add the emojis in the directory `custom_emojis` to your rocketchat server as custom emojis.
`Administration -> Custom Emojis`. They shall have the same name as the filenames, i.e.
- plus_one  for  plus_one.png
- plus_two  for  plus_two.png
- plus_three  for  plus_three.png
- plus_four  for  plus_four.png

4. start the bot with `python3 start_bot.py`

# Usage
To create a poll write:
`@BOTNAME poll "Do you like cookies" yes no`


# Mensabot (cafeteria bot)
The Mensabot is a Pollbot,  with an additional feature to post food of a cafeteria
Currently tailored forspecific cafeterias in Freiburg.
## Mensabot setup.
Same procedure as with the pollbot, just the config is different: 
```
BOTNAME = "testman"
PASSWORD = "strong_pw"
SERVER = "https://test.testserver.com"
MENSA_CACHE_URL = 'https://info.l-b-f.de/cache/mensa' 
MENSA_NAMES = ['Flugplatz', 'Rempartstrasse', 'Institusviertel']
DEFAULT_MENSA = 'Flugplatz'
```
Where `MENSA_CACHE_URL` is an url, which shall return a JSON object of the form: 
```
{  
   "Flugplatz":{  
      "Montag 22.10.":[  
         {  
            "veggy":1,
            "bezeichnung":"Essen 1",
            "gericht":"Kartoffelrösti<br>Kräuterquark<br>Kichererbsendip<br>Blattsalat"
         },
         {  
            "veggy":0,
            "bezeichnung":"Essen 2",
            "gericht":"Freiburger Münsterwurst<br>Pommes frites<br>Curryketchup<br>Blattsalat"
         }
      ],
      "Dienstag 23.10.":[  
         {  
            "veggy":1,
            "bezeichnung":"Essen 1",
            "gericht":"Tortellini gefüllt mit Ricotta und Spinat<br>Gorgonzolasauce<br>mit Spinatstreifen und Cashewkernen,Blattsalat<br>Dessert"
         },
         {  
            "veggy":0,
            "bezeichnung":"Essen 2",
            "gericht":"Lammragout mit Gemüse<br>Risoleekartoffeln<br>Blattsalat"
         }
      ],
      "Mittwoch 24.10.":[  
         {  
            "veggy":1,
            "bezeichnung":"Essen 1",
            "gericht":"Cannelloni mit Gemüse und Käsekruste<br>Tomatensauce<br>Petersilienpesto , Blattsalat"
         },
         {  
            "veggy":0,
            "bezeichnung":"Essen 2",
            "gericht":"Geflügel Saté-Spieß<br>Röstzwiebeln<br>Erdnusssauce<br>Basmatireis, Beilagensalat"
         }
      ],
      "Donnerstag 25.10.":[  
         {  
            "veggy":1,
            "bezeichnung":"Essen 1",
            "gericht":"Vegie Tag<br>Kürbislasagne<br>Pastinakensauce<br>Beilagensalat"
         },
         {  
            "veggy":1,
            "bezeichnung":"Essen 2",
            "gericht":"Vegie Tag<br>Quinoa Burger<br>Dreierlei Pommes frites<br>Blattsalat"
         }
      ],
      "Freitag 26.10.":[  
         {  
            "veggy":1,
            "bezeichnung":"Essen 1",
            "gericht":"Indisches Masala mit Auberginen und Karotten<br>Joghurtdip<br>Basmatireis<br>Mixsalat"
         },
         {  
            "veggy":0,
            "bezeichnung":"Essen 2",
            "gericht":"Paniertes Seelachsfilet MSC<br>Sauce Tartar<br>Kräuterkartoffeln<br>Blattsalat"
         }
      ]
}
```




