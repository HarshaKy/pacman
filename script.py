import subprocess

# base_command = 'py -2 pacman.py -l gen/corners/{} -p CornerSeekingAgent -q'
# base_command = 'py -2 pacman.py -l gen/classic/{} -p MDPAgent -n 25 -q'
base_command = 'py -2 pacman.py -p QLearningAgent -x 50 -q -n 100 -l gen/classic/{}'

for i in range(1, 11):
    command = base_command.format(i)
    subprocess.run(command, shell=True)