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

	orders = []
	best = []
	for i in range(0,4):
		best.append(0)

	# vertices = random.randint(1, 100)
	# edgeRatio = random.random()

	vertices = 100
	edgeRatio = 0.5

	for i in range(0,100):
		scores = []

		graph, edges = randomizedInput(vertices, edgeRatio)

		naiveOrder, naiveScore = naive2approx(graph, vertices, edges)
		scores.append((0, naiveScore))
		print 'naive', naiveScore
		orders.append(naiveOrder)

		greedyDiffOrder, greedyDiffScore = greedyDiff(graph, vertices, edges)
		scores.append((1, greedyDiffScore))
		print 'greedy diff', greedyDiffScore
		orders.append(greedyDiffOrder)

		greedyRatioOrder, greedyRatioScore = greedyRatio(graph, vertices, edges)
		scores.append((2, greedyRatioScore))
		print 'greedy ratio', greedyRatioScore
		orders.append(greedyRatioOrder)

		topologicalOrder, topologicalScore = topologicalSort(graph, vertices, edges)
		scores.append((3, topologicalScore))
		print 'topological sort', topologicalScore
		orders.append(topologicalOrder)

		best[max(scores, key=lambda x:x[1])[0]] += 1

	print '# of naive best: ', best[0]
	print '# of greedy diff best: ', best[1]
	print '# of greedy ratio best: ', best[2]
	print '# of topological sort best: ', best[3]
	print 'vertices: ', vertices, '\nedgeRatio: ', edgeRatio
	createOutput('TEAMNAME.out', orders)

#--------------------------------------------------------------------
#------------TOPOLOGICAL SORT----------------------------------------
#--------------------------------------------------------------------
def topologicalSort(graph, vertices, edges):
	order = findSourceLike(graph, 0, vertices)
	score = countForward(graph, vertices, order)
	return order, score

def findSourceLike(graph, start, end):
	deleted = []
	for x in range(start, end):
		incoming = []
		for i in range(start, end):
			if i not in deleted:
				curIncoming = 0
				for j in range(start, end):
					if graph[j][i] != 0 and j not in deleted:
						curIncoming += 1
				incoming.append((i, curIncoming))
		delete = min(incoming, key=lambda tup: tup[1])[0]
		deleted.append(delete)
	return deleted

#--------------------------------------------------------------------
#------------GREEDY WIN-LOSS DIFFERENCE------------------------------
#--------------------------------------------------------------------
def greedyDiff(graph, vertices, edges):
	order = findIncreasingRankDiff(graph, 0, vertices)
	score = countForward(graph, vertices, order)
	return order, score

def findIncreasingRankDiff(graph, start, end):
	inMinusOut = []
	for i in range(start, end):
		incoming = 0
		outgoing = 0
		for j in range(start, end):
			if graph[i][j] != 0:
				outgoing += 1
			if graph[j][i] != 0:
				incoming += 1
		inMinusOut.append((i, incoming - outgoing))
	inMinusOut.sort(key=lambda tup: tup[1])
	return [i[0] for i in inMinusOut]

#--------------------------------------------------------------------
#------------GREEDY WIN-LOSS RATIO-----------------------------------
#--------------------------------------------------------------------
def greedyRatio(graph, vertices, edges):
	order = findIncreasingRankRatio(graph, 0, vertices)
	score = countForward(graph, vertices, order)
	return order, score

def findIncreasingRankRatio(graph, start, end):
	inMinusOut = []
	for i in range(start, end):
		incoming = 0
		outgoing = 0
		for j in range(start, end):
			if graph[i][j] != 0:
				outgoing += 1
			if graph[j][i] != 0:
				incoming += 1
		if outgoing == 0:
			outgoing = 1
		inMinusOut.append((i, incoming / outgoing))
	inMinusOut.sort(key=lambda tup: tup[1])
	return [i[0] for i in inMinusOut]


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

def randomizedInput(size, trueRatio):
	random_array = [[0 for x in xrange(size)] for y in xrange(size)]
	edges = 0
	for i in range(size):
		for j in range(size):
			if i != j and random.random() < trueRatio:
				random_array[i][j] = 1
				edges += 1
			else:
				random_array[i][j] = 0
	return random_array, edges

def randomizedInputFile(name, size):
	random_array, edges = randomizedInput(size)

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
