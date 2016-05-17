# File: Clustering.py
# Author: John Gordon     Email: gordon8@umbc.edu
# Run program with: python3 Clustering.py numberOfClusters file.txt
# file.txt - A series of 2d points, format: x,y

# Description: Program displays a graph of the points from file.txt divided into their
# clusters.

import sys
import matplotlib.pyplot as plt
import random
import math

# Set initial centroids
def initCentroids(numClusters, points):

    cents = []
    nums = []
    if(numClusters <= len(points)):
        # Generate random initial centroids for amount of clusters
        while(len(nums) != numClusters):
            # Pick a point randomly
            num1 = random.randint(0, len(points)-1)
            if num1 not in nums:
                nums.append(num1)
                cents.append(points[num1])

    # Else, there will be more clusters than points; so there will be same clusters
    else:
        for i in range(0,numClusters):
            num1 = random.randint(0, len(points)-1)
            cents.append(points[num1])

    return cents

# Calculates and sets the clusters based off the current centroids
def setClusters(centroids, points, clusters, pointDists):

    i = 0    # Increment for current point distance from nearest centroid
    flag = False    # Flag to see if a cluster was updated (for while loop check)
    for p in points:
        pos = 0
        clustPos = -1
        for c in centroids:
            # Distance between point and centroid
            # Distance formula: sqrt((x2-x1)^2 + (y2-y1)^2)
            dist = math.sqrt((abs(c[0]-p[0])**2) + (abs((c[1]-p[1]))**2))

            # If distance is less than previous point-centroid distance
            if dist < pointDists[i]:
                pointDists[i] = dist
                clustPos = pos

            pos += 1
        
        # Add the point to the cluster element that correlates to which centroid caused
        # the least distance
        # If there was an update with a point-centroid distance
        if(clustPos != -1):
            cPos = 0
            # Check if point is already in cluster, if it is, update the list appropriately
            for clust in clusters:
                if p in clust:
                    clust.remove(p)
                    # If point changes which cluster its in
                    if cPos != clustPos:
                        flag = True

                cPos += 1

            clusters[clustPos].append(p)

        i += 1

    return clusters, pointDists, flag

# Update centroids
# New centroid = mean of points currently in associated cluster
def getCentroids(centroids, clusters):

    i = 0    # Increment for current cluster/centroid
    # For each cluster, get mean x and y for new centroid
    for clust in clusters:
        num, totalX, totalY, avgX, avgY = 0, 0, 0, 0, 0
        for point in clust:
            num += 1
            totalX += point[0]
            totalY += point[1]

        avgX = totalX/float(num)
        avgY = totalY/float(num)
        centroids[i] = [avgX,avgY]
        i += 1

    return centroids

def main(argv):

    points = []
    clusters = []
    # Create list of lists according to num of clusters
    for i in range(0,int(argv[1])):
        clusters.append([])

    ''' File I/O '''
    # Read in file, split at comma each line to get list of coordinate
    with open(argv[2]) as f:
        for line in f:
            line2 = line.split(',')
            num = 0
            # Need to strip return char and make number an int
            for p in line2:
                if '\n' in p:
                    p = p.strip('\n')
                    
                p = int(p)
                line2[num] = p
                num += 1

            points.append(line2)

    # Create list for point-centroid distances
    pointDists = []
    for n in range(0,len(points)):
        pointDists.append(sys.maxsize)

    ### First get initial k centroids (k = numberOfClusters)
    # centroids - list of coordinates of the current centroids
    k = int(argv[1])
    centroids = initCentroids(k, points)
    print("initial centroids:",centroids, '\n')

    ##### While loop - Until assignments of clusters and centroids can no longer change
    # or until 300 iterations (which ever comes first)
    flag, flag2, count, count2 = False, True, 0, 0
    while(flag2 and (count < 300)):

        ### Next, calculate which cluster each point belongs to.
        clusters, pointDists, flag = setClusters(centroids, points, clusters, pointDists)


        ### Then update centroids based on current clusters
        centroids = getCentroids(centroids, clusters)

        # If there is no new assignment of clusters
        if(flag):
            count2 += 1
        else:
            count2 = 0
        # If there are no new assignments more than 50 times consecutively
        if(count2 > 50):
            print("Clusters cannot change anymore. Exiting loop...")
            flag2 = False

        count += 1

    #### End while
    print("centroids:",centroids, '\n')
    print("clusters:",clusters)
    minX, minY, maxX, maxY = sys.maxsize, sys.maxsize, 0, 0
    for point in points:
        if point[0] < minX:
            minX = point[0]
        if point[1] < minY:
            minY = point[1]
        if point[0] > maxX:
            maxX = point[0]
        if point[1] > maxY:
            maxY = point[1]

    # Plot final clusters and centroids
    i = 0
    j = 0
    colors = ['b','g','r','c','m','y','k']
    plt.title('K-Means Clusters')
    plt.axis([minX-1, maxX+1, minY-1, maxY+1])
    plt.grid(True)
    for clust in clusters:
        for point in clust:
            if i == len(colors):
                i = 0
            # Plot point in cluster
            plt.plot(point[0],point[1],colors[i]+'o')

        # Plot centroid
        plt.plot(centroids[j][0],centroids[j][1],colors[i]+'*')
        i += 1
        j += 1
    plt.show()

if __name__ == "__main__":
    main(sys.argv)
