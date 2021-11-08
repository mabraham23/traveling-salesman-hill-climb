from __future__ import with_statement
import random
import signal
import math
import signal, time
from contextlib import contextmanager

global best_util_so_far
global best_route_so_far
global random_restarts 

# return a list of routes that are the neighbors of the route passed in
def neighbors(route):
  # scale randomness with size of the cities
  rand_i = random.randint(0,len(route)-1)
  rand_j = random.randint(0,len(route)-1)

  new_route = route.copy()

  first = new_route[rand_i]
  new_route[rand_i] = new_route[rand_j]
  new_route[rand_j] = first

  return new_route  

# returns an entire route that has been hill climbned 
def hill_climbing(calc_total_dist, initial_route, dist_table, size):
  route = initial_route
  u = math.inf 
  improved = True
  swaps = 0
  swap_thresh = size * 100
  while improved:
    improved = False
    if swaps <= swap_thresh:
      improved = True
    n = neighbors(route)
    swaps += 1
    c = calc_total_dist(n, dist_table)
    if c < u:
      u = c
      route = n
      improved = True
  return route, u

# calculates the sum of the distances for all cities in a given route
def calc_total_dist(route, dist_table):
  total_dist = 0
  last_i = len(route)-1
  for i in range(len(route)-1):
    total_dist += dist_table[route[i]][route[i+1]]
  total_dist += dist_table[route[last_i]][route[0]]
  return total_dist

# process data from raw data files
def read_data(file):
  cities = []
  distances = []
  size = 0
  with open('./data/' + file + '_name.txt', 'r') as f:
    lines = f.readlines()
    i = 0
    for line in lines:
      if line[0] != "#":
        cities.append(i)
        distances.append([])
        i += 1 
        size += 1

  with open('./data/' + file + '_dist.txt', 'r') as f:
    raw_lines = f.readlines()
    lines = []
    for line in raw_lines:
      if line[0] != "#":
        lines.append(line)
    for i in range(len(lines)):
      words = lines[i].split()
      for j in range(len(words)):
        distances[i].append(int(words[j]))

  return cities, distances, size


def main():

  initial_route, dist_table, size = read_data("barsoom1024")

  global best_util_so_far
  global best_route_so_far 
  global random_restarts 
  best_util_so_far = math.inf
  best_route_so_far = []
  random_restarts = 0

  while True:
    random_restarts += 1
    random.shuffle(initial_route)
    route, u = hill_climbing(calc_total_dist, initial_route, dist_table, size)
    if u < best_util_so_far:
      # print(u)
      best_util_so_far = u
      best_route_so_far = route


def signal_handler(signum, frame):
  # print("random restarts:", random_restarts)
  print(best_util_so_far)
  print(*best_route_so_far, sep=' ')
  quit()

signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(120)   
try:
    main()
except:
  quit()

