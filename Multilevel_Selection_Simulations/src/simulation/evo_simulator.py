'''
Module description: 
    defines a single custom class, EvolutionSimulator, which simulates 
    evolution under game-theoretic scenarios for the purpose of investigating 
    multi-level selection theory as an explanation for altruism
    
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from socialunits.individual import Individual 
from socialunits.group import SocialGroup
from socialunits.enums import Genotype, ReproductionType, AltruismType
from migration import randomRedistribution, migrationDict
from itertools import chain
import math, random, csv, threading
from os.path import join
from test.test_bufio import lengths
      
class EvolutionSimulator:
    
    '''
    Description:
        runs highly parameterized evolutionary simulations for the purpose of investigating 
        multi-level selection theory as an explanation for the persistence of altruistic behavior
        in populations. The constructor is designed to allow overriding
        to extend/modify functionality. 
    
    Non-instance variable parameters:
    # fileName: name of CSV file to write/append, including extension
    
    Parameters/instance variables:
    # numGroups: number of groups--initially has value of parameter numGroups
    # migrationFunction: function for managing migration of individuals from group to group,
        between rounds. Choose from functions defined in simulation.migration, or create a custom function
    # mutationRate: probability that an allele in offspring is opposite of parnent's
    # threaded: boolean, whether or not certain thread-safe operations are run in parallel (4 threads max)
    # toWriteCSV: boolean, whether to record data to CSV file
    # toWriteColumnTitles: boolean, whether to write column titles to CSV file. Useful to specify as false
        when appending to a file that already has titles
     # toPrintDataVecs: boolean, whether to print vectors of data at end of simulation
    
    Keyword args/instance variables:
    ***NOTE***: parameters regarding death are not specified in this implementation as
        it is implicit in the default behavior of socialunits.group.SocialGroup that all 
        individuals perish after one round of reproduction. 
    # reproduction: must be of type socialunits.enums.ReproductionType
    # baseReproductionChances: baseline number of reproduction opportunities to have +1 child per individual 
        per round
    # baseReproductionProbability: baseline probability of successful reproduction for each opportunity in 
        baseReproductionChances
    # costOfAltruism: value of the cost incurred as the result of altruism. Value is subtracted from 
        baseReproductionProbability to modulate altruists' reproduction
    # extraReproductionProbability: probability of successful reproduction of +1 child beyond base reproduction.
        However many times one is the beneficiary of altruism, one has that many chances at
        extra offspring with a probability each time of extraReproductionProbability  
    # altruismType: must be of type socialunits.enums.AltruismType. See class's docstring for 
        details
    # targetGroupSize: all groups to be of this size or targetGroupSize+1, provided population size is 
        greater than targetGroupSize
    # seedProportionAltruistic: approximate proportion of altruists in starting population (actual number
        of altruists equals the ceiling of seedProportionAltruistic times the initial population size
    # rounds: number of rounds of the simulation
    
    Other instance variables:
    # populationCount: count of population at large--initially assigned numGroups*targetGroupSize
    # allIndividuals: list of all individuals (type socialunits.inidividual.Individual) in population
    # groups: list of all groups (type socialunits.group.SocialGroup)
    # kwargs: reference to key word args maintained so that they can be inputted to instance methods 
        of class SocialGroup as required
    # groupCountsVec: list of counts of groups (how many groups in play each round)
    # populationCountsVec: list of counts of total population (how many total individuals each round)
    # altruistProportionsVec: list of altruist proportions (proportion of altruists each round)
    # prefixParams: vector of numeric values that represent simulation parameters. prefixParams 
        gets concatenated with vectors of output data before vectors appended to CSV file. Initialized
        only if toWriteCSV or toPrintDataVecs is true
    # columnTitles: titles of columns for data vectors. Initialized only if towriteCSV or
        toPrintDataVecs is true
    # filePath: path for which to write/append CSV file. Initialized only if toWriteCSV is true
    # countAltruistic: total count of altruistic individuals in population
    # countSelfish: total count of selfish individuals in population
    
    Errors:
    # TypeError: raised if reproduction is not of type socialunits.enums.ReproductionType
    # TypeError: raised if altruismType not of type socialunits.enums.AltruismType 
    '''
    
    def __init__(self, numGroups=2, migrationFunction=randomRedistribution, 
                 mutationRate=0, threaded=True, toWriteCSV=False, fileName=None, toWriteColumnTitles=True, 
                 toPrintDataVecs=False, **kwargs):
        
        # instance vars that may have default value: 
        self.numGroups = numGroups
        self.migrationFunction = migrationFunction
        self.mutationRate = mutationRate
        self.threaded = threaded
        self.toWriteCSV = toWriteCSV
        self.toWriteColumnTitles = toWriteColumnTitles
        self.toPrintDataVecs = toPrintDataVecs
                
        #keyword args:
        self.reproduction = kwargs['reproduction']
        if not isinstance(self.reproduction, ReproductionType):
            raise TypeError('reproduction must be of type socialunits.enums.ReproductionType')
        self.baseReproductionChances = kwargs['baseReproductionChances']
        self.baseReproductionProbability = kwargs['baseReproductionProbability']
        self.costOfAltruism = kwargs['costOfAltruism'] 
        self.extraReproductionProbability = kwargs['extraReproductionProbability']
        self.altruismType = kwargs['altruismType']
        if not isinstance(self.altruismType, AltruismType):
            raise TypeError('altruismType must of type socialunits.enums.AltruismType')
        self.targetGroupSize = kwargs['targetGroupSize']
        self.seedProportionAltruistic = kwargs['seedProportionAltruistic']
        self.rounds = kwargs['rounds']
        
        #other instance vars:
        self.populationCount = self.numGroups * self.targetGroupSize
        self.allIndividuals = []
        self.groups = []
        self.kwargs = kwargs
        self.groupCountsVec = []
        self.populationCountsVec = []
        self.altruistProportionsVec = []
        if toWriteCSV or self.toPrintDataVecs:
            self.prefixParams = self._prefixParams()
            self.columnTitles = self._columnTitles()
            if toWriteCSV:
                self.filePath = join('..', '..', fileName) 
        
        '''initialize all individuals to specifications of phenotype proportions. Also initializes two additional
           instance variables, countAltuistic and countSelfish'''
        if self.reproduction == ReproductionType.asexual:
            self._createIndividualsAsexual(self.seedProportionAltruistic)
        elif self.reproduction == ReproductionType.sexual:
            self._createIndividualsSexual(self.seedProportionAltruistic)
        
        # initialize groups:
        for _ in range(self.numGroups):
            self.groups.append(SocialGroup(self.reproduction))
            
    def _createIndividualsAsexual(self, seedProportionAltruistic):
        self.countAltruistic = int(math.ceil(self.populationCount * seedProportionAltruistic))
        self.countSelfish = self.populationCount - self.countAltruistic
        self.allIndividuals = list(chain(
                                  [Individual(Genotype.A, self.reproduction, self.mutationRate) for _ in range(self.countAltruistic)], 
                                  [Individual(Genotype.S, self.reproduction, self.mutationRate) for _ in range(self.countSelfish)]))
    
    def _createIndividualsSexual(self, seedProportionAltruistic):
        raise RuntimeError('Sexual reproduction not yet implemented')
    
    def _prefixParams(self):    
        
        '''
        returns a vector numeric values represent the parameters/independent variables of the simulation. These
        will be prepending the vectors containing the dependent trial data. In this way the simulation parameters
        get associated with results before the data is written to file. The five values of -10 are placeholders
        for additional parameters, so that if parameters are added later earlier data will still have vectors of
        equal length
        '''
        
        return [self.targetGroupSize, self.extraReproductionProbability, self.costOfAltruism,
                self.rounds, self.baseReproductionChances, self.baseReproductionProbability,
                self.altruismType.value, migrationDict[self.migrationFunction], self.seedProportionAltruistic,
                self.reproduction.value, self.mutationRate, -10, -10, -10, -10, -10] 
    
    def _columnTitles(self):
        
        '''returns column titles for data vectors'''
        
        roundTitles = ['starting state'] + ['Round ' + str(i+1) for i in range(self.rounds)]
        placeholderTitles = ['placeholder ' + str(i) for i in range(1,6)]
        return ['dependent vars', 'target group size', 'benefit from altruism', 'cost to altruist', 
                'number of rounds', 'base reproduction rate', 'base reproduction probability',
                'altruism type', 'migration type', 'seed proportion altruistic', 
                'reproduction method', 'mutation rate'] + placeholderTitles + roundTitles 
    
    # merge members of all groups into single population
    def _mergeGroups(self):
        self.allIndividuals = []
        self.allIndividuals = list(chain(*[group.members for group in self.groups]))
        #for group in self.groups:
            #self.allIndividuals += group.members
    
    # resets list of groups for next round    
    def _resetGroups(self):
        self.numGroups = self.populationCount / self.targetGroupSize
        self.groups = [SocialGroup(self.reproduction) for _ in range(self.numGroups)]
    
    def _migrationPhase(self):
        self.migrationFunction(self)
    
    def _assignToGroupsRandomly(self, individuals):
        # shuffles population to achieve random group assignment
        random.shuffle(individuals)
        # assign to groups
        while len(individuals) > 0:
            for group in self.groups:
                if len(individuals) > 0:
                    group.addMember(individuals.pop())
                else:
                    break; 
    
    def _initiateGroupAssignment(self):
        self._assignToGroupsRandomly(self.allIndividuals)
        
    def _writeColumnTitles(self):
        with open(self.filePath, 'wb') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(self.columnTitles)
            
    def _updateGroupData(self):
        self.populationCount = 0
        self.countAltruistic = 0
        self.countSelfish = 0
        
        for group in self.groups:
            self.countAltruistic += group.countAltruistic
            self.countSelfish += group.countSelfish
            self.populationCount += group.size()
        
        try:
            self.altruistProportionsVec.append(self.countAltruistic / float(self.populationCount))
        except ZeroDivisionError:
            self.altruistProportionsVec.append(-1)
        self.populationCountsVec.append(self.populationCount)
        self.groupCountsVec.append(self.numGroups)
           
    def _finalizeDataVecs(self):
        self.altruistProportionsVec = ['altruist proportions'] + self.prefixParams + self.altruistProportionsVec
        self.populationCountsVec = ['population counts'] + self.prefixParams + self.populationCountsVec
        self.groupCountsVec = ['groups counts'] + self.prefixParams + self.groupCountsVec
        
    def _writeDataVecs(self):
        with open(self.filePath, 'ab') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(self.altruistProportionsVec)
            csvWriter.writerow(self.populationCountsVec)
            csvWriter.writerow(self.groupCountsVec)
    
    def _printDataVecs(self):
        print(self.columnTitles)
        print(self.altruistProportionsVec)
        print(self.populationCountsVec)
        print(self.groupCountsVec)
    
    def  runEvolutionarySimulation(self):
     
        '''
         Description: runs complete evolutionary simulation. Works principally by running
             a loop as many times as self.rounds. For each round, for each group in self.groups,
             the instance methods socialunits.group.SocialGroup playSocialGame() and
             deathAndReproduction() are called for each group, followed by migration phase (managed
             by method _migrationPhase() of this class). Threading is used to process instance 
             methods of SocialGroup in parallel, with self.splits number of threads, the value of 
             which can be specified as a constructor parameter (note that if playSocialGame or 
             deathAndReproduction are overridden and changed in such a way that groups interact
             with other groups during these methods, self.numSplits will need to set to zero to
             avoid race conditions)  
         '''
        
        def getSplits(self):
            splits = []
            length = len(self.groups)
            if length >= 4:
                splitSize = length / 4
                splits.append(self.groups[:splitSize])
                splits.append(self.groups[splitSize:splitSize * 2])
                splits.append(self.groups[splitSize * 2: splitSize * 3])
                splits.append(self.groups[splitSize*3:])
            elif length >= 2:
                splits.append(self.groups[:length / 2])
                splits.append(self.groups[length / 2:])
            else: 
                splits.append(self.groups)
            return splits
            
        def _runLifeCycleGroupsSplit(self, splitOfGroups):
            for group in splitOfGroups:
                group.playSocialGame(**self.kwargs)
                group.deathAndReproduction(**self.kwargs)
                
        self._initiateGroupAssignment()
        if self.toWriteCSV:
            if self.toWriteColumnTitles:
                self._writeColumnTitles()
            self._updateGroupData()
        for _ in range(self.rounds):
            if self.threaded:
                splits = getSplits(self)
                threads = []
                for split in splits:
                    thread = threading.Thread(target=_runLifeCycleGroupsSplit, args=(self, split,))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
            else:
                _runLifeCycleGroupsSplit([self.groups])
            self._migrationPhase()
            self._updateGroupData()
            
        self._finalizeDataVecs()
        if self.toPrintDataVecs:
            self._printDataVecs()
        if self.toWriteCSV:
            self._writeDataVecs()
            
if __name__ == '__main__':                      
    simulator = EvolutionSimulator(migrationFunction = randomRedistribution,
                              rounds=40, targetGroupSize=10, seedProportionAltruistic = .6,
                              reproduction=ReproductionType.asexual, costOfAltruism=.1, 
                              extraReproductionProbability=.5, baseReproductionChances=1, 
                              baseReproductionProbability=1.0, mutationRate=0,
                              altruismType=AltruismType.weak, toWriteCSV=True, toPrintDataVecs=True, 
                              fileName='testData.csv')
    simulator.runEvolutionarySimulation()