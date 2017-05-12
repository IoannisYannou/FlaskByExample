import feedparser
from flask import Flask, render_template, request
import json
import urllib2
import urllib

api_key = {}
with open('api_keys.txt', 'r') as f:
	for line in f:
		service,key = line.strip().split()
		api_key[service] = key

print (api_key)

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			 'cnn': 'http://rss.cnn.com/rss/edition.rss',
			 'fox': 'http://feeds.foxnews.com/foxnews/latest',
			 'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc', 
			'city': 'London,UK',
			'currency_from': 'GBP',
			'currency_to': 'USD'}

@app.route('/')
def home():
	# get customized headlines, based on user input or default
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)

	# get customized weather based on user input or default
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)

	# return render_template("home.html", articles=articles, weather=weather)
	# get customized currency based on user input or default
	currency_from = request.args.get("currency_from")
	if not currency_from:
		currency_from = DEFAULTS["currency_from"]
	currency_to = request.args.get("currency_to")
	if not currency_to:
		currency_to = DEFAULTS['currency_to']
	rate, currencies = get_rates(currency_from, currency_to)

	return render_template("home.html", articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies))

def get_news(query):
	if not query or query.lower() not in RSS_FEEDS:
		publication = DEFAULTS['publication']
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return feed['entries']

def get_weather(query):
	api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
	query = urllib.quote(query)
	url = api_url.format(query, api_key['openweathermap'])
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = {"description":parsed["weather"][0]["description"], 
				   "temperature":parsed["main"]["temp"], 
				   "city":parsed["name"],
				   "country": parsed['sys']['country']}
	return weather

def get_rates(frm, to):
	api_url = "https://openexchangerates.org//api/latest.json?app_id={}"
	url = api_url.format(api_key["openexchangerates"])
	all_currency = urllib2.urlopen(url).read()
	parsed = json.loads(all_currency).get('rates')
	frm_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return (to_rate/frm_rate, parsed.keys())

# if '__name__' == '__main__':
app.run(port=5000, debug=True)