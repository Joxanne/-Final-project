# -*- coding: utf-8 -*-
import discord
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"登入身分為 --> {client.user}")

data = [
    ("Despacito Remix", "https://youtu.be/kJQP7kiw5Fk?si=Z-jj-x-aiRqIuHl-", 0.5994),
    ("Shape of You", "https://youtu.be/JGwWNGJdvx8?si=UtIE9-gzMSUVHX9b", 0.6808),
    ("See You Again", "https://youtu.be/RgKAFK5djSk?si=En7IUe8nVoTXx7cq", 0.0),
    ("Uptown Funk", "https://youtu.be/OPf0YbXqDm0?si=0J1PSWJwNiye-Nek", 0.6476),
    ("Sugar", "https://youtu.be/09R8_2nJtjg?si=Kjp66SPs8P8PchtS", 0.9602),
    ("Roar", "https://youtu.be/CevxZvSJLk8?si=UDHmYecDEqJtUXPO", 0.8555),
    ("Counting Stars", "https://youtu.be/hT_nvWreIhg?si=rzJAIY9nVn1lZjoj", -0.5574),
    ("Sorry", "https://youtu.be/BerNfXSuvJ0?si=XuVmRw62KZ6WMe_E", -0.466),
    ("Thinking out Loud", "https://youtu.be/lp-EO5I60KA?si=vYoXFEdTnz71NsGu", 0.9712),
    ("We Don't Talk Anymore", "https://youtu.be/3AtDnEC4zak?si=IYw-hRSMx2myauAb", -0.7641),
    ("Photograph", "https://youtu.be/nSDgHBxUbVQ?si=l1gAb7PvnbUY7W4J", 0.1877),
    ("Love is Gone", "https://youtu.be/hCrtcVDgCGw?si=-Gz71iuDu-fvwFFE", -0.2376)
]

def read(target_score):
    # 初始化最小差異值為正無窮大
    min_difference = float('inf')
    # 初始化最小差異的歌曲和URL為空
    min_difference_song = None
    best_fit_url = None
    
    # 遍歷歌曲資料
    for song, url, score in data:
        # 將歌曲的情感分數轉換為浮點數
        score = float(score)
        
        # 計算目標分數與歌曲分數的差異
        difference = abs(target_score - score)
        
        # 如果差異小於目前最小差異，更新最小差異值和相應的歌曲資訊
        if difference < min_difference:
            min_difference = difference
            min_difference_song = song
            best_fit_url = url

    # 返回最接近的歌曲、差異值和URL
    return min_difference_song, min_difference, best_fit_url


@client.event
# 當頻道有新訊息
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    # 新訊息包含Hello，回覆Hello, world!
    if message.content == "Hello":
        await message.channel.send("Hello, I am J bot ! Please share your current emotion, and I will recommend a song for you.")
        return

    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(message.content)
    song, difference, url = read(score['compound'])
    degree = "{:.2f}".format((1-difference)*100)

    if score['compound'] > 0:
        await message.channel.send("Detect the emotion is Positive.")
        await message.channel.send(f'The song "{song}" is for you! Matching degree is {degree}%')
        await message.channel.send(url)

    elif score['compound'] < 0:
        await message.channel.send("Detect the emotion is Negative.")
        await message.channel.send(f'The song "{song}" is for you! Matching degree is {degree}%')
        await message.channel.send(url)

    else:
        await message.channel.send("Detect the emotion is Neutral.")
        await message.channel.send(f'The song "{song}" is for you! Matching degree is {degree}%')
        await message.channel.send(url)

    print(f"The getting score is",score['compound'])

client.run("MTE1MzkyNTc5MjgyMTE1Mzg2Mg.GQmixW.Ludzh-xTa5gWYnNkeRT__z8zy49CJK__FbZBD0")
