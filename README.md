# Rocketchat-pollbot
Pollbot for rocketchat

# Requirements
- rocketchat-API==0.6.3

# Setup
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


# Usage
To create a poll write:
`@BOTNAME poll "Do you like cookies" yes no`
