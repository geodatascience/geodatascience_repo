from wordcloud import WordCloud
from twython import Twython
from PIL import Image
import numpy as np
import json
import re
import os

def collectAndSaveTweets(
	searchtoken,
	credentialfilepath,
	tweetfilepath,
	maxattempts=10,
	nboftweetstobefetch=500,
	language='fr'
):
	# credential parameters
	with open(credentialfilepath, mode='r') as f:
		d = json.load(f)

	# session object
	api = Twython(d['CONSUMER_KEY'], d['CONSUMER_SECRET'],
               d['ACCESS_TOKEN'], d['ACCESS_SECRET'])

	# Check if the connexion is successful
	api.verify_credentials()

	# file that holds the tweets
	tweetfile = open(tweetfilepath, 'w')

	# tweet count
	tweets = 0

	# apply a search wuery using the API
	for i in range(0, maxattempts):

		if(nboftweetstobefetch < tweets):
			break

		# Query Twitter:
		if(0 == i):
			results = api.search(
				q=searchtoken,
				count=1000,
				lang=language,
				tweet_mode='extended'
			)
		else:
			# After the first call we should have
			# max_id from result of previous call.
			# Pass it in query. Use the extended mode to get
			# all the content of the tweet and not a truncated version.
			results = api.search(
				q=searchtoken,
				include_entities='true',
				max_id=next_max_id,
				tweet_mode='extended'
			)

		# Save the returned tweets :
		# Tweets content are truncated
		# (even in the extended mode) when retweeted.
		# If it is the case, the full text of the
		# original tweet is in the retweeted_status
		# field of the JSON response.
		for result in results['statuses']:
			if 'retweeted_status' in result:
				tweetfile.write(result['retweeted_status']['full_text'])
			else:
				tweetfile.write(result['full_text'])
			tweets += 1

		# Get the next max_id to iterate over the results:
		try:
			next_results_url_params = results['search_metadata']['next_results']
			next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]
		except:
			break

	# close the file thats holds the tweets
	tweetfile.close()

class FilterObj(object):
    def __init__(self, *tabuwords):
        self.__tabuwords = tabuwords

    def __call__(self, text):
        def isnotin(tabu): return text.lower().find(tabu) == -1
        return (re.match("^#", text) is not None) and all(map(isnotin, self.__tabuwords))

def getFrequencyDictForText(fulltext, filterobj):
    result = {}
    for textblock in re.split('[\s\n,\.\)\(\"]+', fulltext):
        if filterobj(textblock):
            val = result.get(textblock.lower()[1:], 0)
            result[textblock.lower()[1:]] = val + 1
    return result

def makeImage(text, maskimagepath, outputpath):
    mask = np.array(Image.open(maskimagepath, mode='r'))
    wc = WordCloud(
        background_color="white",
        mask=mask,
        contour_width=3,
        contour_color='black'
    )
    # generate word cloud
    wc.generate_from_frequencies(text)
    wc.to_file(outputpath)

if __name__ == '__main__':
	# keywords to search for
	SEARCHTOKEN = input('enter the search token:')

	# global parameters
	PATHTOTHEJSONFILE = "./credentials.json"
	TWEETSFILEPATH = "./tweets.txt"
	MASKIMAGEPATH = "./temporary/test.png"
	OUTPUTPATH = "output.png"
	LANG = "fr"

	# collect and save the tweets
	collectAndSaveTweets(
		SEARCHTOKEN,
		PATHTOTHEJSONFILE,
		TWEETSFILEPATH,
		language=LANG
	)

	# build a frequency map from the content
	tweetfile = open(TWEETSFILEPATH, mode='r')
	fulltext = tweetfile.read()
	filterobj = FilterObj(*re.split('\s', SEARCHTOKEN))

	# generate image and save into image
	makeImage(
		getFrequencyDictForText(fulltext, filterobj),
		maskimagepath=MASKIMAGEPATH,
		outputpath=OUTPUTPATH
	)
