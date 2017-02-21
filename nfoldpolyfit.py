#	Starter code for linear regression problem
#	Below are all the modules that you'll need to have working to complete this problem
#	Some helpful functions: np.polyfit, scipy.polyval, zip, np.random.shuffle, np.argmin, np.sum, plt.boxplot, plt.subplot, plt.figure, plt.title
import sys
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
import random
import math

def nfoldpolyfit(X, Y, maxK, n, verbose):
#	NFOLDPOLYFIT Fit polynomial of the best degree to data.
#   NFOLDPOLYFIT(X,Y,maxDegree, nFold, verbose) finds and returns the coefficients 
#   of a polynomial P(X) of a degree between 1 and N that fits the data Y 
#   best in a least-squares sense, averaged over nFold trials of cross validation.
#
#   P is a vector (in numpy) of length N+1 containing the polynomial coefficients in
#   descending powers, P(1)*X^N + P(2)*X^(N-1) +...+ P(N)*X + P(N+1). use
#   numpy.polyval(P,Z) for some vector of input Z to see the output.
#
#   X and Y are vectors of datapoints specifying  input (X) and output (Y)
#   of the function to be learned. Class support for inputs X,Y: 
#   float, double, single
#
#   maxDegree is the highest degree polynomial to be tried. For example, if
#   maxDegree = 3, then polynomials of degree 0, 1, 2, 3 would be tried.
#
#   nFold sets the number of folds in nfold cross validation when finding
#   the best polynomial. Data is split into n parts and the polynomial is run n
#   times for each degree: testing on 1/n data points and training on the
#   rest.
#
#   verbose, if set to 1 shows mean squared erroror as a function of the 
#   degrees of the polynomial on one plot, and displays the fit of the best
#   polynomial to the data in a second plot.
#   
#
#   AUTHOR: Dipendra Kumar Jha (This is where you put your name)
#
        # At first we have to randomize the dataset
        randomX = np.array(X)
        randomY = np.array(Y)
        rand = []
        for i in range(30):
            rand.append(i)
        # Shuffling the array values using random    
        random.shuffle(rand)
        for i in range(30):
            randomX[i] = X[rand[i]]
            randomY[i] = Y[rand[i]]
        x_trainset=[]
        x_testset=[]
        y_trainset=[]
        y_testset=[]
        # Now, we have to create 30/n test datasets of n-size for n-fold cross validation
        trainset_count = 30//n
        # Each time we will create 30-n size train set as well
        for i in range(trainset_count): 
            x_testset.append(np.array(randomX[(i*n):((i+1)*n)]))
            y_testset.append(np.array(randomY[(i*n):((i+1)*n)]))
            x_trainset.append(np.concatenate((np.array(randomX[:(i*n)]), np.array(randomX[((i+1)*n):])), axis=0))
            y_trainset.append(np.concatenate((np.array(randomY[:(i*n)]), np.array(randomY[((i+1)*n):])), axis=0))   
     
        # A large value of optimal MSE
        least_MSE = 658556  
        all_MSE = []
        k_optimal = 0  
        # for all values 0, 1, ..., maxK
        for k in range(maxK+1):
            MSE=[]
            # iterating over the validation set
            for i in range(trainset_count):
                weights = np.polyfit(x_trainset[i], y_trainset[i], k)
                poly = np.poly1d(weights)
                # testing the found polynomials   
                summation=0
                for j in range(n):
                    x=x_testset[i][j]
                    y=y_testset[i][j]
                    y_p = poly(x)
                    error = y_p - y
                    summation = summation + math.pow(error, 2)
                curMSE=summation/n
                MSE.append(curMSE)
            finalMSE = sum(MSE)/trainset_count
            all_MSE.append(finalMSE)
            # keep tracking the optimal MSE
            if(finalMSE < least_MSE):
                least_MSE=finalMSE
                k_optimal=k
        print 'The optimal value of k is: ' + str(k_optimal)
        # Plot graphs
        K_domain=[]
        for i in range(maxK+1):
            K_domain.append(i)
        #  x-axis: k, y-axis-MSE graph 
        plt.plot(K_domain, all_MSE, '-')
        plt.show()
        # plotting the polynomials to fit the points
        optimal_weights=np.polyfit(randomX, randomY, k_optimal)
        optimal_poly=np.poly1d(optimal_weights)
        xp = np.linspace(np.amin(X, axis=0), np.amax(X, axis=0), 30)
        plt.plot(randomX, randomY, '.', xp, optimal_poly(xp), '-')
        plt.show() 
        # Value needed for question 1(c)
        print 'The predicted value of x=3: '+str(optimal_poly(3))
                                             
def main():
	# read in system arguments, first the csv file, max degree fit, number of folds, verbose
	rfile = sys.argv[1]
	maxK = int(sys.argv[2])
	nFolds = int(sys.argv[3])
	verbose = bool(sys.argv[4])
	
	csvfile = open(rfile, 'rb')
	dat = csv.reader(csvfile, delimiter=',')
	X = []
	Y = []
	# put the x coordinates in the list X, the y coordinates in the list Y
	for i, row in enumerate(dat):
		if i > 0:
			X.append(float(row[0]))
			Y.append(float(row[1]))
	X = np.array(X)
	Y = np.array(Y)
	nfoldpolyfit(X, Y, maxK, nFolds, verbose)

if __name__ == "__main__":
	main()
