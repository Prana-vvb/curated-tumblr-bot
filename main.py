import discord
import os
import praw
import requests
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

reddit = praw.Reddit(
    client_id=os.getenv('RCLIENT_ID'),
    client_secret=os.getenv('RCLIENT_SECRET'),
    user_agent=os.getenv('RUSER_AGENT')
)

def get_post():
    try:
        subreddit = reddit.subreddit('CuratedTumblr')
        post = random.choice([post for post in subreddit.hot(limit=10)])
        title = post.title
        link = post.url
        subreddit = post.subreddit.display_name
        return f"**{title}**\nFrom r/{subreddit}: {link}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching post: {e}")
        return "Sorry, I can't fetch a post right now."

@client.event
async def on_ready():
    print(f"{client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$post"):
        post = get_post()
        await message.channel.send(post)

client.run(os.getenv("TOKEN"))
