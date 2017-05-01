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
from socialunits.enums import Genotype, ReproductionType, ProsocialityType,\
    Phenotype
from migration import randomRedistribution, biasedRedistribution, totalIsolation, getMigrationFunctionKey
from itertools import chain
import math, random, csv, threading
from os.path import join
import numpy
      
class EvolutionSimulator:
    
    '''
    Description:
        runs highly parameterized evolutionary simulations for the purpose of investigating 
        multi-level selection theory as an explanation for the persistence of altruistic behavior
        in populations. The constructor is designed to allow overriding to extend/modify functionality.
        Note that by default, there are only two phenotypes allowed in the population, either altruistic
        vs. selfish, or reciprocating vs. selfish. The altruistic and reciprocating phenotypes are treated 
        similarly and collectively referred to as 'prosocial'. 
    
    Non-instance variable parameters:
    # fileName: name of CSV file to write/append, including extension
    
    Parameters/instance variables:
    # numGroups: number of groups--initially has value of parameter numGroups
    # migrationFunction: function for managing migration of individuals from group to group,
        between rounds. Choose from functions defined in simulation.migration, or create a custom function
    # prosocialPhenotype: member of socialunits.enums.Phenotype, and either altruistic or reciprocating
    # mutationRate: probability that an allele in offspring is opposite of parnent's
    # threaded: boolean, whether or not certain thread-safe operations are run in parallel (4 threads used)
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
    # costOfProsociality: value of the cost incurred as the result of prosocial behavior. Value is subtracted 
        from baseReproductionProbability to modulate prosocial individuals' reproduction
    # extraReproductionProbability: probability of successful reproduction of +1 child beyond base reproduction.
        However many times one is the beneficiary of prosocial behavior, one has that many chances at
        extra offspring with a probability each time of extraReproductionProbability  
    # typeProsociality: must be of type socialunits.enums.ProsocialityType. See class's docstring for 
        details
    # targetGroupSize: all groups begin each round at this size at least, but may be as high as 
        one less than double targetGroupSize. Group sizes are determined by, at the end of each round, 
        taking as many groups as the the floor of the total population divided by targetGroupSize, and 
        dividing individuals between them as evenly as possible. So long as the total population greatly 
        exceeds, targetGroupSize, actual group sizes tend to equal targetGroupSize or targetGroupSize+1.
    # seedProportionProsocial: approximate proportion of prosocial individuals in starting population 
        (actual number of prosocial individuals equals the ceiling of seedProportionProsocial times the initial population size)
    # rounds: number of rounds of the simulation
    
    Other instance variables:
    # populationCount: count of population at large--initially assigned numGroups*targetGroupSize
    # allIndividuals: list of all individuals (type socialunits.inidividual.Individual) in population
    # groups: list of all groups (type socialunits.group.SocialGroup)
    # kwargs: reference to key word args maintained so that they can be inputted to instance methods 
        of class SocialGroup as required
    # groupCountsVec: list of counts of groups (how many groups in play each round)
    # populationCountsVec: list of counts of total population (how many total individuals each round)
    # prosocialProportionsVec: list of prosocial proportions (proportion of prosocial individuals each round)
    # stdDeviationsVec: list of standard deviations (one per round) of prosocial proportions among all groups 
    # prefixParams: vector of numeric values that represent simulation parameters. prefixParams 
        gets concatenated with vectors of output data before vectors appended to CSV file. Initialized
        only if toWriteCSV or toPrintDataVecs is true
    # columnTitles: titles of columns for data vectors. Initialized only if towriteCSV or
        toPrintDataVecs is true
    # filePath: path for which to write/append CSV file. Initialized only if toWriteCSV is true
    # countProsocial: total count of prosocial individuals in population
    # countSelfish: total count of selfish individuals in population
    
    Constructor method signature: __init__(self, numGroups=10, migrationFunction=randomRedistribution, 
        prosocialPhenotype=Phenotype.altruistic, mutationRate=0, threaded=True, toWriteCSV=False, 
        fileName=None, toWriteColumnTitles=True, toPrintDataVecs=True, **kwargs)
        
    Public methods:
    # runEvolutionarySimulation(self): runs complete evolutionary simulation given parameters specified
        in constructor
    '''
    
    def __init__(self, numGroups=10, migrationFunction=randomRedistribution, prosocialPhenotype=Phenotype.altruistic,
                 mutationRate=0, threaded=True, toWriteCSV=False, fileName=None, toWriteColumnTitles=True, 
                 toPrintDataVecs=True, **kwargs):
        
        '''
        --See class's docstring for description of constructor's parameters-- 
        
        Errors:
        # TypeError: raised if reproduction is not of type socialunits.enums.ReproductionType
        # TypeError: raised if typeProsociality not of type socialunits.enums.ProsocialityType 
       ''' 
        
        # instance vars that may have default value: 
        self.numGroups = numGroups
        self.migrationFunction = migrationFunction
        self.prosocialPhenotype = prosocialPhenotype
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
        self.costOfProsociality = kwargs['costOfProsociality'] 
        self.extraReproductionProbability = kwargs['extraReproductionProbability']
        self.typeProsociality = kwargs['typeProsociality']
        if not isinstance(self.typeProsociality, ProsocialityType):
            raise TypeError('typeProsociality must of type socialunits.enums.ProsocialityType')
        self.targetGroupSize = kwargs['targetGroupSize']
        self.seedProportionProsocial = kwargs['seedProportionProsocial']
        self.rounds = kwargs['rounds']
        
        #other instance vars:
        self.populationCount = self.numGroups * self.targetGroupSize
        self.allIndividuals = []
        self.groups = []
        self.kwargs = kwargs
        self.groupCountsVec = []
        self.populationCountsVec = []
        self.prosocialProportionsVec = []
        self.stdDeviationsVec = []
        if toWriteCSV or self.toPrintDataVecs:
            self.prefixParams = self._prefixParams()
            self.columnTitles = self._columnTitles()
            if toWriteCSV:
                self.filePath = join('..', '..', 'simulationdata', fileName) 
        
        '''initialize all individuals to specifications of phenotype proportions. Also initializes two additional
           instance variables, countProsocial and countSelfish'''
        if self.reproduction == ReproductionType.asexual:
            self._createIndividualsAsexual(self.seedProportionProsocial)
        elif self.reproduction == ReproductionType.sexual:
            self._createIndividualsSexual(self.seedProportionProsocial)
        
        # initialize groups:
        for _ in range(self.numGroups):
            self.groups.append(SocialGroup(self.reproduction))
            
    def _createIndividualsAsexual(self, seedProportionProsocial):
        
        '''initialize asexually reproducing population by populating list self.allIndividuals'''
        
        self.countProsocial = int(math.ceil(self.populationCount * seedProportionProsocial))
        self.countSelfish = self.populationCount - self.countProsocial
        if self.prosocialPhenotype == Phenotype.altruistic:
            prosocialGenotype = Genotype.A
        elif self.prosocialPhenotype == Phenotype.reciprocating:
            prosocialGenotype = Genotype.R
        self.allIndividuals = list(chain(
                                  [Individual(prosocialGenotype, self.reproduction, self.mutationRate) for _ in range(self.countProsocial)], 
                                  [Individual(Genotype.S, self.reproduction, self.mutationRate) for _ in range(self.countSelfish)]))
    
    def _createIndividualsSexual(self, seedProportionProsocial):
        
        '''initialize sexually reproducing population by populating list self.allIndividuals'''
        
        raise RuntimeError('sexual reproduction not yet implemented')
    
    def _prefixParams(self):    
        
        '''
        returns a vector numeric values represent the parameters/independent variables of the simulation. These
        will prepend the vectors containing the dependent trial data. In this way the simulation parameters
        get associated with results before the data is written to file. The five values of -10 are placeholders
        for additional parameters, so that if parameters are added later earlier data will still have vectors of
        equal length
        '''
        
        return [self.targetGroupSize, self.extraReproductionProbability, self.costOfProsociality, self.reproduction.value,
                self.prosocialPhenotype.value, self.rounds, self.baseReproductionChances, self.baseReproductionProbability,
                self.typeProsociality.value, getMigrationFunctionKey(self.migrationFunction), self.seedProportionProsocial,
                self.mutationRate, -10, -10, -10, -10, -10] 
    
    def _columnTitles(self):
        
        '''returns column titles for data vectors'''
        
        roundTitles = ['starting state'] + ['Round ' + str(i+1) for i in range(self.rounds)]
        placeholderTitles = ['placeholder ' + str(i) for i in range(1,6)]
        return ['dependent vars', 'target group size', 'extra reproduction probability', 'cost of prosociality', 
                'reproduction type', 'prosocial phenotype', 'number of rounds', 'base reproduction rate', 
                'base reproduction probability', 'prosociality type', 'migration type', 'seed proportion prosocial', 
                'mutation rate'] + placeholderTitles + roundTitles 
          
    def _writeColumnTitles(self):
        
        '''writes column titles to file'''
        
        with open(self.filePath, 'ab') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(self.columnTitles)
            
    def _finalizeDataVecs(self):
        
        '''appends row titles with prefix parameters and dependant variable data to put data vectors in final
        representation'''
        
        self.prosocialProportionsVec = ['prosociality proportions:'] + self.prefixParams + self.prosocialProportionsVec
        self.populationCountsVec = ['population counts:'] + self.prefixParams + self.populationCountsVec
        self.groupCountsVec = ['groups counts:'] + self.prefixParams + self.groupCountsVec
        self.stdDeviationsVec = ['standard deviations in prosocial proportions'] + self.prefixParams + self.stdDeviationsVec
        
    def _writeDataVecs(self):
        
        '''writes data vectors to file'''
        
        with open(self.filePath, 'ab') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(self.prosocialProportionsVec)
            csvWriter.writerow(self.populationCountsVec)
            csvWriter.writerow(self.groupCountsVec)
            csvWriter.writerow(self.stdDeviationsVec)
    
    def _printDataVecs(self):
        
        '''prints data vectors'''
        
        print(self.columnTitles)
        print(self.prosocialProportionsVec)
        print(self.populationCountsVec)
        print(self.groupCountsVec)
        print(self.stdDeviationsVec)
        
    def _updatePopulationData(self):
        
        '''called each round to append data from round to data vectors'''
        
        # update counts and make list of group's proportions to calculate std deviation
        self.populationCount = 0
        self.countProsocial = 0
        self.countSelfish = 0
        prosocialProportionsAllGroups = []
        for group in self.groups:
            self.countProsocial += group.countProsocial
            self.countSelfish += group.countSelfish
            self.populationCount += group.size()
            try:
                prosocialProportionsAllGroups.append(group.proportionProsocial())
            except ZeroDivisionError:
                # skip appending proportion of groups for which the population is zero
                pass
            
        # append to data vectors
        try:
            self.prosocialProportionsVec.append(self.countProsocial / float(self.populationCount))
        except ZeroDivisionError:
            # proportion of -.1 indicates that populationCount is 0, thus entire population is extinct
            self.prosocialProportionsVec.append(-.1)
        self.populationCountsVec.append(self.populationCount)
        self.groupCountsVec.append(self.numGroups)
        if prosocialProportionsAllGroups:
            self.stdDeviationsVec.append(numpy.std(prosocialProportionsAllGroups))
        else:
            # append with -1 in case of complete extinction of population
            self.stdDeviationsVec.append(-1)
    def _mergeGroups(self):
        
        '''merge members of all groups into single population'''
        
        self.allIndividuals = []
        self.allIndividuals = list(chain(*[group.members for group in self.groups]))
        
    def _resetGroupsBeforeReassignment(self):
        
        '''reassigns self.groups with a new list of groups of appropriate length for next round'''

        self.populationCount = len(self.allIndividuals)
        if self.populationCount == 0:
            self.numGroups = 0
            self.groups = []
            return
        
        '''normally if targetGroupSize does not equally divide the population, the number of groups
        is rounded down and some groups take on extra members. However if rounding down would result in
        zero groups, 1 group is maintained'''
        self.numGroups = self.populationCount / self.targetGroupSize        
        if self.numGroups == 0:
            self.numGroups = 1
        
        self.groups = [SocialGroup(self.reproduction) for _ in range(self.numGroups)]
        
    def _migrationPhase(self):
        
        '''wrapper method that simply calls the migration function instance variable'''
        
        self.migrationFunction(self)
    
    def _assignToGroupsRandomly(self, individuals):
        
        '''randomly assigns individuals in input list to groups'''
        
        # shuffle individuals to achieve random ordering
        random.shuffle(individuals)
        
        # assign to groups one by one
        while len(individuals) > 0:
            for group in self.groups:
                if len(individuals) > 0:
                    group.addMember(individuals.pop())
                else:
                    break; 

    def  runEvolutionarySimulation(self):
     
        '''
         Description: runs complete evolutionary simulation. Works principally by running
             a loop as many times as self.rounds. For each round, for each group in self.groups,
             the instance methods socialunits.group.SocialGroup playSocialGame() and
             deathAndReproduction() are called, followed by migration phase (managed by method 
             _migrationPhase of this class). If self.threaded is true, threading is used to process 
             instance methods of SocialGroup in parallel, with four threads (note that if playSocialGame 
             or deathAndReproduction are overridden and changed in such a way that groups interact with 
             other groups during the execution of these methods, self.threaded will need to be set 
             to false to avoid race conditions).  
         '''
        
        def getSplits(self):
            
            '''split self.groups into a list of up to four splits for the purposes of threading'''
            
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
            
            '''runs life cycle of group for a single split of groups'''
            
            for group in splitOfGroups:
                group.playSocialGame(**self.kwargs)
                group.deathAndReproduction(**self.kwargs)
         
        # initial assignment to groups        
        self._assignToGroupsRandomly(self.allIndividuals)
        
        # prepare initial data if printing or writing data
        if self.toWriteCSV or self.toPrintDataVecs:
            if self.toWriteCSV:
                if self.toWriteColumnTitles:
                    self._writeColumnTitles()
            self._updatePopulationData()
        
        # play every round    
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
                _runLifeCycleGroupsSplit(self, self.groups)
                                
            self._migrationPhase()
            
            if self.toWriteCSV or self.toPrintDataVecs:
                self._updatePopulationData()
        
        if self.toWriteCSV or self.toPrintDataVecs:    
            self._finalizeDataVecs()
            if self.toPrintDataVecs:
                self._printDataVecs()
            if self.toWriteCSV:
                self._writeDataVecs()
            
if __name__ == '__main__':
    
    '''use main for testing/debugging, modifying parameters as desired'''
                         
    simulator = EvolutionSimulator(numGroups=10, migrationFunction = biasedRedistribution, 
                                    prosocialPhenotype=Phenotype.altruistic,
                                    rounds=30, targetGroupSize=10, seedProportionProsocial = .6,
                                    reproduction=ReproductionType.asexual, costOfProsociality=0.00, 
                                    extraReproductionProbability=.5, baseReproductionChances=1, 
                                    baseReproductionProbability= .85, mutationRate=0.0,
                                    typeProsociality=ProsocialityType.weak, tWriteCSV=False, toPrintDataVecs=True, 
                                    fileName='testData.csv')
    simulator.runEvolutionarySimulation()
