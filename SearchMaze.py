import math

class Graph:

    def __init__(self,start,end,black,amount):
        self.black = black
        self.dim = int(amount)
        self.nodes = [start,end]
        self.beg = start
        self.fin = end
        self.nei = dict()
        self.construct()

    def construct(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) not in self.black:
                    source = (i,j)
                    if source not in self.nodes:
                        self.nodes.append(source)
                    self.nei[source] = []
                    q = [-1,0,1]
                    for w in range(3):
                        for z in range(3):
                            if (w != 1 or z != 1) and self.dim > i+q[w] >= 0 and self.dim > j+q[z] >= 0:
                                if (i+q[w],j+q[z]) not in self.black:
                                    x = (i+q[w],j+q[z])
                                    if x not in self.nodes:
                                        self.nodes.append(x)
                                    self.nei[source].append(x)


    def ASTAR(self):
        calcH = lambda p: math.sqrt((self.fin[0]-p[0])**2+(self.fin[1]-p[1])**2)
        distance = lambda p1,p2: math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
        g_cost = dict()
        parent = dict()
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) in self.nodes:
                    g_cost[(i,j)] = float("Inf")
                    parent[(i,j)] = None
        g_cost[self.beg] = 0
        open = set()
        closed = set()
        open.add(self.beg)
        while len(open):
            minf = float("Inf")
            current = None
            for x in open:
                if g_cost[x] + calcH(x) < minf:
                    minf = g_cost[x] + calcH(x)
                    current = x
            if current == self.fin:
                path = []
                p = parent[current]
                while p != self.beg:
                    path.append(p)
                    p = parent[p]
                return list(reversed(path))
            open.remove(current)
            closed.add(current)
            for p in self.nei[current]:
                if p not in closed:
                    if g_cost[current] + distance(current,p) < g_cost[p]:
                        g_cost[p] = g_cost[current] + distance(current,p)
                        parent[p] = current
                        if p not in open:
                            open.add(p)
        return None # not reachable



