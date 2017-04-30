'''
Module description: 
    this script is just like experiment 4 except that the prosocial phenotype 
    used is reciprocating instead of altruistic. The purpose is to test the 
    hypothesis that reciprocity is a higher fitness phenotype than altruism.

Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from evo_simulator import EvolutionSimulator
from socialunits.enums import ReproductionType, ProsocialityType
from migration import randomRedistribution
from time import time
from socialunits.enums import Phenotype

'''test every combination of cost of prosociality from 0 to .2 in steps of .01 and 
extra reproduction probability from 0 to .4 in steps of .05.'''

# write column titles only on the first simulatation
toWriteColumnTitles = True
for costOfProsociality in [prob / 100.0 for prob in range(0, 21)]:
    for extraReproductionProbability in [prob / 20.0 for prob in range(0, 9)]:
        if costOfProsociality > .01 or extraReproductionProbability > 0:
            toWriteColumnTitles = False
        
        simulator = EvolutionSimulator(migrationFunction = randomRedistribution, 
                              prosocialPhenotype=Phenotype.reciprocating,
                              rounds=30, targetGroupSize=10, seedProportionProsocial = .53,
                              reproduction=ReproductionType.asexual, costOfProsociality=costOfProsociality, 
                              extraReproductionProbability=extraReproductionProbability, baseReproductionChances=1, 
                              baseReproductionProbability=1.0, mutationRate=0.0,
                              typeProsociality=ProsocialityType.strong, toWriteCSV=True, toPrintDataVecs=False, 
                              fileName='experiment6_reciprocity.csv', toWriteColumnTitles=toWriteColumnTitles)
        
        # print length of time for each round--helps for identifying when population grows so much that the
        # simulatation algorithm becomes very slow
        startTime = time()
        
        # run one round with given parameters
        simulator.runEvolutionarySimulation()
        
        print('finished round:')
        print(' costOfProsocialiy = ' + str(costOfProsociality))  
        print(' extraReproductionProbability = ' + str(extraReproductionProbability))
        print(' execution time = ' + str(time() - startTime) + '\n')