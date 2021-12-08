#!/usr/bin/env python3

from __future__ import with_statement
import random
import signal
import math
import sys
import os 
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


def main(argv):

  if len(argv) > 1:
    data_file = argv[1]
  else:
    data_file = "barsoom1024"

  initial_route, dist_table, size = read_data(data_file)

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

if __name__ == "__main__":
  signal.signal(signal.SIGALRM, signal_handler)
  if len(sys.argv) > 1:
    data_file = sys.argv[1]
    data_file = "data/" + data_file + "_name.txt"
    if not os.path.exists(data_file):
      print("{} does not exist.".format(data_file))
      quit()
  
  else:
    print("Please enter a data file.")
    print("Usage: ./hill-climb.py <data_file>")
    quit()

  if len(sys.argv) > 2:
    # check if time is valid
    try:
      time_limit = int(sys.argv[2])
      if time_limit <= 0 or time_limit > 3600:
        raise ValueError
      signal.alarm(time_limit)
    except ValueError:
      print("Invalid time limit:", sys.argv[2] + ".", "Time limit must be an integer between 1 and 3600")
      quit()
  else:
    print("No time limit specified. Defaulting to 120 seconds.")
    print("Usage: ./hill-climb.py <data_file> <time_limit>")
    signal.alarm(120)   
  try:

      main(sys.argv)
  except:
    quit()

