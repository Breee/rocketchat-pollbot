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


# Usage
To create a poll write:
`@BOTNAME poll "Do you like cookies" yes no`
