'''
Module description: 
    module for defining migration behavior. Includes an Enum for specifying different
    types of migration, and associated custom migration methods, which are designed to
    be called in the method _migrationPhase of simulatation.evo_simulator.EvolutionSimulator 
    
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from enum import Enum
from random import shuffle

class MigrationType(Enum):
    
    '''
    Instances of evo_simulator.EvolutionSimulator are each associated with a type of migration.
    With randomRedistribution, all individuals in population are randomly reshuffled into new groups
    after every round of the life cycle. With phenotypeStratisfied, at each round individuals are reassigned 
    to groups such that groups tend to have a preponderance either of prosocial individuals, or a preponderance
    of selfish individuals. With totalIsolation, individuals never migrate from the group in which they are
    initially assigned or born into. The total isolation condition serves as a control to test the effect
    that migration has on the outcome of an evolutionary simulatation.
    '''
    
    totalRandomRedistribution = 0
    phenotypeStratified = 1
    totalIsolation = 2
    
def randomRedistribution(self):
    
    '''executes phase of migration such that all individuals are pooled together and then randomly 
    assigned to new groups'''
    
    self._mergeGroups()
    self._resetGroupsBeforeReassignment()
    self._assignToGroupsRandomly(self.allIndividuals)
        
def biasedRedistribution(self):
    
    '''executes phase of migration such that the groups resulting from migration will tend to have
    either mostly prosocial individuals or mostly selfish individuals'''
    
    def _assignToGroupsBiased(individuals):
        
        '''assigns individuals to groups, biasing assignment of an individual toward a group
        that has a high proportion of individuals of that individual's phenotype'''
        
        # shuffles population of all individuals to randomize order
        shuffle(individuals)
       
        '''assign individuals to groups. Basic idea is to cycle through groups two at a time, while
        also popping two individuals at a time from list. If one individual is prosocial while
        the other is selfish, the prosocial individual is assigned to the group with more prosocial 
        individuals and vice-versa for the selfish individual. Otherwise, if the two individuals
        have the same phenotype, then each is simply assigned to group.'''
                
        while len(individuals) > 0:
            if len(self.groups) > 1:
                for groupIndex in range(0, (len(self.groups) - 1), 2):
                    if len(individuals) > 1 and not len(self.groups) == 1:
                        group1 = self.groups[groupIndex]
                        group2 = self.groups[groupIndex + 1]
                        individ1 = individuals.pop()
                        individ2 = individuals.pop()
                        if individ1.phenotype == individ2.phenotype:
                            group1.addMember(individ1)
                            group2.addMember(individ2)
                        else:
                            if individ1.phenotype == self.prosocialPhenotype:
                                individA = individ1 
                                individS = individ2
                            else:
                                individA = individ2 
                                individS = individ1               
                            
                            try:
                                if group1.proportionProsocial() > group2.proportionProsocial():
                                    group1.addMember(individA)
                                    group2.addMember(individS)
                                else:
                                    group1.addMember(individS)
                                    group2.addMember(individA)
                            
                            except(ZeroDivisionError):
                                if group1.countProsocial == 0:
                                    group2.addMember(individA)
                                    group1.addMember(individS)
                                else:
                                    group1.addMember(individA)
                                    group2.addMember(individS)
                    elif len(individuals) == 1 or len(self.groups) == 1:
                        self.groups[groupIndex].addMember(individuals.pop())
            elif len(self.groups) == 1:
                self.groups[0].addMember(individuals.pop())
        
    self._mergeGroups()
    self._resetGroupsBeforeReassignment()
    _assignToGroupsBiased(self.allIndividuals)
    
def totalIsolation(self):
    
    '''no migration between groups, so simply pass'''
    
    pass

def getMigrationFunctionKey(migrationFunction):
    
    '''returns numeric key associated with migration function'''
    
    if migrationFunction == randomRedistribution:
        return 0
    elif migrationFunction == biasedRedistribution:
        return 1
    elif migrationFunction == totalIsolation:
        return 2
    else:
        raise RuntimeError("migration function not found among options implemented")
         
    