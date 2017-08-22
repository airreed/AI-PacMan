# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from util import Queue
from util import PriorityQueue
from game import Directions
class Node:
  def __init__(self, state, action, cost, parent, heuristicCost=0):
    self.state = state
    self.action = action
    self.cost = cost
    self.parent = parent
    self.heuristicCost = heuristicCost

  def __cmp__(self, other): 
    return cmp(self.cost, other.cost)

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  
  if problem.isGoalState(problem.getStartState()):
    return [Directions.STOP]
  result = []
  dfshelper(problem, problem.getStartState(), result)
  return result
  
def dfshelper(problem, currentState, result):
  # already add to visited list in getSuccessors
  if problem.isGoalState(currentState):
    return True
  children = problem.getSuccessors(currentState)
  # print "CurrentState:", currentState, "Current successors:", children
  if children == []:
    return False
  for (nextState, action, cost) in children:
    if nextState not in problem._visited:
      if dfshelper(problem, nextState, result):
        result.insert(0, action)
        # print "Result:", result
        return True
  return False

    

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  visited = {}
  startState = problem.getStartState()
  if problem.isGoalState(startState):
    return [Directions.STOP]
  root = Node(startState, None, 0, None)
  queue = Queue()
  queue.push(root)
  visited[root.state] = True
  while not queue.isEmpty():
    currentStateNode = queue.pop()
    if problem.isGoalState(currentStateNode.state):
      return goalRoute(currentStateNode)
    children = problem.getSuccessors(currentStateNode.state)
    for (nextState, action, cost) in children:
      node = Node(nextState, action, cost, currentStateNode)
      if nextState not in visited: 
        # print 'Add ', nextState, ' to queue'
        visited[nextState] = True
        queue.push(node)
  print 'Found nothing'
  return [Directions.STOP] 

def goalRoute(currentStateNode):
  result = []
  while currentStateNode.parent is not None:
    result.insert(0, currentStateNode.action)
    currentStateNode = currentStateNode.parent
  print result
  return result

      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  visited = {}
  startState = problem.getStartState()
  if problem.isGoalState(startState):
    return [Directions.STOP]
  root = Node(startState, None, 0, None)
  queue = PriorityQueue()
  queue.push(root, root.cost)
  visited[root.state] = True
  while not queue.isEmpty():
    currentStateNode = queue.pop()
    if currentStateNode.state not in visited:
      visited[currentStateNode.state] = True
    if problem.isGoalState(currentStateNode.state):
      return goalRoute(currentStateNode)
    children = problem.getSuccessors(currentStateNode.state)
    for (nextState, action, cost) in children:
      node = Node(nextState, action, cost + currentStateNode.cost, currentStateNode)
      if nextState not in visited: 
        visited[nextState] = True
        queue.push(node, node.cost)
  return [Directions.STOP]


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  visited = {}
  startState = problem.getStartState()
  if problem.isGoalState(startState):
    return [Directions.STOP]
  root = Node(startState, None, 0, None, heuristic(startState, problem))
  queue = PriorityQueue()
  queue.push(root, root.cost + root.heuristicCost)
  visited[root.state] = True
  while not queue.isEmpty():
    currentStateNode = queue.pop()
    if problem.isGoalState(currentStateNode.state):
      return goalRoute(currentStateNode)
    children = problem.getSuccessors(currentStateNode.state)
    for (nextState, action, cost) in children:
      node = Node(nextState, action, cost + currentStateNode.cost, currentStateNode, heuristic(nextState, problem))
      if nextState not in visited: 
        queue.push(node, node.cost + node.heuristicCost)
        visited[node.state] = True
  return [Directions.STOP]
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
