import sys
import random
import operator
import copy
import itertools

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
			for x in xrange(int(argv[1]), int(argv[2]) + 1):
				filenames.append(argv[0] + '/' + str(x) + '.in')

			actualRun(filenames, naiveIterations)
		else:
			actualRun(argv, naiveIterations)
	else:
		randomRun(naiveIterations)

names = ['naive', 'greedy diff', 'greedy ratio', 'topological', 'topo-greedy', 'topo-greedy-ratio', 'local-max', 'cc/brute']
orders = []
numberOfBest = [0 for x in xrange(len(names))]

def printBest(numberOfBest):
	for x in range(len(numberOfBest)):
		print '# of ' + str(names[x]) + ', ' + str(numberOfBest[x])

def actualRun(s, naiveIterations):
	for i in xrange(len(s)):
		graph, num_vertices, num_edges = processInputMatrix(s[i])

		vertices = range(num_vertices)
		scores, curOrders = runAllAlgorithms(graph, num_vertices, num_edges, vertices, False, naiveIterations)

		best = max(scores, key=lambda x:x[1])[0]
		numberOfBest[best] += 1
		bestOrder = curOrders[best][1]
		orders.append(bestOrder)
		bestName = names[best]
		print 'best is: ', bestName, '\n'

	printBest(numberOfBest)

	createOutput('ParanoidSheep.out', orders)


def randomRun(naiveIterations):	
	# num_vertices = random.randint(1, 100)
	# edgeRatio = random.random()
	num_vertices = 100
	edgeRatio = 0.5
	repeats = 10

	for i in xrange(repeats):
		graph, num_edges = randomizedInput(num_vertices, edgeRatio)

		vertices = range(num_vertices)
		scores, curOrders = runAllAlgorithms(graph, num_vertices, num_edges, vertices, False, naiveIterations)

		best = max(scores, key=lambda x:x[1])[0]
		numberOfBest[best] += 1
		bestOrder = curOrders[best][1]
		orders.append(bestOrder)
		bestName = names[best]
		print 'best is: ', bestName, '\n'

	printBest(numberOfBest)
	print 'num_vertices: ', num_vertices, '\nedgeRatio: ', edgeRatio
	createOutput('ParanoidSheep.out', orders)

def runAllAlgorithms(graph, num_vertices, num_edges, vertices, in_cc, naiveIterations):
	scores = []
	orders = []

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

	topoGreedyRatioOrder, topoGreedyRatioScore = topologicalRankedRatioSort(graph, num_vertices, num_edges, vertices)
	scores.append((5, topoGreedyRatioScore))
	orders.append((5, topoGreedyRatioOrder))

	localMaxOrder, localMaxScore = permLocalMax(graph, num_vertices, num_edges, vertices, naiveOrder, naiveScore)
	scores.append((6, localMaxScore))
	orders.append((6, localMaxOrder))
	
	if not in_cc:
		forwardScores = {}

		ccOrder, ccScore = cc_order(graph, num_vertices, num_edges, naiveIterations)
		scores.append((7, ccScore))
		orders.append((7, ccOrder))

		for x in xrange(len(scores)):
			print '' + str(names[x]) + ': ' + str(scores[x][1])

		# print 'naive', naiveScore
		# print 'greedy diff', greedyDiffScore
		# print 'greedy ratio', greedyRatioScore
		# print 'topological sort', topologicalScore
		# print 'topo-greedy sort', topoGreedyScore
		# print 'topo-greedy-ratio sort', topoGreedyRatioScore
		# print 'local-max', localMaxScore
		# print 'cc/brute', ccScore
	else:
		scores.append((7, 0))
		orders.append((7, None))

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
	maxOrder = copy.copy(order)

	for i in xrange(num_vertices):
		j = random.randint(0, num_vertices - 1)
		curOrder = copy.copy(order)
		curOrder[i], curOrder[j] = curOrder[j], curOrder[i]
		curForward = countForward(graph, num_vertices, curOrder)

		if curForward > maxForward:
			maxForward = curForward
			maxOrder = curOrder

	if maxForward == forward:
		return maxOrder
	else:
		return findLocalMax(graph, num_vertices, maxOrder, maxForward)

#--------------------------------------------------------------------
#------------TOPO-GREEDY-RATIO---------------------------------------
#--------------------------------------------------------------------
def topologicalRankedRatioSort(graph, num_vertices, num_edges, vertices):
	order = findRankLike(graph, vertices)
	score = countForward(graph, num_vertices, order)
	return order, score

def findRankRatioLike(graph, vertices):
	deleted = []
	for x in vertices:
		inOutRatio = []
		for i in vertices:
			if i not in deleted:
				incoming = 0
				outgoing = 0
				for j in vertices:
					if graph[i][j] != 0 and j not in deleted:
						outgoing += 1
					if graph[j][i] != 0 and j not in deleted:
						incoming += 1
				if outgoing == 0:
					outgoing = 1
				inOutRatio.append((i, incoming / outgoing))
		delete = min(inOutRatio, key=lambda tup: tup[1])[0]
		deleted.append(delete)
	return deleted

#--------------------------------------------------------------------
#------------TOPO-GREEDY---------------------------------------------
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
	inOutRatio = []
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
		inOutRatio.append((i, incoming / outgoing))
	inOutRatio.sort(key=lambda tup: tup[1])
	return [i[0] for i in inOutRatio]

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
	for i in xrange(numIterations):
		order = generateRandomOrder(vertices)
		forward = countForward(graph, num_vertices, order)
		order, forward = flip(order, forward, num_edges)
		if forward > maxForward:
			maxForward = forward
			maxOrder = copy.copy(order)

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
	for i in xrange(num_vertices):
		node1 = order[i]
		for j in xrange(i, num_vertices):
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
#------------CONNECTED COMPONENTS -----------------------------------
#--------------------------------------------------------------------

def cc_order(graph, num_vertices, num_edges, naiveIterations):
	clumps = cc_finder(graph)
	final = []
	for clump in clumps:
		if len(clump) < 9:
			final += bruteForce(graph, len(clump), clump)[1]
		else:
			scores, curOrders = runAllAlgorithms(graph, len(clump), num_edges, clump, True, naiveIterations)
			best = max(scores, key=lambda x:x[1])[0]
			bestOrder = curOrders[best][1]
			final += bestOrder
			
	return final, countForward(graph, num_vertices, final)
	
def cc_finder(graph):
	#Returns a list of lists of nodes which are connected
	visited = set()
	cc_clumps = []
	
	for node in xrange(len(graph)):
		if not node in visited:
			clump = explore(graph, node)
			visited = visited.union(clump)
			cc_clumps.append(list(clump))
			
	return cc_clumps
	
	
def explore(graph, start):
	#Finds the set of nodes reachable from start by going any direction
	q = set()
	q.add(start)
	visited = set()
	while len(q) != 0:
		n = q.pop()
		if not n in visited:
			visited.add(n)
			for i in xrange(len(graph)):
				if graph[n][i] == 1 or graph[i][n] == 1:
					q.add(i)
	
	return visited
	
#--------------------------------------------------------------------
#------------Brute Force --------------------------------------------
#--------------------------------------------------------------------
def bruteForce(graph, num_vertices, vertices):
	permutations = []
	for i in itertools.permutations(vertices):
		permutations.append(list(i))
		
	best_score = 0
	best_order = []
	for perm in permutations:
		rand_score = countForward(graph, num_vertices, perm)
		if rand_score > best_score:
			best_score = rand_score
			best_order = perm
			
	return best_score, best_order
	
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
	randomArray = [[0 for x in xrange(size)] for y in xrange(size)]
	num_edges = 0
	for i in xrange(size):
		for j in xrange(size):
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
	for i in xrange(size):
		for j in xrange(size):
			fout.write(str(randomArray[i][j]) + " ")

		fout.write("\n")
	fout.close()

def processInputMatrix(s):
	fin = open(s, "r")
	line = fin.readline().split()
	N = int(line[0])
	num_edges = 0

	d = [[0 for j in xrange(N)] for i in xrange(N)]
	for i in xrange(N):
		line = fin.readline().split()
		for j in xrange(N):
			d[i][j] = int(line[j])
			if d[i][j] != 0:
				num_edges += 1
	return d, N, num_edges

if __name__ == '__main__':
	main(sys.argv[1:])

