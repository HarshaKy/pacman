# Automated Agent Evaluation of Generated Pac-Man Levels

I verify that I am the sole author of the following programmes:

1. RLAgents.py
2. features.py
3. QLearningAgents.py
4. ConerSeekingAgents.py
5. search.py
6. MDPAgents.py
7. script.py
8. analysis.ipynb

The remainder of the project was created by a team of developers from UC Berkeley. The map generation algorithm was 
also built by someone else. I do not claim ownership of their work. They have also been credited appropriately in the files
and in the report.

## Folder structure

```
📦 pacman
├─ layouts
│  ├─ gen
│  │  ├─ corners
│  │  │  ├─ 1.lay
│  │  │  │  ├─ 3.lay
│  │  │  └─ ...
│  │  └─ classic
│  │     ├─ 1.lay
│  │     ├─ 2.lay
│  │     ├─ 3.lay
│  │     └─ ...
│  └─ human
│     ├─ originalClassic.lay
│     ├─ mediumClassic.lay
│     ├─ smallGrid.lay
│     └─ ...
├─ map_generation
├─ test_cases
├─ cornerSeekingAgents.py
├─ search.py
├─ RLAgents.py
├─ QLearningAgents.py
├─ MDPAgents.py
├─ features.py
└─ ...
```

To run the game:
```
python pacman.py
```

To run the Corner Seeking Agent:
```
python pacman.py -p CornerSeekingAgent -n 20 -q -l gen/corners/3
```

To run the RL Agent:
```
python pacman.py -p QLearningAgent -x 50 -q -n 60 -l gen/classic/4 
```

To run the MDP Agent:
```
python pacman.py -p MDPAgent -n 10 -q -l gen/classic/1
```

The options -n, -q, etc.. have been explained in detail in pacman.py