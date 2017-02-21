import sys
import csv
import numpy as np
import scipy

def perceptrona(w_init, X, Y):
	#figure out (w, k) and return them here. w is the vector of weights, k is how many iterations it took to converge.
	# initialising w (weight) and k (epoch)
	w = np.array(w_init)
	k = 0
	# modify X vector -> [1, X^2, X]
	# Bias = 1
	X_new = []
	for x in X:
	    X_new.append([1, x*x, x])
	#Creating np array type
	X_new=np.array(X_new)
	mismatch=True
	while mismatch==True:
	   mismatch=False
	   # increase Epoch
	   k=k+1
	   # iterating over all the training set
	   for i in range(len(X)):
	       # W0 + W1*X^2 + W2*X
	      det = w[0] + w[1]*X_new[i][1] + w[2]*X_new[i][2]
	      # Classify properly
	      class_type = 1.0
	      if det < 0:
	         class_type=-1.0
	      # If there is mis classification
	      if class_type!=Y[i]: 
	          mismatch=True
	          w[0]=w[0]+(Y[i]*X_new[i][0])
	          w[1]=w[1]+(Y[i]*X_new[i][1])	
	          w[2]=w[2]+(Y[i]*X_new[i][2])	
	print "Value of Epoch: "+ str(k)
	print "Values of W: "+str(w[0])+ '  '+str(w[1])+ '   '+str(w[2])
	return (w, k)


def main():
	rfile = sys.argv[1]
	
	#read in csv file into np.arrays X1, X2, Y1, Y2
	csvfile = open(rfile, 'rb')
	dat = csv.reader(csvfile, delimiter=',')
	X1 = []
	Y1 = []
	X2 = []
	Y2 = []
	for i, row in enumerate(dat):
		if i > 0:
			X1.append(float(row[0]))
			X2.append(float(row[1]))
			Y1.append(float(row[2]))
			Y2.append(float(row[3]))
	X1 = np.array(X1)
	X2 = np.array(X2)
	Y1 = np.array(Y1)
	Y2 = np.array(Y2)
	# initialising w_init with more dimensionality
	w_init = np.array([0.0,0.0, 0.0])
	#perceptrona(w_init, X1, Y1)
	perceptrona(w_init, X2, Y2)

if __name__ == "__main__":
	main()
