import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
trigger_sad = ["angry","miserable","sad","dissapointed","unhappy","depressed"]
trigger_lonely = ["so alone","all alone","lonely","need friend","someone to talk to","need comfort","need a freind","lonesome","heartbroken"]
trigger_curse = ["Fuck","fuck","shit","shitting","shitted","damn it","damnit","son of a bitch","dick","pussy","ass","bitch","asshole","cunt","bullshit","barbara streisand"]
magic8 = ["should","should I","Should I","what should I do?","should I do it?","if I should","Magic 8 ball","Magic 8ball","MAGIC 8BALL","magic 8 ball","magic 8ball","can you answer"]
gratitude = ["Thank you","thanks","Thanks","thx",'thnx',"thank u","thank"]
member_name = ['@lilchewie','@illo','@PlainBrain']

respond_sad = ["I am sorry you are feeling that way.","Things will get better in time","This too shall pass","You will make it through this, I believe in you","There's always a silver lining if you look for it","Sometimes when your down, you just need to change your perspective to look up"]
starter_encouragements = ["Cheer up!","Hang in there.",
  "You are a great person / bot!"]
respond_lonely = ["Hey, there! I will be your friend.","I've always liked you","I like spending time with you","You are a great friend to me","I enjoy our time together"]
respond_curse = ["Oh! My virgin bot ears!","wow,such language!","you kiss your mother with that mouth?","Im going to get you a bar of soap to wash your mouth out!","tsk tsk, such language","such obscenities!","I do not approve of such language","What is it with you humans and cursing","cursing has no place here","Oh my","Oh no you didnt!","wowsers, you must be mad","why you curse so much bro?"]
respond_magic8 = ["Don't count on it","No way!","Thats a terrible idea","Don't do it","Got any more terrible ideas?","yeah, thats a hard no my friend.","Absolutely NOT!","I can't emphasize this enough. NO.","Yes, and by yes, I really mean NO!","the answer is no.","You know what you should so, I dont need to tell you","Go with your gut","Cannot make prediction now","Try again later","Dude, I have no idea.","idk, *shrugs*","The number you're trying to call is currently busy. Please call back and try again later.","Concentrate real hard and ask again.","u do u boo, u do u.","Thats a great idea, do it!","Absolutely, YES!","Im going to say, YES!","No, and by no, I really mean YES!","I dont always say yes, but when I do, I say it emphatically","yesssir","YES!","Hold on... downloading all the wisdom from the universe....and, they said NO","Eh, maybe?","If you think its a bad idea, it probably is","If you think its a good idea, it probably is","You should weigh out your options","Im going to say YES","Im going to say NO.","nah, bro.","Take a step outside your situation and answer this question for yourself.","Go flip a coin, im busy.","The answer is yes","Abso-friggin-lutely","Indubitably"]
respond_gratitude = ['You are welcome :)',"Anything for you buddy","ur welcome","no worries","you are very welcome my friend","no problemo",'no problem','you got it dude','anything for you buddy','you are the most welcome','you are welcome','welcome']

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements


client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if any(word in message.content for word in trigger_curse):
    await message.channel.send(random.choice(respond_curse))

  if any(word in message.content for word in magic8):
    await message.channel.send(random.choice(respond_magic8))
  
  if any(word in message.content for word in trigger_lonely):
    await message.channel.send(random.choice(respond_lonely))

  if any(word in message.content for word in trigger_sad):
    await message.channel.send(random.choice(respond_sad))
  
  if any(word in message.content for word in gratitude):
      await message.channel.send(random.choice(respond_gratitude))

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith("$new"):
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

    if message.content.startswith("$list"):
      encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if message.content.startswith("$responding"):
    value = message.content.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")



keep_alive()
client.run(os.getenv('TOKEN'))