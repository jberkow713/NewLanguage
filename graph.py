import random
import copy

def create_matrix(dim):    
  final = []
  for x in range(dim):
    final.append([random.randint(0,1) for x in range(dim)])
  return final

def on_graph(matrix,coord):
  if coord[0]>=0 and coord[0]<=len(matrix)-1:
    if coord[1]>=0 and coord[1]<=len(matrix)-1:
      return matrix[coord[0]][coord[1]]
  return False

def find_islands(matrix):
  
  M2 = copy.deepcopy(matrix)
  count = 0
  for x in matrix:
    inner_count = 0    
    for y in x:
      if y ==1:
        C,I = count, inner_count      
        positions = [(C-1,I), (C+1,I), (C,I+1), (C,I-1)]
        island=True
        for X in positions:
          if on_graph(matrix,X) ==1:
            island=False
            break
        if island==True:
            M2[C][I]='-'            
      inner_count +=1
    count+=1        
  
  return M2

class Graph:
  def __init__(self, num_nodes, edges):
    self.num_nodes = num_nodes
    self.edges = edges
    self.data = self.create_edges()
    self.adjacency_matrix = self.create_adjacency_matrix()

  def create_edges(self):
    Data = [[] for _ in range(self.num_nodes)]    
    for n1,n2 in self.edges:
      if n2 not in Data[n1]:
        Data[n1].append(n2)
      if n1 not in Data[n2]:
        Data[n2].append(n1)
    return Data    

  def create_adjacency_matrix(self):
    adj_list = [[0] * self.num_nodes for _ in range(self.num_nodes)]       
    for i in range(self.num_nodes):
      d = self.data[i]     
      for x in d:
        adj_list[i][x]=1   
    return adj_list

  def add_edge(self, edge):
    i,j = edge   
    if i not in self.data[j]:
      self.data[j].append(i)
    if j not in self.data[i]:
      self.data[i].append(j)  
  
  def remove_edge(self, edge):
    i,j = edge
    if i in self.data[j]:
      self.data[j].remove(i)
    if j in self.data[i]:
      self.data[i].remove(j)
  
  def bfs(self, root):
    queue  = []
    # Tracks if connected edge has been discovered in graph
    discovered = [False] * len(self.data)
    discovered[root]=True
    # distance tracks distance from root to specific nodes
    distance = [None] *len(self.data)    
    distance[root]=0

    parent = [None]*len(self.data)

    queue.append(root)
    idx = 0
    while idx <len(queue):
      current = queue[idx]
      idx+=1
      for edge in self.data[current]:
        if discovered[edge]==False:
          discovered[edge]=True
          queue.append(edge)

          parent[edge] = current
          distance[edge] = 1+distance[current]
    return queue, distance, parent
  def dfs(self,root):
    stack = []
    discovered = [False] *len(self.data)
    result = []
    parent = [None]*len(self.data)

    stack.append(root)
    while len(stack)>0:
      current = stack.pop()
      discovered[current]=True
      result.append(current)
      for neighbor in self.data[current]:
        if parent[neighbor]==None:
          parent[neighbor]=current
        if discovered[neighbor]==False:
          stack.append(neighbor)

    return result, parent  

    pass
  def __repr__(self):
    return "\n".join(["{}: {}".format(n,neighbors) for n,neighbors in enumerate(self.data)])
  def __str__(self):
    return self.__repr__()   


# G = Graph(12, [(1,2), (3,4),(4,3), (1,3),(10,11), (4,11)])
# G.add_edge((4,5))
# G.remove_edge((4,5))
# print(G)
# print(G.adjacency_matrix)
# G.create_adjacency_matrix()
# print(G.bfs(3))
# print(G.dfs(3))


class D_Graph:
  def __init__(self, num_nodes, edges, direction=False, weighted=False):
    self.num_nodes = num_nodes 
    self.edges = edges
    self.direction = direction
    self.weighted = weighted
    self.data = self.create_edges()[0]
    self.weights = self.create_edges()[1]
  
  def create_edges(self):
    # Creating weights/connections given weighted,direction parameters, and edges
    Data = [[] for _ in range(self.num_nodes)] 
    if self.weighted ==True:
      weights = [[] for _ in range(self.num_nodes)]              

      for n1,n2,weight in self.edges:
        if n2 not in Data[n1]:
          Data[n1].append(n2)
          weights[n1].append(weight)
        if self.direction==False:
          if n1 not in Data[n2]:
            Data[n2].append(n1)
            weights[n2].append(weight)     

    elif self.weighted==False:
      weights = None
      for n1,n2 in self.edges:
        if n2 not in Data[n1]:
          Data[n1].append(n2)
        if self.direction ==False:
          if n1 not in Data[n2]:
            Data[n2].append(n1)

    return Data, weights   

D  = D_Graph(12, [(1,2,5), (3,4,6),(4,3,6), (1,3,5),(10,11,8), (4,11,2)], False, True)
print(D.data, D.weights)

