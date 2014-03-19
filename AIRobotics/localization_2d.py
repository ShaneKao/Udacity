#!/usr/bin/python


# P(Color|SeeColor) = sensor_right * P(in color) + sensor_wrong * P(no in color)
# P(Color|SeeColor) = sensor_right
# P(NotColor|SeeColor) = 1 - sensor_right
# P(InRed|SeeRed) = sensor_right
# P(InGreen|SeeRed) = 1 - sensor_right
# P(InGreen|SeeGreen) = sensor_right
# P(InRed|SeeGreen) = 1-sensor_right
# 
def sense( measurement):
	q = []
    
	pCorrectCollor = 1.0

	pSum = 0
	for i in range (len(colors)):
		tempRow=[]
		
		for j in range(len(colors[i])):
			matches = (colors[i][j] == measurement)
			
			# P(InColor|ColorSeen)
			pCC = sensor_right
			pnCC = 1.000 - sensor_right 
			
			if matches:
				newprob = pCC * p[i][j]
				#print "match new prob is " + str(newprob) + " multiplied " + str(pCC) + " x " + str(p[i][j]) + " in cell " + str(i) + ", " + str(j)
				pSum = pSum + newprob
				tempRow.append(newprob)
			else:
				newprob = pnCC * p[i][j]
				#print "no match new prob is " + str(newprob)
				pSum = pSum + newprob
				tempRow.append(newprob)
				

		q.append(tempRow)
	#print "pSum is " + str(pSum)
	for i in range (len(colors)):
		for j in range(len(colors[i])):
			if pSum == 0:
				q[i][j] = 0
			else:
				q[i][j] = q[i][j] / pSum
			
	return q


# [0,0] - no move
# 0,1 right
# 0,-1 left
# 1,0 down
# -1, 0 up


def moveHorizontal(motion):
	H = motion[1]
	
	q = []
	
	for i in range(len(colors)):
		newRow = []
		for j in range(len(colors[i])):
			oldX = ( j - H ) % len(colors[i])
			newRow.append( (p[i][oldX] * p_move) + (p[i][j] * ( 1.00 - p_move)) )
			#print "putting old x value of "  + str(oldX) + " into " + str(i) + ", " + str(j)
		
		
		q.append(newRow)
	
	#print "moved horizontal " + str(H)
	return q

def moveVertical(motion):
	V = motion[0]
	q = []

	for i in range(len(colors)):
		newRow = []
		for j in range(len(colors[i])):
			oldY = (i - V) % len(colors)
			newRow.append(p[oldY][j] * p_move  + p[i][j] * ( 1.00 - p_move))
		

		q.append(newRow)

	#print "moved vertical " + str(V)
	return q
	
def move(motion):
	q = p
	
	if motion[1] != 0:
		q = moveHorizontal(motion)
	elif motion[0] != 0:
		q = moveVertical(motion)
	elif sum(motion) == 0:
		#print "NO MOVE"
		q = p
	else:
		print "no motion found"
	
	return q

def printList(lst):
	for i in range(len(lst)):
		print lst[i]
		
# colors=[['green', 'green', 'green' ],
# 		['green',   'red',   'red'],
# 		['green', 'green', 'green',]]
# 		
# measurements=['red', 'red']
# motions=[[0,0], [0,1]]

colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

numrows = len(colors)
numcols = len(colors[0])
cells = numrows * numcols
uniformProb = 1.000/cells
#print "uniform prob is " + str(uniformProb)
p=[]
totalRed = 0

for i in range(len(colors)):
	
	row = []
	for j in range(len(colors[i])):
		row.append(uniformProb)
		if colors[i][j] == 'red':
			totalRed += 1
	
	p.append(row)

#pRed = 1.0000 * totalRed / cells
#pGreen = 1.0000 - pRed

#print "Initial probs:"
#print printList(p)

for i in range(len(motions)):
	p=move(motions[i])
	p=sense(measurements[i])
	#print "\nAfter move and sense sense " + str(i+1)
	#printList(p)



#print "\n\nFinal:\n"
printList( p)	

psum = 0
for i in range(len(p)):
	for j in range(len(p[i])):
		psum = psum + p[i][j]
		

		
print "Sum of p is " + str(psum)
	