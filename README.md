# tsp-mabraham23

This project is an attempt at making a close prediction to the traveling salesman problem using hill-climbing

1. To run the program do the following:
  - edit the hill-climb.py file with the name of the data file and number of seconds that the program should run for ( ex. "barsoom1024" and change signal.alarm(120) for the number of seconds ). By default the alarm will be a couple hundredths of a second over so you may need to subract one second if you want it to be exactly under.
  - run python3 hill-climb.py
  
2. The program will output on the first line, the best utility found and on the remaining lines the space seperated indecies of the cities in the order they should be traversed.
