import sys
import math as m

class Node():
    def __init__(self, idx):
        self.links = [] #list of connected Node
        self.reach = False
        self.distBob = m.inf
        self.relativeDist = m.inf
        self.idx = idx
        self.gtw = False
        self.gtwlink = 0
    
    def __lt__(self, other):
    #use for sorting
        if self.relativeDist < other.relativeDist:
            return True
        elif self.relativeDist > other.relativeDist:
            return False
        else:
            if self.distBob < other.distBob:
                return True
            elif self.distBob > other.distBob:
                return False
            else:
                return self.gtwlink >= other.gtwlink

    
    def __str__(self):
        return f'N{self.idx},rd {self.relativeDist}, d {self.distBob}, gtwlink {self.gtwlink}'

class Graph():
    def __init__(self):
        self.nodes = {}
        self.gtw = []
    
    def reset(self):
        #reset graph
        for node in self.nodes.values():
            node.reach = False #reinit graph search
            node.relativeDist = m.inf
            node.distBob = m.inf
            node.gtwlink = 0
    
    def calculate_Dist(self, si, stopGtwFound=False):
        #parse all node and save the distance to bob for each of them
        
        #create set of unvisited nodes
        UnvisitedNodes = list(self.nodes.values())
        
        #set initial node
        current_node = UnvisitedNodes[si]
        current_node.relativeDist = 0
        current_node.distBob = 0
        
        while UnvisitedNodes:
            #select closest unvisited Node
            current_node = min(UnvisitedNodes, key= lambda n: n.distBob)
            #stop if nodes are not connected
            if current_node.distBob == m.inf:
                print(f"Stop because no Nodes from UnvisitedNodes are connected", file=sys.stderr, flush=True)
                break
            
            current_node.reach = True
            UnvisitedNodes.remove(current_node)
            #print(f"Selecting Node:{current_node.idx}, dist={current_node.distBob}, rdist={current_node.relativeDist}", file=sys.stderr, flush=True)
            
            #update all connected nodes
            for child_node in current_node.links:
                #skip Node already visited
                if child_node.reach:
                    continue
                    
                #evaluate Dist from this Node
                dist = current_node.distBob + 1
                if dist < child_node.distBob:
                    child_node.distBob = dist #update distBob if shortest than saved
                    
                rdist = current_node.relativeDist + 1 - child_node.gtwlink
                if rdist < child_node.relativeDist:
                    child_node.relativeDist = rdist #update relativeDist 
                
            #check if all gateway have been visited
            if all([n.reach for n in self.gtw]) and stopGtwFound:
                print(f"Stop because have gateway have been visited", file=sys.stderr, flush=True)
                break
            

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]

graph = Graph()
graph.nodes = {i:Node(i) for i in range(n)}

for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    graph.nodes[n1].links.append(graph.nodes[n2])
    graph.nodes[n2].links.append(graph.nodes[n1])

for i in range(e):
    ei = int(input())  # the index of a gateway node
    graph.nodes[ei].gtw = True
    graph.gtw.append(graph.nodes[ei])

#for node in graph.nodes.values():
#    print((node.idx, node.gtw, node.links), file=sys.stderr, flush=True)

# game loop
while True:
    si = int(input())  # The index of the node on which the Bobnet agent is positioned this turn

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    #reset graph
    graph.reset()
    
    #count connected gtw
    for gtw in graph.gtw:
        for n in gtw.links:
            n.gtwlink += 1
    
    #update all Node to save distance from Bob
    graph.calculate_Dist(si=si)
    
    #sort gateway by relative distance then distance from Bob
    graph.gtw.sort()
    gtw = graph.gtw[0]
    for n in graph.gtw:
        print(n, file=sys.stderr, flush=True)

    gtw.links.sort()
    node = gtw.links[0]
    for n in gtw.links:
        print(n, file=sys.stderr, flush=True)
                
    #pop best link
    print(f"{gtw.idx} {node.idx}") 
    
    #delete link from graph (both way)
    gtw.links.remove(node)
    node.links.remove(gtw)
