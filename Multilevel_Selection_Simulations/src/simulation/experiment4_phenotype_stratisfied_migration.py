'''
Module description: 
    this script is similar to those of experiments 1 and 2, except that the
    two parameters tested are cost of prosociality and extra reproduction 
    probability, instead of group size and extra reproduction probability.
    Also phenotype stratisfied migration is used in place of random redistribution. 
    The purpose is to corroborate the claim that populations with 
    phenotype-stratified groups better favor multi-level selection, as well
    as to visualize the relationship between the aforementioned parameters
    and the fitness of the altruistic phenotype.
     
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from evo_simulator import EvolutionSimulator
from socialunits.enums import ReproductionType, ProsocialityType
from migration import biasedRedistribution
from time import time

'''test every combination of cost of prosociality from 0 to .2 in steps of .01 and 
extra reproduction probability from 0 to .5 in steps of .05.'''

# write column titles only on the first simulation
toWriteColumnTitles = True
for costOfProsociality in [prob / 100.0 for prob in range(0, 21)]:
    for extraReproductionProbability in [prob / 20.0 for prob in range(0, 11)]:
        if costOfProsociality > .01 or extraReproductionProbability > 0:
            toWriteColumnTitles = False
        
        simulator = EvolutionSimulator(migrationFunction = biasedRedistribution,
                              rounds=30, targetGroupSize=10, seedProportionProsocial = .53,
                              reproduction=ReproductionType.asexual, costOfProsociality=costOfProsociality, 
                              extraReproductionProbability=extraReproductionProbability, baseReproductionChances=1, 
                              baseReproductionProbability=1.0, mutationRate=0.0,
                              typeProsociality=ProsocialityType.strong, toWriteCSV=True, toPrintDataVecs=False, 
                              fileName='experiment4_phenotype_stratified_migration.csv', toWriteColumnTitles=toWriteColumnTitles)
        
        # print length of time for each round--helps for identifying when population grows so much that the
        # simulation algorithm becomes very slow
        startTime = time()
        
        # run one round with given parameters
        simulator.runEvolutionarySimulation()
        
        print('finished round:')
        print(' costOfProsocialiy = ' + str(costOfProsociality))  
        print(' extraReproductionProbability = ' + str(extraReproductionProbability))
        print(' execution time = ' + str(time() - startTime) + '\n')