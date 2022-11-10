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
  
  def __repr__(self):
    return "\n".join(["{}: {}".format(n,neighbors) for n,neighbors in enumerate(self.data)])
  def __str__(self):
    return self.__repr__()   


G = Graph(12, [(1,2), (3,4),(4,3), (1,3)])
G.add_edge((4,5))
G.remove_edge((4,5))
print(G)
print(G.adjacency_matrix)
G.create_adjacency_matrix()

