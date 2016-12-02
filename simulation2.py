 # This is modified based on part 1. You can switch backoff algorithm in Ethernet run function

import random
import simpy
import math

RANDOM_SEED = 29
SIM_TIME = 1000000
Ts = 1
NUM_HOSTS = 10;

class Ethernet:
        def __init__(self, env, arrival_rate):
            self.env = env
            self.arrival_rate = arrival_rate
            self.hosts = [Host(env,arrival_rate) for i in range(NUM_HOSTS)]
            self.transmitted = 0
            self.collisions = 0

        def run(self, env):
            while True:
                transHosts = []
                for host in self.hosts:
                    #if a host is trying to transmit now
                    if ((host.L > 0) and (math.floor(env.now) == host.S)):
                            transHosts.append(host)
                #if no collision, let the host transmit
                if (len(transHosts) == 1):
                    transHosts[0].process_packet(env)
                    self.transmitted += 1
                
                #if two or more packets try to send now, there is collision
                if (len(transHosts) > 1):
                    for host in transHosts:
                            #!!!
                        #change backoff method here
                        host.exp_backoff(env)
                        self.collisions += 1

                #timeout for a timeslot slot Ts
                yield self.env.timeout(Ts) 
                

def main():
        random.seed(RANDOM_SEED)
        print ("{0:<12} {1:<17} {2:<10} {3:<15}".format(
                "Arrival_rate","TransmittedPackets", "Throughput", "Collision"))
        #lambda is set here
        for arrival_rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:             
                env = simpy.Environment()

                #start running the ethernet
                ether = Ethernet(env, arrival_rate)
                env.process(ether.run(env))
                env.run(until=SIM_TIME)
                print ("{0:<12.2f} {1:<17} {2:<10.5f} {3:<15} ".format(
                        float(arrival_rate),
                        int(ether.transmitted),
                        float(float(ether.transmitted)/SIM_TIME),
                        int(ether.collisions)))
                #print result
        
if __name__ == '__main__': main()
