import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
text = "I can't breathe, I'm so weak, I know this isn't easy. Don't tell me that your love is gone."
score = sia.polarity_scores(text)

if score['compound'] > 0:
    print(f", Positive, {score['compound']}")
elif score['compound'] < 0:
    print(f", Negative, {score['compound']}")
else:
    print(f", Neutral, {score['compound']}")
