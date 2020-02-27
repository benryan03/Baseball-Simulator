baseball_simulator is a Python program that simulates a complete baseball game.

For every pitch, a pseudorandom number from 1-100 is generated.
The number determines the result of the pitch, using the following rules:

1-35: Ball (35%)
36-62: Strike (30%)
67-76: Foul (10%)
77-82: Ground out (6%)
83-87: Fly out (5%)
88-92: Single (5%)
93-96: Double (4%)
97-98: Home run (2%)
99: Hit by pitch (1%)
100: Triple (1%)

When the simulation is complete, the program will output the game stats, and also write them to a .txt file.