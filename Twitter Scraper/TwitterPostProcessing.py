#!/usr/bin/env python

# Author: Neal Soni & Dylan Gleicher
# Used to process the twitter information stored in the folder with the passed in twitter handled. Ex.
# Run this using python3 TwitterPostProcessing <TwitterHandle>

import sys
import csv
import os
import ast
import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math
from math import ceil, log10
from matplotlib import rcParams
from colorconverter import hsv2rgb, rgb2hsv
from graphs import *

rcParams.update({'figure.autolayout': True})

# Screen name (name of organization)
screen_name =  sys.argv[1]

absolute_path_to_screen_name = ""
absolute_path_to_images = ""
absolute_path_to_saveFiles = ""
absolute_path_to_figures = ""

# Returns an array with all the tweets of a twitter user. Scans the csv of all
# tweets that was created in the API Scraper. There are alot of API limitations so we can't get everything
def get_all_tweets(screen_name):
	allTweets = []
	# Open the csv for reading
	with open(absolute_path_to_saveFiles +screen_name+"_tweets.csv", "r") as f:
		reader = csv.reader(f)
		# reads csv into a list of lists
		data = list(list(rec) for rec in csv.reader(f, delimiter=','))
		for i in range(1, len(data)):
			dict1 = {}
			curr = data[i]
			for j in range(0, len(data[0])):
				dict1[data[0][j]] = curr[j]
			allTweets.append(dict1)
	# return the array of all tweets
	return allTweets


# Returns the information of a twitter user in a dictionary,
# Scans the info csv file created in the API Scraper
def getUserInformation(screen_name):
	userinfo = {}
	# Opens the csv for reading
	with open(absolute_path_to_saveFiles +screen_name+"_info.csv", "r") as f:
		reader = csv.reader(f)
		# reads csv into a list of lists
		data = list(list(rec) for rec in csv.reader(f, delimiter=','))
		curr = data[1]
		for j in range(0, len(data[0])):
			userinfo[data[0][j]] = curr[j]
	# return the dictionary of info
	return userinfo


# Using Vader, this function returns an array with positive, neutral,
# and negative sentiment analysis percentages for each tweet we have
def getVaderAnalysis(screen_name):
	# Get all tweets possible with current API limitations
	allTweets = get_all_tweets(screen_name)

	count = 0
	negativeTweets = 0
	neutralTweets = 0
	positiveTweets = 0

	for tweet in allTweets:
		# Calling vader API to analyze the sentiment
		sentiment = ast.literal_eval(str(tweet["score"]))["compound"]

		if sentiment <= -0.05:
			negativeTweets += 1
		elif sentiment < 0.05:
			neutralTweets += 1
		else:
			positiveTweets += 1

		count += 1

	# Return the array
	vader = [(round((positiveTweets/count)*100,3)), (
		round((neutralTweets/count)*100,3)), (
		round((negativeTweets/count)*100,3))]
	return vader


def step (rgb, repetitions=1):
	r = rgb[0]
	g = rgb[1]
	b = rgb[2]

	lum = math.sqrt( .241 * r + .691 * g + .068 * b )

	h, s, v = rgb2hsv(r,g,b)

	h2 = int(h * repetitions)
	lum2 = int(lum * repetitions)
	v2 = int(v * repetitions)

	if h2 % 2 == 1:
		v2 = repetitions - v2
		lum = repetitions - lum

	return (h2, lum, v2)

def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0

	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg

	return out

def processTwitterInfo(allTweets, userinfo):
	outputJSON = {}

	count = 0
	likes = []
	likesWithImages  = []
	likesForRetweet  = []
	likesForOriginal = []


	retweets = []
	tweetRespondedTo = []
	colors = []
	tweetRespondedToUsers = {}
	responseCount = 0
	tweetsWithImages = 0

	tweetsWithNoLikes = 0

	negativeTweets = 0
	neutralTweets = 0
	positiveTweets = 0

	for tweet in allTweets:
		# print(count, tweet)
		likes.append(int(tweet["likes"]))
		retweets.append(int(tweet["retweets"]))
		# print(tweet["originalTweetData"])

		#get who the user responds to:
		originalTweet =  ast.literal_eval(str(tweet["originalTweetData"]))
		tweetRespondedTo.append(originalTweet)
		try:
			original_screen_name = originalTweet["user"]["screen_name"]
			if original_screen_name in tweetRespondedToUsers.keys():
				tweetRespondedToUsers[original_screen_name][0] += 1
				tweetRespondedToUsers[original_screen_name][1].append(originalTweet)
			else:
				tweetRespondedToUsers[original_screen_name] = [1, [originalTweet]]

			if originalTweet["images"] != '[]':

				tweetsWithImages += 1
				imagesColors = originalTweet["colors"]
				likesWithImages.append(int(tweet["likes"]))
				for image in imagesColors:
					for color in image:
						colors.append(np.array((int(color['r']), int(color['g']), int(color['b']))))
		except:
			pass

		if tweet["responseTo"] != '':
			likesForRetweet.append(int(tweet["likes"]))
			responseCount += 1
		else:
			likesForOriginal.append(int(tweet["likes"]))
		if tweet["images"] != '[]':
			tweetsWithImages += 1
			likesWithImages.append(int(tweet["likes"]))
			imagesColors = ast.literal_eval(str(tweet["colors"]))
			for image in imagesColors:
				for color in image:
					colors.append(np.array((int(color['r']), int(color['g']), int(color['b']))))
		sentiment = ast.literal_eval(str(tweet["score"]))["compound"]
		if sentiment <= -0.05:
			negativeTweets += 1
		elif sentiment < 0.05:
			neutralTweets += 1
		else:
			positiveTweets += 1

		if int(tweet["likes"]) == 0:
			tweetsWithNoLikes += 1
		count += 1

	print("count of colors: ", len(colors))
	outputJSON["colorCount"] = len(colors)

	# imageName = createImagePallete(colors)
	# outputJSON["colorImage"] = imageName


	print("there are " + str(count) + " tweets")
	outputJSON["tweetCount"] = str(count)


	print("(% Positive, % Neutral, % Negative): (", round(positiveTweets/count,5), round(neutralTweets/count, 5), round(negativeTweets/count, 5), ") tweets")
	sentimentRatio = {}

	sentimentRatio["positivePercentage"]    = round(positiveTweets/count,5)
	sentimentRatio["neutralPercentage"]     = round(neutralTweets/count, 5)
	sentimentRatio["negativePercentage"]    = round(neutralTweets/count, 5)
	sentimentRatio["positiveCount"]  		= round(positiveTweets,5)
	sentimentRatio["neutralCount"]   		= round(neutralTweets, 5)
	sentimentRatio["negativeCount"]  		= round(neutralTweets, 5)
	outputJSON["sentiment"] = sentimentRatio



	allTweets.sort(key=lambda x: int(x["likes"]), reverse=True)
	topFiveTweets = allTweets[:5]
	outputJSON["topFiveTweets"] = topFiveTweets
	print(topFiveTweets)


	likes.sort()
	retweets.sort()
	likesWithImages.sort()

	#get most responded to people:
	tweetRespondedToUsersKeys = list(tweetRespondedToUsers.keys())
	tweetRespondedToUsersKeys.sort(key=lambda x: tweetRespondedToUsers[x][0], reverse=True)
	topFiveRespondingTo = tweetRespondedToUsersKeys[:5]
	topFiveReversed = topFiveRespondingTo[::-1]
	print("top five people responded to: ", topFiveRespondingTo)
	outputJSON["topFiveRespondedTo"] = topFiveRespondingTo


	name = makeHistogram("likes_histogram", likes, "likes per post", "# of posts in range", "Histogram of likes for "+screen_name+" tweets", absolute_path_to_figures)
	outputJSON["likes_histogram"] = name

	name = makeHistogram("likes_with_images_histogram", likesWithImages, "likes per post with image", "# of posts in range", "Histogram of likes for "+screen_name+"'s tweets with images", absolute_path_to_figures)
	outputJSON["likes_with_images_histogram"] = name

	name = makeHistogram("likes_for_retweets_histogram", likesForRetweet, "likes per retweet post", "# of posts in range", "Histogram of likes for tweets "+screen_name+" retweets", absolute_path_to_figures)
	outputJSON["likes_for_retweets_histogram"] = name

	name = makeHistogram("likes_for_original_histogram", likesForOriginal, "likes per original post", "# of posts in range", "Histogram of likes for "+screen_name+"'s original tweets", absolute_path_to_figures)
	outputJSON["likes_for_original_histogram"] = name

	name = createHorizontalSingleBarGraph(
		"responded_most",
		topFiveReversed,
		[tweetRespondedToUsers[x][0] for x in topFiveReversed],
		'Responses (#)',
		'Account (user name)',
		"Top 5 Accounts Responded To", absolute_path_to_figures)

	# createHorizontalDoubleBarGraph(
	# 	"RespondedMost2",
	# 	topFiveReversed,
	# 	[tweetRespondedToUsers[x][0] for x in topFiveReversed],
	# 	[tweetRespondedToUsers[x][1][0]["user"]["followers"] for x in topFiveReversed],
	# 	'Responses (#)',
	# 	'Account (user name)',
	# 	"Top 5 Accounts Responded To")

	#get most popular responded to people:
	tweetRespondedToUsersKeys = list(tweetRespondedToUsers.keys())
	tweetRespondedToUsersKeys.sort(key=lambda x: int(tweetRespondedToUsers[x][1][0]["user"]["followers"]), reverse=True)
	topFiveMostPopularRespondingTo = tweetRespondedToUsersKeys[:5]
	topFiveReversed = topFiveMostPopularRespondingTo[::-1]
	print("Top five most popular people responded to: ", topFiveMostPopularRespondingTo)
	outputJSON["topFiveMostPopularRespondingTo"] = topFiveMostPopularRespondingTo




	createHorizontalSingleBarGraph(
		"responded_popular",
		topFiveReversed,
		[int(tweetRespondedToUsers[x][1][0]["user"]["followers"]) for x in topFiveReversed],
		'Account Followers (#)',
		'Account (user name)',
		"Top 5 Most Popular Accounts Responded To", absolute_path_to_figures)

	# createHorizontalDoubleBarGraph(
	# 	"RespondedPopular2",
	# 	topFiveReversed,
	# 	[tweetRespondedToUsers[x][0] for x in topFiveReversed],
	# 	[tweetRespondedToUsers[x][1][0]["user"]["followers"] for x in topFiveReversed],
	# 	'Responses (#)',
	# 	'Account (user name)',
	# 	"Top 5 Most Popular Accounts Responded To")

	print("% tweets with no likes:", round(tweetsWithNoLikes/count, 5))
	outputJSON["no_likes_percent"] = round(tweetsWithNoLikes/count, 5)
	outputJSON["no_likes_count"] = round(tweetsWithNoLikes, 5)

	allTweets.sort(key=lambda x: int(x["likes"]), reverse=True)
	fivePercent = int(count*0.05)
	topFivePercentofTweets = allTweets[:fivePercent]
	# print(topFiveTweets["image"])
	countOfImagesInTopFivePercent = 0
	for tweet in topFivePercentofTweets:
		if tweet["images"] != '[]':
			countOfImagesInTopFivePercent += 1

	print("out of the top 5% of the tweets,", round(countOfImagesInTopFivePercent/fivePercent, 5), "had images")

	print("Median likes: ", round(likes[int(count/2)]))

	fig1, ax1 = plt.subplots()
	ax1.set_title('Basic Plot')
	ax1.boxplot(likes)
	fig1.show()
	print("Median likes with Images:", round(likesWithImages[int(tweetsWithImages/2)]))
	print("Median retweets: ", round(retweets[int(count/2)]))

	print("% of posts with images: ", round(tweetsWithImages/count,5))

	print("(responded tweets : self posted tweets) ratio: ", round(responseCount/(count - responseCount),5))

def computeStatistics(userinfo, vader):


# Computes scores for most of the metrics and returns an array
# with all this information
def computingScores(userinfo, vader):
	score = []
	# Gets all the tweets from a user
	all_tweets = get_all_tweets(screen_name)

	# Gets number of followers
	followers = userinfo['Followers']
	print("Follows " + str(followers))
	score.append(userinfo['Name'])

	# Frequency of Tweets
	score.insert(1, str(3.45))

	sum_of_likes = 0
	sum_of_retweets = 0
	for tweet in all_tweets:
		# Ratio between followers and posts that are favorited
		sum_of_likes += int(tweet["likes"])
		# Ratio between followers and posts that are retweeted
		sum_of_retweets += int(tweet["retweets"])

	favorites = (sum_of_likes / len(all_tweets))
	retweets = (sum_of_retweets / len(all_tweets))

	# We multiply by 10000 because the number is too small as it is
	ratio_fav = (favorites/int(followers))*10000
	score.insert(2, str(round(ratio_fav, 3)))

	# We multiply by 10000 because the number is too small as it is
	ratio_retw = (retweets/int(followers))*10000
	score.insert(3, str(round(ratio_retw, 3)))


	# Ratio between Verified followers and total followers
	# Currently hardcoded because data isn't obtainable yet
	verified = 400
	# We multiply by 10000 because the number is too small as it is
	ratio_verf = (verified/int(followers))*10000
	score.insert(4, str(round(ratio_verf, 3)))

	##### COMPUTING MEDIANS BEGINS HERE! #####

	# Checking if the current org already has data in the CSV
	count = 0
	# boolean that checks above condition
	is_there = False
	score_list = []
	# csv_file = industry + '_scores.csv'
	# open csv file
	with open(csv_file, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			if not is_there:
				count += 1
			name = userinfo['Name']
			elem = row[0]
			score_list.append(row)
			# if the twitter username appears in the csv
			if name.replace("\n", "") == elem.replace("\n", ""):
				is_there = True

	# Writing everything to a CSV file so that we can
	# compute the median later!
	if is_there:
		count -= 1
		# Overwrites the current data if we want to update information
		override = {count:[userinfo['Name'], ratio_fav, ratio_retw,
		ratio_verf, vader[0], vader[1]]}
		# opens csv for writing (in case of overwrite)
		with open(csv_file, 'w') as csvfile:
			score_writer = csv.writer(csvfile)
			# Overwrite each row in the csv (only changes one row though)
			for line, row in enumerate(score_list):
				data = override.get(line, row)
				score_writer.writerow(data)
	else:
		# opens csv for appending (if we are not overwriting, a.k.a user is new)
		with open(csv_file, 'a') as csvfile:
			score_writer = csv.writer(csvfile)
			# Append this row to the csv
			score_writer.writerow([userinfo['Name'], ratio_fav, ratio_retw,
				ratio_verf, vader[0], vader[1]])

	# dictionary with all the data from each score
	data = {'engagement': score, 'reactions': vader}
	return data


def createImagePallete(colors, path):
	rows = int(len(colors)/100) if len(colors) > 100 else 8
	pallete = sorted(colors, key=lambda rgb : step(rgb,rows))

	# rows = int(len(pallete)/100) if len(pallete) > 100 else 8
	pallete = pallete[:len(pallete)-len(pallete)%rows]

	palette = np.array(chunkIt(pallete, rows))
	# indices = np.random.randint(0, len(palette), size=(4, 6))
	# print(palette)
	plt.imshow(palette)

	ax = plt.subplot(111)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines["bottom"].set_visible(False)
	ax.spines["left"].set_visible(False)
	plt.title("Color Pallete for "+ screen_name, fontsize=18)
	ymin, ymax = ax.get_ylim()
	print(ymax)
	plt.text(0, -1 * ymax/10, "Data source: www.twitter.com", fontsize=10)
	plt.axis('off')
	plt.tight_layout()
	# plt.colorbar()
	photoName = screen_name + "_pallete" + '.pdf'
	plt.savefig(path + photoName)
	return photoName
	# plt.show()

def createHorizontalSingleBarGraph(name, x, y, x_axis, y_axis, title, path):
	plt.clf()
	y_pos = np.arange(len(x))
	ax = plt.subplot(111)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	arr = plt.barh(y_pos, y, align='center', alpha=0.5)
	plt.yticks(y_pos, x, fontsize=14)
	plt.xticks(fontsize=14)
	plt.xlabel(x_axis, fontsize=16)
	plt.ylabel(y_axis, fontsize=16)
	plt.title(title, fontsize=22)
	for i, v in enumerate(y):
		ax.text(v, i, str("{:,}".format(v)),  fontweight='bold')
	plt.text(0, -1.25, "Data source: www.twitter.com"
			 "", fontsize=10)
	plt.tight_layout()

	plt.savefig(path + screen_name + "_" + name + '.pdf')
	return screen_name + name
	# plt.show()

def createHorizontalDoubleBarGraph(name, x, y1, y2, x_axis, y_axis, title, path):
	fig, ax1 = plt.subplots()

	color = 'tab:red'
	y_pos = np.arange(len(x))
	ax1.set_ylabel('time (s)')
	ax1.set_xlabel('exp', color=color)
	ax1.barh(y_pos, y1, align='center', color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

	color = 'tab:blue'
	ax2.set_xlabel('sin', color=color)  # we already handled the x-label with ax1
	ax2.barh(y_pos, y2, align='center', color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()

	plt.savefig(path + name + '.pdf')

def makeHistogram(name, data, x_axis, y_axis, title, path):
	plt.clf()
	plt.figure(figsize=(12, 9))
	ax = plt.subplot(111)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	plt.xticks(fontsize=14)
	plt.yticks(fontsize=14)
	plt.xlabel(x_axis, fontsize=16)
	plt.ylabel(y_axis, fontsize=16)
	plt.title(title,   fontsize=22)
	bins = 50

	arr = plt.hist(list(data),
			  alpha=0.5, bins=50)
	ymin, ymax = ax.get_ylim()
	for i in range(bins):
		if arr[0][i] != 0:
			plt.text(arr[1][i],arr[0][i]+ymax/90,str("{:,}".format(int(arr[0][i]))),fontweight='bold')

	plt.text(0, -1 * ymax/10, "Data source: www.twitter.com", fontsize=10)
	plt.tight_layout()
	box_inches="tight" #removes all the extra whitespace on the edges of your plot.
	print(path + screen_name + "_" + name + '.pdf')
	plt.savefig(path + screen_name + "_" + name + '.pdf')
	# plt.show()
	return name + '.pdf'


if __name__ == '__main__':
	# pass in the username of the account you want to download
	screen_name = sys.argv[1]

	absolute_path_to_screen_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ),  screen_name)) + '/'
	absolute_path_to_images = os.path.join(absolute_path_to_screen_name, 'images') + '/'
	absolute_path_to_saveFiles = os.path.join(absolute_path_to_screen_name, 'files') + '/'
	absolute_path_to_figures = os.path.join(absolute_path_to_screen_name, 'figures') + '/'

	userinfo = getUserInformation(screen_name)
	allTweets = get_all_tweets(screen_name)


	processTwitterInfo(allTweets, userinfo)
	# computingScores(userinfo, getVaderAnalysis(screen_name))
