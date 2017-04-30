'''
Module description: 
    this script is the same as in experiment 1 except that weak altruism is used
    instead of strong altruism. This controls against the (hypothesized) decrease 
    in relative fitness that occurs with strong altruism as group size becomes lesser.
    The hypothesis here is that altruism fitness will be inversely correlated with 
    group size. Also the range of extra reproduction probability is reduced from 
    0-.6 to 0-.5 to improve computation time.  
    
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from evo_simulator import EvolutionSimulator
from socialunits.enums import ReproductionType, ProsocialityType
from migration import randomRedistribution
from time import time

'''test every combination of target group size from 2 to 21 and extra reproduction probability from 
0 to .5 in steps of .05.'''

# write column titles only on the first simulation
toWriteColumnTitles = True
for targetGroupSize in range (2, 22):
    for extraReproductionProbability in [prob / 20.0 for prob in range(0, 11, 1)]:
        if targetGroupSize > 2 or extraReproductionProbability > 0:
            toWriteColumnTitles = False
        
        simulator = EvolutionSimulator(migrationFunction = randomRedistribution,
                              rounds=30, targetGroupSize=targetGroupSize, seedProportionProsocial = .53,
                              reproduction=ReproductionType.asexual, costOfProsociality=.02, 
                              extraReproductionProbability=extraReproductionProbability, baseReproductionChances=1, 
                              baseReproductionProbability=1.0, mutationRate=0.0,
                              typeProsociality=ProsocialityType.weak, toWriteCSV=True, toPrintDataVecs=False, 
                              fileName='experiment2_weak_selection_control.csv', toWriteColumnTitles=toWriteColumnTitles)
        
        # print length of time for each round--helps for identifying when population grows so much that the
        # simulation algorithm becomes very slow
        startTime = time()
        
        # run one round with given parameters
        simulator.runEvolutionarySimulation()
        
        print('finished round:')
        print(' targetGroupSize = ' + str(targetGroupSize))  
        print(' extraReproductionProbability = ' + str(extraReproductionProbability))
        print(' execution time = ' + str(time() - startTime) + '\n')