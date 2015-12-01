import sys
import random
import operator
#--------------------------------------------------------------------
#       TO DO:
#               3 Input Files by Wednesday
#               Implement Smart Algorithms
#               Come up with team name
#               Double check what we need to turn in (including student id # stuff)
#--------------------------------------------------------------------
#------------MAIN----------------------------------------------------
#--------------------------------------------------------------------

def main(argv):
	graph, vertices, edges = processInputMatrix(argv[0])

	orders = []

	naiveOrder, naiveScore = naive2approx(graph, vertices, edges)
	print(naiveOrder, naiveScore)
	orders.append(naiveOrder)

	greedyDiffOrder, greedyDiffScore = greedyDiff(graph, vertices, edges)
	print(greedyDiffOrder, greedyDiffScore)
	orders.append(greedyDiffOrder)

	greedyRatioOrder, greedyRatioScore = greedyRatio(graph, vertices, edges)
	print(greedyRatioOrder, greedyRatioScore)
	orders.append(greedyRatioOrder)

	createOutput('TEAMNAME.out', orders)
	randomizedInput("test", 100)

#--------------------------------------------------------------------
#------------GREEDY WIN-LOSS DIFFERENCE------------------------------
#--------------------------------------------------------------------
def greedyDiff(graph, vertices, edges):
	order = findIncreasingRank(graph, 0, vertices, operator.sub)
	score = countForward(graph, vertices, order)
	return order, score

def findIncreasingRank(graph, start, end, funct):
	inMinusOut = []
	for i in range(start, end):
		incoming = 0
		outgoing = 0
		for j in range(start, end):
			if graph[i][j] != 0:
				outgoing += 1
			if graph[j][i] != 0:
				incoming += 1
		inMinusOut.append((i, funct(incoming, outgoing)))
	inMinusOut.sort(key=lambda tup: tup[1])
	return [i[0] for i in inMinusOut]


#--------------------------------------------------------------------
#------------GREEDY WIN-LOSS RATIO-----------------------------------
#--------------------------------------------------------------------
def greedyRatio(graph, vertices, edges):
	order = findIncreasingRank(graph, 0, vertices, operator.div)
	score = countForward(graph, vertices, order)
	return order, score

#--------------------------------------------------------------------
#------------NAIVE 2-APPROXIMATION-----------------------------------
#--------------------------------------------------------------------
def naive2approx(graph, vertices, edges):
	order = generateRandomOrder(0, vertices)
	forward = countForward(graph, vertices, order)
	order, forward = flip(order, forward, edges)
	return order, forward

def generateRandomOrder(start, end):
	f = range(start, end)
	random.shuffle(f)
	return f

def countForward(graph, vertices, order):
	counter = 0
	for i in range(vertices):
		node1 = order[i]
		for j in range(i, vertices):
			node2 = order[j]

			if graph[node1][node2] != 0:
				counter += 1

	return counter

def flip(order, forward, edges):
	if forward <= edges / 2:
		return order[::-1], (edges - forward)
	return order, forward

#--------------------------------------------------------------------
#------------FILE MANIPULATION---------------------------------------
#--------------------------------------------------------------------
def createOutput(name, orders):
	fout = open(name, 'w')

	for order in orders:
		for i in order:
			if i == len(order) - 1:
				fout.write(str(i))
			else:
				fout.write(str(i) + ' ')
		fout.write('\n')
	fout.close()

def randomizedInput(name, size):
	random_array = [[0 for x in xrange(size)] for y in xrange(size)]
	edge = [0, 1]
	for i in range(size):
		for j in range(size):
			if i == j:
				random_array[i][j] = 0
			else:
				random_array[i][j] = random.choice(edge)

	fout = open(name, 'w')
	fout.write(str(size)+"\n")
	for i in range(size):
		for j in range(size):
			fout.write(str(random_array[i][j]) + " ")

		fout.write("\n")
	fout.close()

def processInputMatrix(s):
	fin = open(s, "r")
	line = fin.readline().split()
	N = int(line[0])
	edges = 0

	d = [[0 for j in xrange(N)] for i in xrange(N)]
	for i in xrange(N):
		line = fin.readline().split()
		for j in xrange(N):
			d[i][j] = int(line[j])
			if d[i][j] != 0:
				edges += 1
	return d, N, edges

if __name__ == '__main__':
	main(sys.argv[1:])
