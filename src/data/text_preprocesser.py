import string
import pandas as pd
import re
import nltk
import demoji
from nltk.corpus import wordnet,stopwords
from nltk.stem import WordNetLemmatizer

demoji.download_codes()
nltk.download(['averaged_perceptron_tagger','stopwords','wordnet'])


stopwords = nltk.corpus.stopwords.words('english')
lemmatizer = WordNetLemmatizer()

# Pos tag, used Noun, Verb, Adjective and Adverb
wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}

dftweet = pd.read_csv("/content/df_tweet.csv")

# nlp data cleaning method
def text_preprocesser(text):

    # remove url
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text_no_url = url_pattern.sub(r'', text)

    # to lower
    text_lower = "".join([i.lower() for i in text_no_url])

    # remove @user and #(except doge)
    text_doge = []
    exception = ['#doge', '#dogecoin', '@dogecoin']
    for i in text_lower.split():
        if i in exception:
            text_doge.append(re.sub('[#@]','',i))
        else:
            text_doge.append(i)
    text_doge = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", str(text_doge)).split())
    # if without emoji desc
    # text_doge = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
    # ' " ", str(text_doge)).split())

    # remove special characters
    text_clean = "".join([i for i in text_doge if i not in string.punctuation])

    # remove stopword eg: I, the, and
    # text_cleaner = " ".join([i for i in str(text_clean).split() if i not in stopwords])

    # convert emojis to description
    text_cleanest = demoji.replace_with_desc(text_clean).replace(':',' ')

    # word lemmatizer (condense word to base form)
    pos_tagged_text = nltk.pos_tag(text_cleanest.split())
    text_cant_be_cleaner = " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])

    return text_cant_be_cleaner

dftweet['tweet_text'] = dftweet['tweet_text'].fillna("")

dftweet['cleaned_text'] = dftweet['tweet_text'].apply(text_preprocesser)
