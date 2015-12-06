import sys
import random
import operator
#--------------------------------------------------------------------
#------------MAIN----------------------------------------------------
#--------------------------------------------------------------------

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main(argv):

	naiveIterations = 10

	if argv:
		if len(argv) == 3 and is_int(argv[1]) and is_int(argv[2]):
			
			filenames = []
			for x in range(int(argv[1]), int(argv[2]) + 1):
				filenames.append(argv[0] + '/' + str(x) + '.in')

			actualRun(filenames, naiveIterations)
		else:
			actualRun(argv, naiveIterations)
	else:
		randomRun(naiveIterations)

names = []
names.append('naive')
names.append('greedy diff')
names.append('greedy ratio')
names.append('topological')
names.append('topo-greedy')
names.append('local-max')

orders = []
numberOfBest = [0, 0, 0, 0, 0, 0]

def setup():
	orders = []
	numberOfBest = [0, 0, 0, 0, 0, 0]

def actualRun(s, naiveIterations):
	setup()	

	for i in range(0, len(s)):
		graph, num_vertices, num_edges = processInputMatrix(s[i])

		vertices = range(num_vertices)
		scores, curOrders = runAllAlgorithms(graph, num_vertices, num_edges, vertices, False, naiveIterations)

		best = max(scores, key=lambda x:x[1])[0]
		numberOfBest[best] += 1
		bestOrder = curOrders[best][1]
		orders.append(bestOrder)
		bestName = names[best]
		print 'best is: ', bestName

	printBest(numberOfBest)

	createOutput('ParanoidSheep.out', orders)


def randomRun(naiveIterations):
	setup()
	
	# num_vertices = random.randint(1, 100)
	# edgeRatio = random.random()
	num_vertices = 100
	edgeRatio = 0.5
	repeats = 20

	for i in range(0,repeats):
		graph, num_edges = randomizedInput(num_vertices, edgeRatio)

		vertices = range(num_vertices)
		scores, curOrders = runAllAlgorithms(graph, num_vertices, num_edges, vertices, False, naiveIterations)

		best = max(scores, key=lambda x:x[1])[0]
		numberOfBest[best] += 1
		bestOrder = curOrders[best][1]
		orders.append(bestOrder)
		bestName = names[best]
		print 'best is: ', bestName

	printBest(numberOfBest)
	print 'num_vertices: ', num_vertices, '\nedgeRatio: ', edgeRatio
	createOutput('ParanoidSheep.out', orders)

def printBest(numberOfBest):
	print '# of naive best: ', numberOfBest[0]
	print '# of greedy diff best: ', numberOfBest[1]
	print '# of greedy ratio best: ', numberOfBest[2]
	print '# of topological sort best: ', numberOfBest[3]
	print '# of topo-greedy best: ', numberOfBest[4]
	print '# of local-max best: ', numberOfBest[5]

def runAllAlgorithms(graph, num_vertices, num_edges, vertices, in_cc, naiveIterations):
	scores = []
	orders = []

	if not in_cc:
		forwardScores = {}

	naiveOrder, naiveScore = naive2approx(graph, num_vertices, num_edges, vertices, naiveIterations)
	scores.append((0, naiveScore))
	orders.append((0, naiveOrder))

	greedyDiffOrder, greedyDiffScore = greedyDiff(graph, num_vertices, num_edges, vertices)
	scores.append((1, greedyDiffScore))
	orders.append((1, greedyDiffOrder))

	greedyRatioOrder, greedyRatioScore = greedyRatio(graph, num_vertices, num_edges, vertices)
	scores.append((2, greedyRatioScore))
	orders.append((2, greedyRatioOrder))

	topologicalOrder, topologicalScore = topologicalSort(graph, num_vertices, num_edges, vertices)
	scores.append((3, topologicalScore))
	orders.append((3, topologicalOrder))

	topoGreedyOrder, topoGreedyScore = topologicalRankedSort(graph, num_vertices, num_edges, vertices)
	scores.append((4, topoGreedyScore))
	orders.append((4, topoGreedyOrder))

	topoGreedyOrder, topoGreedyScore = topologicalRankedSort(graph, num_vertices, num_edges, vertices)
	scores.append((4, topoGreedyScore))
	orders.append((4, topoGreedyOrder))

	localMaxOrder, localMaxScore = permLocalMax(graph, num_vertices, num_edges, vertices, naiveOrder, naiveScore)
	scores.append((5, localMaxScore))
	orders.append((5, localMaxOrder))

	print 'naive', naiveScore
	print 'greedy diff', greedyDiffScore
	print 'greedy ratio', greedyRatioScore
	print 'topological sort', topologicalScore
	print 'topo-greedy sort', topoGreedyScore
	print 'local-max', localMaxScore	

	return scores, orders

#--------------------------------------------------------------------
#------------PERMUTATIONS-LOCAL-MAX----------------------------------
#--------------------------------------------------------------------
def permLocalMax(graph, num_vertices, num_edges, vertices, startingOrder, startingForward):
	localMaxOrder = findLocalMax(graph, num_vertices, startingOrder, startingForward)
	localMaxForward = countForward(graph, num_vertices, localMaxOrder)

	return localMaxOrder, localMaxForward

def findLocalMax(graph, num_vertices, order, forward):
	maxForward = forward
	maxOrder = order

	for i in range(num_vertices - 1):
		j = i + 1
		order[i], order[j] = order[j], order[i]
		curForward = countForward(graph, num_vertices, order)

		if curForward > maxForward:
			maxForward = curForward
			maxOrder = list(order)

		order[i], order[j] = order[j], order[i]

	if maxForward == forward:
		return order
	else:
		return findLocalMax(graph, num_vertices, maxOrder, maxForward)

#--------------------------------------------------------------------
#------------TOPO-GREEDY--------------------------------------------
#--------------------------------------------------------------------
def topologicalRankedSort(graph, num_vertices, num_edges, vertices):
	order = findRankLike(graph, vertices)
	score = countForward(graph, num_vertices, order)
	return order, score

def findRankLike(graph, vertices):
	deleted = []
	for x in vertices:
		inMinusOut = []
		for i in vertices:
			if i not in deleted:
				incoming = 0
				outgoing = 0
				for j in vertices:
					if graph[i][j] != 0 and j not in deleted:
						outgoing += 1
					if graph[j][i] != 0 and j not in deleted:
						incoming += 1
				inMinusOut.append((i, incoming - outgoing))
		delete = min(inMinusOut, key=lambda tup: tup[1])[0]
		deleted.append(delete)
	return deleted

#--------------------------------------------------------------------
#------------TOPOLOGICAL SORT----------------------------------------
#--------------------------------------------------------------------
def topologicalSort(graph, num_vertices, num_edges, vertices):
	order = findSourceLike(graph, vertices)
	score = countForward(graph, num_vertices, order)
	return order, score

def findSourceLike(graph, vertices):
	deleted = []
	for x in vertices:
		incomingAll = []
		for i in vertices:
			if i not in deleted:
				incoming = 0
				for j in vertices:
					if graph[j][i] != 0 and j not in deleted:
						incoming += 1
				incomingAll.append((i, incoming))
		delete = min(incomingAll, key=lambda tup: tup[1])[0]
		deleted.append(delete)
	return deleted


#--------------------------------------------------------------------
#------------GREEDY WIN-LOSS RATIO-----------------------------------
#--------------------------------------------------------------------
def greedyRatio(graph, num_vertices, num_edges, vertices):
	order = findIncreasingRankRatio(graph, vertices)
	score = countForward(graph, num_vertices, order)
	return order, score

def findIncreasingRankRatio(graph, vertices):
	inMinusOut = []
	for i in vertices:
		incoming = 0
		outgoing = 0
		for j in vertices:
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
#------------GREEDY WIN-LOSS DIFFERENCE------------------------------
#--------------------------------------------------------------------
def greedyDiff(graph, num_vertices, num_edges, vertices):
	order = findIncreasingRankDiff(graph, vertices)
	score = countForward(graph, num_vertices, order)
	return order, score

def findIncreasingRankDiff(graph, vertices):
	inMinusOut = []
	for i in vertices:
		incoming = 0
		outgoing = 0
		for j in vertices:
			if graph[i][j] != 0:
				outgoing += 1
			if graph[j][i] != 0:
				incoming += 1
		inMinusOut.append((i, incoming - outgoing))
	inMinusOut.sort(key=lambda tup: tup[1])
	return [i[0] for i in inMinusOut]

#--------------------------------------------------------------------
#------------NAIVE 2-APPROXIMATION-----------------------------------
#--------------------------------------------------------------------
def naive2approx(graph, num_vertices, num_edges, vertices, numIterations):
	maxOrder = None
	maxForward = 0
	for i in range(numIterations):
		order = generateRandomOrder(vertices)
		forward = countForward(graph, num_vertices, order)
		order, forward = flip(order, forward, num_edges)
		if forward > maxForward:
			maxForward = forward
			maxOrder = order

	return maxOrder, maxForward

def flip(order, forward, num_edges):
	if forward <= num_edges / 2:
		return order[::-1], (num_edges - forward)
	return order, forward

def generateRandomOrder(vertices):
	random.shuffle(vertices)
	return vertices

forwardScores = {}

def countForward(graph, num_vertices, order):
	score = hasScore(order)
	if score:
		return score

	counter = 0
	for i in range(num_vertices):
		node1 = order[i]
		for j in range(i, num_vertices):
			node2 = order[j]

			if graph[node1][node2] != 0:
				counter += 1

	forwardScores[str(order)] = counter 

	return counter

def hasScore(order):
    try:
        x = forwardScores[str(order)]
        return x
    except KeyError:
        return None

#--------------------------------------------------------------------
#------------FILE MANIPULATION---------------------------------------
#--------------------------------------------------------------------
def createOutput(name, orders):
	fout = open(name, 'w')

	for order in orders:
		for i in order:
			fout.write(str(i + 1) + ' ')
		fout.write('\n')
	fout.close()

def randomizedInput(size, trueRatio):
	randomArray = [[0 for x in range(size)] for y in range(size)]
	num_edges = 0
	for i in range(size):
		for j in range(size):
			if i != j and random.random() < trueRatio:
				randomArray[i][j] = 1
				num_edges += 1
			else:
				randomArray[i][j] = 0
	return randomArray, num_edges

def randomizedInputFile(name, size):
	randomArray, num_edges = randomizedInput(size)

	fout = open(name, 'w')
	fout.write(str(size)+"\n")
	for i in range(size):
		for j in range(size):
			fout.write(str(randomArray[i][j]) + " ")

		fout.write("\n")
	fout.close()

def processInputMatrix(s):
	fin = open(s, "r")
	line = fin.readline().split()
	N = int(line[0])
	num_edges = 0

	d = [[0 for j in range(N)] for i in range(N)]
	for i in range(N):
		line = fin.readline().split()
		for j in range(N):
			d[i][j] = int(line[j])
			if d[i][j] != 0:
				num_edges += 1
	return d, N, num_edges

if __name__ == '__main__':
	main(sys.argv[1:])

