import sys
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
import math, datetime
from scipy.stats import mode

""""
This is an cross validation program with item_based and user_based collaborative filter. Here we use the Pearson correlation or Manhattan distance to calculate
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
		return 0

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
		
 	

# Predicts the rating with item-based collaborative filtering

def item_cf(data, uids, mids, userID, movieID, distance, k, i):
	
	# This is the list of movies, each have 943-element vector and ith element contains the ratings fo the movie by user i
	movies = []
	def getrating(uid, mid):
		for d in rdata[mid]:
			if d[0]== uid and d[1] == mid:
				rdata[mid].remove(d)
				return d[2]
		return 0		
	

	movies.append([0 for x in range(len(uids))])
	 	 
	# To speed up, divide data
	rdata = [[] for x in range(len(mids)+1)]
 	
 	for d in data:
 		rdata[d[1]].append(d)
	
	for mn in mids:
		movies.append([])
		mrs = []
		mrs.append(0)
		for un in uids:
			mrs.append(0)
			rat = getrating(un, mn)
			mrs[un] = rat
			#print mrs[un], rat
			 
		movies[mn] = mrs
	
	# To store distance metric for different movies
	dists = []
	
	# Ratings for movieID
	mdata = movies[movieID]
	
	for mn in mids:
		if mn == movieID:
			continue
		if distance:
			dis = manhattandist(mdata, movies[mn], userID)
		else:
			sim = pearsoncor(mdata, movies[mn], userID)
			# convert into distance from similarity
			dis = 1 - sim
		
		# only consider people with rating if i == 0
		if i == 0:
			if movies[mn][userID] == 0:
				continue			
		dists.append([mn, dis])
	
	for x in range(len(dists)):
		for y in range(x, len(dists)):
			if dists[y][1] < dists[x][1]:
				dists[x], dists[y] = dists[y], dists[x]
	 
	
	# Find K neighbors
	l = k
	
	# If available rating is less than for K, correct K to size of available neighbors
	if k > len(dists):
		l = len(dists)
	

	kratings = []
	for x in range(l):
	 	kratings.append(movies[dists[x][0]][userID])
	kratings = sorted(kratings)
	
	# Use mode returned by scipy.stats
	urating = mode(kratings)
	urating =  float(urating[0])
	truerating = mdata[userID]
	return urating, truerating


def cross_valid(datafile, use_user, distance, k, i):
	data, mids, uids = read_file(datafile)
	print "datafile: ", datafile
	print "user_user: ", use_user
	print "distance: ", distance
	print "k ", k
	print "i ", i
	#print len(data)

	datatest = [[] for x in range(50)]
	datarest = [[] for x in range(50)]
	 
	for x in range(50):
		start = x * 2000
		end = start + 2000
		datatest[x] = data[start:end]
		datarest[x] = data[:start] + data[end:]
		#print len(datatest[x]), len(datarest[x])

	avgerrors = [0 for x in range(50)]
	tim = datetime.datetime.now()
	
	for x in range(50):
		dt = datatest[x]
		dr = datarest[x]
		error = 0.0
		j = 0
		nums = np.random.randint(0,2000, 10)
		for y in nums:
			d = dt[y]
	 		uid = d[0]
	 		mid = d[1]
	 		truerating = d[2]
	 		try:
	 			if use_user:
	 				predrating, trurating = user_cf(dr, uids, mids, uid, mid, distance, k, i)
	 			else:
	 				predrating, trurating = item_cf(dr, uids, mids, uid, mid, distance, k, i)	 
	 		except:
	 			continue		
	 		# define error as absolute difference between truerating and predrating
	 		cerror = abs(truerating - predrating)
	 		error = error + cerror
	 		print "x: ",x, " j: ", j, " truerating: ", truerating," predictedrating: ", predrating, " cerror: ", cerror 
	 		j = j+1
	 	avgerrors[x] = error/10

	print "Average error: ", sum(avgerrors)/50
	print avgerrors
	tim = str(tim)
	tim = tim.replace(": ", "")
	tim = tim.replace(" ", "")
	fil = open(tim, "w")
	fil.write("\n Userusr: "+str(use_user)+"\tDistance: "+ str(distance) + "\tk: "+ str(k)+ "\ti: "+ str(i)+ "\n\naverageerrors: "+ str(avgerrors))
	fil.close()


 		

if __name__ == "__main__":
	# A fully specified path to a file like u.data
	print "Usage: python crossvalidation.py u.data user_user distance k i"
	datafile = sys.argv[1]
	use_user = int(sys.argv[2])
	if use_user==1:
		use_user = True
	else:
		use_user = False

	distance = int(sys.argv[3])
	if distance == 1:
		distance = True
	else:
		distance = False	
	# number of nearest neighbors to consider
	k = int(sys.argv[4])
	# boolean value. If set to 0 for user-based, only users that have actual ratings for the movie are considered in your top K
	# for item-based, only movies that have actual ratings by the user in your top K
	# else consider top K with actual or filled-in value

	# movies will each have a 943-element vector and ith element will contain the ratings of that movie by user i
	# people will have 1682 element vectors, where the jth element contains that user's ratings for movie j
	# missing rating should be filled by 0
	# predicted rating returned will be mode of the top K neighbors

	i = int(sys.argv[5])
	cross_valid(datafile, use_user, distance, k, i)





















