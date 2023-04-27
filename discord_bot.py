import os
import re
import json
import joblib
import discord
import requests
import stopwords
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------------------------------------------------------------
# Setup

load_dotenv()

# Setting Client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Dictionary to store titles and texts of resulting scraped pages
scrap = {}
scrap['title']     = []
scrap['texts']     = []
scrap['sentiment'] = []

# Inverted index dicitonary
indice = {}

# List of urls, initialized with a random url
# urls = ["https://www.naughtydog.com/company"]

# Headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0'}

# Vectorizer to calculate TFIDF measure
vectorizer = TfidfVectorizer()

# Control variables
total_urls = 0
first_url = True

# classifier (Naive Bayes)
pipeline = joblib.load('modelo_APS.joblib')
 # -------------------------------------------------------------------

# -------------------------------------------------------------------
# Seach functions -
def buscar(palavras, indice):
    # Dictionary to organize search results according to highest TFIDF
    assert type(palavras)==list
    resultado = dict()
    for p in palavras:
        if p in indice.keys():
            for documento in indice[p].keys():
                if documento not in resultado.keys():
                    resultado[documento] = indice[p][documento]
                else:
                    resultado[documento] += indice[p][documento]
    return resultado

def n_maiores(res_busca, n):
    # Sorting result to most relevant to least relevant (in casy n>1)
    res = []
    for k in res_busca.keys():
        # Relevância e documento
        res.append([res_busca[k], k])
    res = sorted(res, reverse = True)[0:n]
    return res

def query(query_string, n, indice):
    palavras = re.findall('\w+', query_string)
    res = buscar(palavras, indice)
    res_n = n_maiores(res, n)
    return res_n
# -------------------------------------------------------------------

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=os.getenv('GUILD_NAME'))
    channel = discord.utils.get(guild.text_channels, name=os.getenv('CHANNEL_NAME'))

    # await channel.send('O bot está online!')

@client.event
async def on_message(message):
    global scrap
    global indice
    global headers
    global first_url
    global vectorizer
    global total_urls
    global pipeline

    if message.author == client.user:
        return

    if message.content.lower() == '!author':
        await message.channel.send('I was created by Matheus Freitas. whose email is matheusfs2@al.insper.edu.br')

    if message.content.lower() == '!source':
        await message.channel.send('Here is the repository with my source code: https://github.com/MatFreitas/NLP_Bot')

    if message.content.lower() == '!help':
        await message.channel.send("!author: returns bot's author's name and email.\n"\
                                   "!source: returns repository of bot.\n\n"\
                                   "!search <words> th=<filter_value>: searches in pages for words.\n"\
                                   "!wn_search <words> th=<filter_value>: searches in pages for words similar to the ones inputted.\n"\
                                   "<filter_value>: fomrmat has to be decimal with one decimal place. Example: '0.3', '-0.4'. Values\n"\
                                   "can range from -1 to 1. This is an optional parameter.\n\n"\
                                   "!run <country> native_name: returns country's native name.\n"\
                                   "!run <country> currency: returns country's currency.\n"\
                                   "!run <country> capital: returns country's capital.\n"\
                                   "!run <country> flag: returns country's flag description.\n"\
                                   "If country name is a compound name, you can write it partially.\n"\
                                   "Info obtained at: https://restcountries.com/")

    if message.content.lower()[:4] == '!run':
        args = message.content.lower().split()[1:]

        # Making first letter of country to be a capital letter
        args[0] = args[0][0].upper() + args[0][1:]
    
        # Validating with regex if arguments are valid
        for arg in args:
            if re.fullmatch("\w[^\d]+", arg) is None:
                await message.channel.send(f"'{arg}' does not seem to be a valid argument.")

        
        response = requests.get(f"https://restcountries.com/v3.1/name/{args[0]}").json()[0]

        if args[1] == "native_name":
            info = list(response["name"]["nativeName"].values())[0]["common"]
            await message.channel.send(f"{args[0]}'s native name is {info}.")

        elif args[1] == "currency":
            currency = list(response["currencies"].values())[0]["name"]
            symbol = list(response["currencies"].values())[0]["symbol"]
            await message.channel.send(f"{args[0]}'s currency is {currency}, which is represented with '{symbol}'.")
        
        elif args[1] == "capital":
            info = list(response["capital"])[0]
            await message.channel.send(f"{args[0]}'s capital is {info}.")  

        elif args[1] == "flag":
            try:
                info = response["flags"]["alt"]
                await message.channel.send(info)     
            except:
                await message.channel.send(f"There does not seem to have a description to {args[0]}'s flag yet!")     

        else:
            await message.channel.send(f"'{args[1]}' is not a valid option! Try using '!help' to understand how to use '!run'.")     

    if message.content.lower()[:6] == '!crawl':
        # Update control total urls variable
        total_urls += 1

        # Getting url from arg
        url = message.content.lower().split()[1]

        # Returns a requests.models.Response object
        try:
            res = requests.get(url, headers=headers)
            html_page = res.content
        except:
            await message.channel.send(f"'{url}' does not seem to be a valid URL!")     
            return

        # Getting title and text of page
        soup = BeautifulSoup(html_page, 'html.parser')
        text_list = soup.find_all('p')
        title_list = soup.find('title')

        # Adding title and text of HTML to scraped pages dictionary
        scrap['title'].append(title_list.text)
        scrap['texts'].append(" ".join([text_list[i].text for i in range(len(text_list))]).replace("\n", " "))

        # Classifying page's general sentiment
        scrap['sentiment'].append([scrap['title'][-1], pipeline.predict_log_proba([scrap['texts'][-1]]).max()])

        # Updating TFIDF vectorizer
        tfidf = vectorizer.fit_transform(scrap['texts'])

        # Updating inverted index dictionary
        new_doc_idx = total_urls - 1
        new_doc_name = scrap['title'][-1]
        for word, idx in vectorizer.vocabulary_.items():
            if word in scrap['texts'][-1].split():
                # If word wasn't in any previous document, create its instance
                if word not in indice.keys():
                    indice[word] = {}

                # Update tfidf of word in new document
                indice[word][new_doc_name] = tfidf[new_doc_idx, idx]

    if message.content.lower()[:7] == '!search':
        # Checking if there is sentiment filter in search (positive)
        if message.content.lower()[-6:-3] == 'th=':
            sentiment_filter = float(message.content.lower()[-3:])
            res = query(message.content.lower()[8:-7], 3, indice)
        # Checking if there is sentiment filter in search (negative)
        elif message.content.lower()[-7:-4] == 'th=':
            sentiment_filter = float(message.content.lower()[-4:])
            res = query(message.content.lower()[8:-8], 3, indice)
        else:
            sentiment_filter = False
            res = query(message.content.lower()[8:], 3, indice)

        # Cheking if there were results to the query search
        if res != []:
            # If there was no filter
            if sentiment_filter == False:
                await message.channel.send("Search result:\n"\
                                                f"{res[0][1]}")
            else:
                for docs in res:
                    title_doc = docs[1]
                    sentiment_doc = None
                    for sentiment in scrap['sentiment']:
                        if sentiment[0] == title_doc:
                            sentiment_doc = sentiment[1]
                    if sentiment_doc is not None:
                        if sentiment_doc > sentiment_filter:    
                            await message.channel.send("Filtered Search result:\n"\
                                                    f"{title_doc}")
                            # If page is adequate, no need to go on
                            break
                        else:
                            await message.channel.send("Page found is too negative! Searching another option...\n")

        else:
            await message.channel.send("No results found!")

    if message.content.lower()[:10] == '!wn_search':
        # Checking if there is sentiment filter in search (positive)
        if message.content.lower()[-6:-3] == 'th=':
            sentiment_filter = float(message.content.lower()[-3:])
            terms = re.findall('\w+', message.content.lower()[10:-7])
        # Checking if there is sentiment filter in search (negative)
        elif message.content.lower()[-7:-4] == 'th=':
            sentiment_filter = float(message.content.lower()[-4:])
            terms = re.findall('\w+', message.content.lower()[10:-8])
        else:
            sentiment_filter = False
            terms = re.findall('\w+', message.content.lower()[10:])

        # Creating dic to store most similar terms to the ones searched
        relevancy = {}

        # To every term in vocabylary, find the relevancy 
        # it has to searched words
        for voc in vectorizer.vocabulary_:
            valor_soma = 0
            for word in terms:
                # Check if vocabulary term is not a stop word
                if voc.lower() not in stopwords.stop_words:
                    syns1 = wordnet.synsets(word)
                    syns2 = wordnet.synsets(voc)
                    # Check if there exists word in wordnet vocabulary
                    if len(syns1) > 0 and len(syns2) > 0:
                        # Score of similarity between words
                        similarity = syns1[0].wup_similarity(syns2[0])
                        if similarity is not None:
                            valor_soma += similarity
            relevancy[voc] = valor_soma

        # Sort dic and get the 5 most similar words
        similar_terms = [i[0] for i in sorted(relevancy.items(), key=lambda x:x[1], reverse=True)[:5]]

        # Formatting query string
        query_string = ' '.join(similar_terms)

        # Searching term in database
        res = query(query_string, 3, indice)

        # Cheking if there were results to the query search
        if res != []:
            # If there was no filter
            if sentiment_filter == False:
                await message.channel.send("Wordnet Search result:\n"\
                                                f"{res[0][1]}")
            else:
                for docs in res:
                    title_doc = docs[1]
                    sentiment_doc = None
                    for sentiment in scrap['sentiment']:
                        if sentiment[0] == title_doc:
                            sentiment_doc = sentiment[1]
                    if sentiment_doc is not None:
                        if sentiment_doc > sentiment_filter:    
                            await message.channel.send("Wordnet filtered Search result:\n"\
                                                    f"{title_doc}")
                            # If page is adequate, no need to go on
                            break
                        else:
                            await message.channel.send("Page found is too negative! Searching another option...\n")

client.run(os.getenv('TOKEN'))