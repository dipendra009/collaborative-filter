import sys
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
import math, datetime
from scipy.stats import mode


def getrating(data, uid, mid):
	for d in data:
		#print d
		if d[0]== uid and d[1] == mid:
			return d[2]
	return 0		

#scipy.stats.pearson(array1, array2)
def pearsoncor(a,b):
	n = len(a)
	nf = float(n)
	meana = sum(a)/nf
	meanb = sum(b)/nf
	num = 0
	denuma = 0
	denumb = 0
	for x in range(n):
		va = meana - a[x]
		vb = meanb - b[x]
		num = num + va * vb
		denuma = denuma + va * va
		denumb = denumb + vb * vb
	denum = math.sqrt(denuma)*math.sqrt(denumb)

	sim = num/denum
	return sim



def manhattandist(a,b):
	dist = 0
	for x in range(len(a)):
		dist = dist + abs(a[x] - b[x])
	return dist	 

def item_cf(data, uids, mids, userID, movieID, distance, k, i):
	movies = []
	def getrating(uid, mid):
		for d in rdata[mid]:
			if d[0]== uid and d[1] == mid:
				rdata[mid].remove(d)
				return d[2]
		return 0		
	

	movies.append([0 for x in range(len(uids))])
	 
	 
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
	
	dists = []
	mdata = movies[movieID]
	for mn in mids:
		if mn == movieID:
			continue
		if distance:
			dis = manhattandist(mdata, movies[mn])
		else:
			sim = pearsoncor(mdata, movies[mn])
			# convert into distance from similarity
			dis = 1 - sim
		# only consider people with rating if i == 1
		if i == 1:
			if movies[mn][userID] == 0:
				continue			
		dists.append([mn, dis])
	for x in range(len(dists)):
		for y in range(x, len(dists)):
			if dists[y][1] < dists[x][1]:
				dists[x], dists[y] = dists[y], dists[x]
	 
	l = k
	if k > len(dists):
		l = len(dists)
		
	kratings = []
	for x in range(l):
	 	kratings.append(movies[dists[x][0]][userID])
	kratings = sorted(kratings)
	m = l/2
	if k%2 == 0:
		urating = float((kratings[m-1] + kratings[m]))/2
	else:
		urating = kratings[int(m)]
	return urating
	 

def user_cf(data, uids, mids, userID, movieID, distance, k, i):
	people = []
	def getrating(uid, mid):
		for d in rdata[mid]:
			
			if d[0]== uid and d[1] == mid:
				rdata[mid].remove(d)
				return d[2]
		return 0		
	people.append([0 for x in range(len(mids))])
	rdata = [[] for x in range(len(mids)+1)]
 	for d in data:
 		rdata[d[1]].append(d)
	for un in uids:
		people.append([])
		prs = []
		prs.append(0)
		for mn in mids:
			prs.append(0)
			rat = getrating(un, mn)
			prs[mn] = rat
		people[un] = prs
	
	
	# finding top k

	dists = []
	udata = people[userID]
	for un in uids:
		if un == userID:
			continue
		if distance:
			dis = manhattandist(udata, people[un])
		else:
			sim = pearsoncor(udata, people[un])
			# convert into distance from similarity
			dis = 1 - sim
		# only consider people with rating if i == 1
		if i == 1:
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

	l = k
	if k > len(dists):
		l = len(dists)
		
	kratings = []
	for x in range(l):
		kratings.append(people[dists[x][0]][movieID])
	
	urating = mode(kratings)
	urating =  float(urating[0])
	return urating
	 

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
	

def plotgraphs(datafile):
	# Read data from file
	data, mids, uids = read_file(datafile)
	print len(data)
	people = []
	rdata = [[] for x in range(len(mids)+1)]
 	for d in data:
 		rdata[d[1]].append(d)
	
	def getrating(uid, mid):
		for d in rdata[mid]:
			
			if d[0]== uid and d[1] == mid:
				rdata[mid].remove(d)
				return d[2]
		return 0		
	
	people.append([0 for x in range(len(mids))])
	for un in uids:
		people.append([])
		prs = []
		prs.append(0)
		for mn in mids:
			prs.append(0)
			rat = getrating(un, mn)
			prs[mn] = rat
		people[un] = prs
	nperson = len(uids)
	pairperson = 0
	nmovieslist = []
	for x in range(nperson):
		for y in range(x+1, nperson):
			nmovies = 0
			for z in range(len(mids)):
				if people[x][z] != 0 and people[y][z] != 0:
					nmovies = nmovies + 1
			nmovieslist.append(nmovies)
	nmovieslist = list(sorted(nmovieslist))
	mean = sum(nmovieslist)/len(nmovieslist)
	median = nmovieslist[int(len(nmovieslist)/2)]
	#print nmovieslist
	print "mean: ", mean 
	print "median: ", median
	plt.hist(nmovieslist,len(set(nmovieslist))-1) 
	plt.xlim(min(nmovieslist), max(nmovieslist))
	plt.xlabel("Number of movies reviewed in common")
	plt.ylabel("Number of user pairs")
	plt.savefig("3asolution.pdf")
	plt.close()
	
	rdata = [[] for x in range(len(mids)+1)]
 	for d in data:
 		rdata[d[1]].append(d)
	
	movies = []
	movies.append(0)
	for mn in mids:
		movies.append(0)
		numrev = 0
		for un in uids:
			rat = getrating(un, mn)
			if rat != 0:
				numrev = numrev + 1
		movies[mn] = numrev
		#print mn, movies[mn], numrev
	#print len(movies) 
	
	print "maximum: ", movies.index(max(movies)), max(movies)
	movies = movies[1:]
	print "miniumum: ", movies.index(min(movies))+1, min(movies)
	movies = list(sorted(movies))
	#print movies
	movies.reverse()
	plt.plot(range(1, len(movies)+1), movies)
	plt.xlabel("Movie's number in order")
	plt.ylabel("Number of reviews")
	#plt.show()
	
	plt.savefig("3bsolutoin.pdf")
	plt.close()


 		

if __name__ == "__main__":
	# A fully specified path to a file like u.data
	datafile = sys.argv[1]
	plotgraphs(datafile )





















