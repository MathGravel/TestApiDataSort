import sys
from datetime import datetime
import random


template_test_name = "test_n{}_date_{}.txt"
limits = [100,1000,10000]

def generator(nInstances,rng):
    identifiers = [str(rng.getrandbits(30)) for i in range(nInstances)]
    values = [str(rng.getrandbits(15)) for i in range(nInstances)]
    for line in [a[0]+"_"+a[1] for a in zip(identifiers,values)]:
        yield line


def generate_test_file(nInstances,rng):
    test_name = template_test_name.format(nInstances,datetime.now().strftime("%Y%m%d%H%M%S"))
    with open(test_name, 'w') as f:
        for line in generator(nInstances,rng):
            f.write(line+"\n")
        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <nInstances> \n For more info, see README.md")
        sys.exit(1)
    if not sys.argv[1].isdigit():
        print("nInstances must be an integer")
        sys.exit(1)
    rng = random.Random()
    rng.seed(datetime.now().timestamp())
    generate_test_file(int(sys.argv[1]),rng)
