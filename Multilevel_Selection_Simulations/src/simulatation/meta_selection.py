'''
Created on Apr 10, 2017

@author: Will_Masha
'''

from evo_simulator import EvolutionSimulator
from socialunits.enums import ReproductionType, ProsocialityType
from migration import randomRedistribution
from socialunits.group import SocialGroup
from math import floor
from random import choice
from time import time


def _deathAndReproductionAsexual(self, **kwargs):
        
    '''subsidiary method of deathAndReproduction. Called for asexually reproducing group'''
    
    groupStartSize = self.size()
    newProgenyCount = 0
    
    allProgeny = SocialGroup(self.reproduction)
    for member in self.members:
        for _ in range(kwargs['baseReproductionChances']):
            newProgeny = member.attemptReproduction(kwargs['baseReproductionProbability'] - member.prosocialCostIncurred)
            if not newProgeny == None:
                allProgeny.addMember(newProgeny)
                newProgenyCount += 1
        for _ in range(member.extraReproductionChances):
            newProgeny = member.attemptReproduction(kwargs['extraReproductionProbability'])
            if not newProgeny == None:
                allProgeny.addMember(newProgeny)
                newProgenyCount += 1
    
    growthRate = newProgenyCount/float(groupStartSize)
    metaReproductionProbability = growthRate * kwargs['metaReproductionCoefficient']
    metaReproductionChances = floor(kwargs['percentMetaParticipation'] * groupStartSize)
    for _ in range(metaReproductionChances):
        newProgeny = choice(self.members).attemptReproduction(metaReproductionProbability)
        if not newProgeny == None:
            allProgeny.addMember(newProgeny)
        
    '''copy all essential instance variables from allProgeny to self. In this way the 
       death of the entire parent generation is implicit'''
    self._supplantGroup(allProgeny)
    
    
toWriteColumnTitles = True
# 0 to .2 in increments of .05
for metaReproductionCoefficient in [coeff / 20 for coeff in range(0, 3, 1)]:
    for extraReproductionProbability in [prob / 10.0 for prob in range(0, 7, 1)]:
        if metaReproductionCoefficient > 0 or extraReproductionProbability > 0:
            toWriteColumnTitles = False
        
        simulator = EvolutionSimulator(migrationFunction = randomRedistribution,
                              rounds=40, targetGroupSize=12, seedProportionProsocial = .6,
                              reproduction=ReproductionType.asexual, costOfAltruism=.02, 
                              extraReproductionProbability=extraReproductionProbability, baseReproductionChances=1, 
                              baseReproductionProbability=.85, mutationRate=0,
                              altruismType=ProsocialityType.strong, metaReproductionCoefficient=metaReproductionCoefficient,
                              percentMetaParticipation=.3, toWriteCSV=True, toPrintDataVecs=False, 
                              fileName='testDataPhase1.csv', toWriteColumnTitles=toWriteColumnTitles)
        
        startTime = time()
        simulator.runEvolutionarySimulation()
        
        print('finished round: metaReproductionCoefficient = ' + str(metaReproductionCoefficient) + 
              ', extraReproductionProbability = ' + str(extraReproductionProbability))
        print('execution time = ' + str(time() - startTime))
