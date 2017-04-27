'''
Module description: 
    this script runs a number of evolutionary simulations testing different combinations
    of two parameters: target group size, and extra reproduction probability. The hypothesis
    under consideration is that as group size decreases, the success of multilevel selection
    in increasing the proportion of altruists in the population at large will increase as well.  
    
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from evo_simulator import EvolutionSimulator
from socialunits.enums import ReproductionType, ProsocialityType
from migration import randomRedistribution
from time import time

'''test every combination of target group size from 2 to 18 and extra reproduction probability from 
0 to .6 in steps of .1.'''

# write column titles only on the first simulatation
toWriteColumnTitles = True
for targetGroupSize in range (2, 19):
    for extraReproductionProbability in [prob / 10.0 for prob in range(0, 7, 1)]:
        if targetGroupSize > 2 or extraReproductionProbability > 0:
            toWriteColumnTitles = False
        
        simulator = EvolutionSimulator(migrationFunction = randomRedistribution,
                              rounds=40, targetGroupSize=targetGroupSize, seedProportionProsocial = .6,
                              reproduction=ReproductionType.asexual, costOfAltruism=.02, 
                              extraReproductionProbability=extraReproductionProbability, baseReproductionChances=1, 
                              baseReproductionProbability=.85, mutationRate=0,
                              altruismType=ProsocialityType.strong, toWriteCSV=True, toPrintDataVecs=False, 
                              fileName='testDataPhase1.csv', toWriteColumnTitles=toWriteColumnTitles)
        
        # print length of time for each round--helps for identifying when population grows so much that the
        # simulatation algorithm becomes very slow
        startTime = time()
        
        # run one round with given parameters
        simulator.runEvolutionarySimulation()
        
        print('finished round: targetGroupSize = ' + str(targetGroupSize) + 
              ', extraReproductionProbability = ' + str(extraReproductionProbability))
        print('execution time = ' + str(time() - startTime) + '\n')