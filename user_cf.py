import sys
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
import math
from scipy.stats import mode

""""
This is an user_based collaborative filter. Here we use the Pearson correlation or Manhattan distance to calculate
distance. In case of Pearson'correlation, we calculate distance using distance = 1 - sim. While measuring the distance
and sim, we do not use the true rating for the userID, movieID to be predicted. We replace the missing values with 0.
So, if the truerating for a movieID, userID is missing, it will be 0 in our case.

"""

# Gives rating for a userID, movieID pair
def getrating(data, uid, mid):
	for d in data:
		#print d
		if d[0]== uid and d[1] == mid:
			return d[2]
	return 0		

#scipy.stats.pearson(array1, array2)

# Calculated Pearson'correlation for two vectors a, b without considering the rating for the userID/movieID to be predicted
def pearsoncor(a,b, pid):
	n = len(a)
	nf = float(n)
	meana = sum(a)/nf
	meanb = sum(b)/nf
	num = 0
	denuma = 0
	denumb = 0
	for x in range(n):
		if x == pid:
			continue
		va = meana - a[x]
		vb = meanb - b[x]
		num = num + va * vb
		denuma = denuma + va * va
		denumb = denumb + vb * vb
	denum = math.sqrt(denuma)*math.sqrt(denumb)
	if denum == 0:
		return 1
	sim = num/denum
	return sim

# Calculated manhattandist for two vectors a, b without considering the rating for the userID/movieID to be predicted
def manhattandist(a,b, pid):
	dist = 0
	for x in range(len(a)):
		# Do not use the rating which we need to predict
		if x == pid:
			continue
		dist = dist + abs(a[x] - b[x])
	return dist	 

# Reads data from datafile and return list of tuples and also userIDs and movieIDs
def read_file(datafile):
	dfile = open(datafile, "r")
	dat = dfile.read().strip()
	dat = dat.split("\n")
	data = [] 
	mids = []
	ratings = []
	uids = []
	for d in dat:
		# userid, itemid, rating, timestamp
		d = d.split("\t")
		uid = int(d[0])
		iid = int(d[1])
		rating = int(d[2])
		tstamp = int(d[3])
		uids.append(uid)
		mids.append(iid)
		data.append([uid, iid, rating, tstamp])
	mids = list(set(sorted(mids)))
	uids = list(set(sorted(uids)))
	return data, mids, uids

# Predicts the rating with user_based collaborative filtering

def user_cf(data, uids, mids, userID, movieID, distance, k, i):
	
	# people will have 1682 element vectors, where the jth element contains that user's ratings for movie j
	people = []
	
	people.append([0 for x in range(len(mids))])
	
	rdata = [[] for x in range(len(mids)+1)]
 	
 	for d in data:
 		rdata[d[1]].append(d)
	
	def getrating(uid, mid):
		for d in rdata[mid]:
			
			if d[0]== uid and d[1] == mid:
				rdata[mid].remove(d)
				return d[2]
		return 0		
	
	for un in uids:
		people.append([])
		prs = []
		prs.append(0)
		for mn in mids:
			prs.append(0)
			rat = getrating(un, mn)
			prs[mn] = rat
		people[un] = prs
	
	
 	# To store distance metric for different movies
	dists = []

	# Ratings for userID
	udata = people[userID]

	for un in uids:
		if un == userID:
			continue
		if distance:
			dis = manhattandist(udata, people[un], movieID)
		else:
			sim = pearsoncor(udata, people[un], movieID)
			# convert into distance from similarity
			dis = 1 - sim
		
		# only consider people with rating if i == 0
		if i == 0:
			if people[un][movieID] == 0:
				continue			
		dists.append([un, dis])
	 	
	for x in range(len(dists)):
		nosort = True
		for y in range(x, len(dists)):
			if dists[y][1] < dists[x][1]:
				nosort = False
				dists[x], dists[y] = dists[y], dists[x]
	 	if nosort:
	 		break

	# Find k neighbors 		
	l = k

	# If available rating is less than for K, correct K to size of available neighbors
	if k > len(dists):
		l = len(dists)
		
	kratings = []
	for x in range(l):
		kratings.append(people[dists[x][0]][movieID])
	
	# Use mode returned by scipy.stats
	urating = mode(kratings)
	urating =  float(urating[0])
	truerating = udata[movieID]
	return urating, truerating
		
		

if __name__ == "__main__":
	
	# A fully specified path to a file like u.data
	datafile = sys.argv[1]
	
	userID = int(sys.argv[2])
	movieID = int(sys.argv[3])
	
	# a boolean, if set to 0, use Pearson correlation else use Manhattan distance
	distance = int(sys.argv[4])
	if distance == 1:
		distance = True
	else:
		distance = False	
	
	# number of nearest neighbors to consider
	k = int(sys.argv[5])
	
	# boolean value. If set to 0 for user-based, only users that have actual ratings for the movie are considered in your top K
	# for item-based, only movies that have actual ratings by the user in your top K
	# else consider top K with actual or filled-in value

	i = int(sys.argv[6])
	
	# Read data from file
	data, mids, uids = read_file(datafile)

	# Use user_based method

	predrating, truerating = user_cf(data, uids, mids, userID, movieID, distance, k, i)
	print "userID:%d\tmovieID:%d\ttrueRating:%d\tpredictedRating:%d\tdistance:%d\tK:%d\tI:%d"%(userID,movieID,truerating,predrating,distance,k,i)		
	
