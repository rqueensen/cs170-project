import sys
import random
import operator
#--------------------------------------------------------------------
#       TO DO:
#               3 Input Files by Wednesday
#               Implement Smart Algorithms
#               Double check what we need to turn in (including student id # stuff)
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
	graph, vertices, edges = processInputMatrix(argv[0])
	
	print cc_finder(graph)
	

def actualRun(s):
	orders = []
	numberOfBest = []
	for i in range(0,5):
		numberOfBest.append(0)

	names = []
	names.append('naive')
	names.append('greedy diff')
	names.append('greedy ratio')
	names.append('topological')
	names.append('topo-greedy')

	for i in range(0, len(s)):
		graph, vertices, edges = processInputMatrix(s[i])

		scores, curOrders = runAllAlgorithms(graph, vertices, edges)

		best = max(scores, key=lambda x:x[1])[0]
		numberOfBest[best] += 1
		bestOrder = curOrders[best][1]
		orders.append(bestOrder)
		bestName = names[best]
		print 'best is: ', bestName

	print '# of naive best: ', numberOfBest[0]
	print '# of greedy diff best: ', numberOfBest[1]
	print '# of greedy ratio best: ', numberOfBest[2]
	print '# of topological sort best: ', numberOfBest[3]
	print '# of topo-greedy best: ', numberOfBest[4]

	createOutput('ParanoidSheep.out', orders)

def randomRun():
	orders = []
	numberOfBest = []
	for i in range(0,5):
		numberOfBest.append(0)

	names = []
	names.append('naive')
	names.append('greedy diff')
	names.append('greedy ratio')
	names.append('topological')
	names.append('topo-greedy')
	
	# vertices = random.randint(1, 100)
	# edgeRatio = random.random()
	vertices = 100
	edgeRatio = 0.5
	repeats = 20

	for i in range(0,repeats):
		graph, edges = randomizedInput(vertices, edgeRatio)

		scores, curOrders = runAllAlgorithms(graph, vertices, edges)

		best = max(scores, key=lambda x:x[1])[0]
		numberOfBest[best] += 1
		bestOrder = curOrders[best][1]
		orders.append(bestOrder)

		bestName = names[best]
		print 'best is: ', bestName

	print '# of naive best: ', numberOfBest[0]
	print '# of greedy diff best: ', numberOfBest[1]
	print '# of greedy ratio best: ', numberOfBest[2]
	print '# of topological sort best: ', numberOfBest[3]
	print '# of topo-greedy best: ', numberOfBest[4]
	print 'vertices: ', vertices, '\nedgeRatio: ', edgeRatio
	createOutput('ParanoidSheep.out', orders)

def runAllAlgorithms(graph, vertices, edges):
	scores = []
	orders = []

	naiveOrder, naiveScore = naive2approx(graph, vertices, edges)
	scores.append((0, naiveScore))
	orders.append((0, naiveOrder))

	greedyDiffOrder, greedyDiffScore = greedyDiff(graph, vertices, edges)
	scores.append((1, greedyDiffScore))
	orders.append((1, greedyDiffOrder))

	greedyRatioOrder, greedyRatioScore = greedyRatio(graph, vertices, edges)
	scores.append((2, greedyRatioScore))
	orders.append((2, greedyRatioOrder))

	topologicalOrder, topologicalScore = topologicalSort(graph, vertices, edges)
	scores.append((3, topologicalScore))
	orders.append((3, topologicalOrder))

	topoGreedyOrder, topoGreedyScore = topologicalRankedSort(graph, vertices, edges)
	scores.append((4, topoGreedyScore))
	orders.append((4, topoGreedyOrder))

	print 'naive', naiveScore
	print 'greedy diff', greedyDiffScore
	print 'greedy ratio', greedyRatioScore
	print 'topological sort', topologicalScore
	print 'topo-greedy sort', topoGreedyScore

	return scores, orders

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
		incomingAll = []
		for i in range(start, end):
			if i not in deleted:
				incoming = 0
				for j in range(start, end):
					if graph[j][i] != 0 and j not in deleted:
						incoming += 1
				incomingAll.append((i, incoming))
		delete = min(incomingAll, key=lambda tup: tup[1])[0]
		deleted.append(delete)
	return deleted

#--------------------------------------------------------------------
#------------TOPO-GREEDY----------------------------------------
#--------------------------------------------------------------------
def topologicalRankedSort(graph, vertices, edges):
	order = findRankLike(graph, 0, vertices)
	score = countForward(graph, vertices, order)
	return order, score

def findRankLike(graph, start, end):
	deleted = []
	for x in range(start, end):
		inMinusOut = []
		for i in range(start, end):
			if i not in deleted:
				incoming = 0
				outgoing = 0
				for j in range(start, end):
					if graph[i][j] != 0 and j not in deleted:
						outgoing += 1
					if graph[j][i] != 0 and j not in deleted:
						incoming += 1
				inMinusOut.append((i, incoming - outgoing))
		delete = min(inMinusOut, key=lambda tup: tup[1])[0]
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
#------------CONNECTED COMPONENTS -----------------------------------
#--------------------------------------------------------------------

def cc_finder(graph):
	#Returns a list of lists of nodes which are connected
	visited = set()
	cc_clumps = []
	
	for node in xrange(len(graph)):
		if not node in visited:
			clump = explore(graph, node)
			visited = visited.union(clump)
			cc_clumps.append(list(clump))
			
	return clump
	
	
def explore(graph, start):
	#Finds the set of nodes reachable from start by going any direction
	q = set(start)
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
	edges = 0
	for i in range(size):
		for j in range(size):
			if i != j and random.random() < trueRatio:
				randomArray[i][j] = 1
				edges += 1
			else:
				randomArray[i][j] = 0
	return randomArray, edges

def randomizedInputFile(name, size):
	randomArray, edges = randomizedInput(size)

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

