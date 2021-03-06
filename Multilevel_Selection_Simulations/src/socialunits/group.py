'''
Module description: defines a single custom class, SocialGroup
Created: Spring 2017

Project: Multilevel_Selection_Simulations
Course: COSI 210a, Independent study with Professor Jordan Pollack

@author: William Edgecomb
'''

from enums import Phenotype, ReproductionType, ProsocialityType
from random import randint, choice
from individual import Individual

class SocialGroup():
    
    '''
    Description: collective social unit, members of type socialunits.individual.Individual.
        Life cycle operations including within-group interactions, calls to Individual's 
        attemptReproduction function, and death are managed by this class. The functionality 
        of these operations is designed to be customizable by overriding the appropriate private
        functions (i.e. _playSocialGameAsexual, _playSocialGameSexual, _deathAndReproductionAsexual,
        _deathAndReproductionSexual).
       
    Instance variables: 
    # self.reproduction: member of socialunits.enums.ReproductionType (sexual or asexual)
    # self.members: list of individuals comprising social group
    # self.countProsocial: count of individuals in group with prosocial (altruistic or reciprocating) phenotype
    # self.countSelfish: count of individuals in group with selfish phenotpye
        
    Constructor method signature: __init__(self, reproduction)
    
    Public methods:
    # size(): returns number of individuals in group
    # addMember(member): adds new individual to group
    # addMember(member): adds iterable of new individuals to group
    # proportionProsocial(): returns proportion of prosocial individuals in group, a real value 
        in range [0,1]
    # playSocialGame(**kwargs): executes a social game in which group members interact
    # deathAndReproduction(**kwargs): manages death and reproduction of group members 
    '''
    
    def __init__(self, reproduction):
        
        '''
        Parameters:
        # reproduction: member of socialunits.enums.ReproductionType (sexual or asexual)
        
        Errors:
        # TypeError: raised if reproduction or genotype is not of proper enum
        '''
        
        if not isinstance(reproduction, ReproductionType):
            raise TypeError('reproduction must be of type socialunits.enums.ReproductionType')
        
        self.reproduction = reproduction
        self.members = [] 
        self.countProsocial = 0
        self.countSelfish = 0
    
    def size(self):
        
        '''Returns number of individuals in group''' 
        
        return len(self.members)
    
    def addMember(self, newMember):
        
        '''
        Description: adds an individual to group by appending to self.members. Increments
            count of prosocial individuals
        
        Parameters:
        # newMember: instance of type socialunits.individual.Individual to be added
        
        Errors:
        # TypeError: raised if individual's phenotype not of type socialunits.enums.Phenotype
        
        Warnings: generic warning raised if newMember not of type Individual, or
            if individual's reproduction type does not match that of the group. In 
            either case the inputted item will not be added to self.members
        '''
        
        if isinstance(newMember, Individual):
            if not newMember.reproduction == self.reproduction:
                raise Warning('cannot add individual with reproduction type not matching that of group...item not added')
                return
            self.members.append(newMember)
            if newMember.phenotype != Phenotype.selfish:
                self.countProsocial += 1
            elif newMember.phenotype == Phenotype.selfish:
                self.countSelfish += 1
            else:
                raise TypeError('newMember\'s phenotype must be of type socialunits.enums.Phenotype')
        else:
            raise Warning('can only add items of type socialunits.individual.Individual to SocialGroup...item not added')
        

    def addMembers(self, newMembers):
        
        '''
        Description: adds an iterable of instances of class socialunits.individual.Individual 
            to group by calling addMember for each individual in iterable. Errors/warnings
            may be raised by addMember
        
        Errors:
        # TypeError: raised if an individual's phenotype not of type socialunits.enums.Phenotype
        
        Warnings: generic warning raised if an item in list is not of type Individual, or
            if the individual's reproduction type does not match that of the group. In 
            either case that item will not be added.
        
        '''
        
        for member in newMembers:
            self.addMember(member)
    
    def proportionProsocial(self):
        
        '''
        Returns: proportion of prosocial individuals in population, a real number in range [0,1]
        
        Errors:
         # ZeroDivisionError: raised if population size of group is zero
        '''
        
        return self.countProsocial / float(self.size())
            
   
    
    def playSocialGame(self, **kwargs):
        
        '''
        Description, generally: 
            plays a social game between group members. This is a wrapper method that
            calls a different private subsidary method--_playGameAsexual or _playGameSexual depending 
            on group's reproduction type. It is recommended that one override these subsidiary methods 
            to change the behavior of playSocialGame. 
            
            Broadly, the intent is that during playSocialGame members of the group will have interactions
            that are governed by the respective members' phenotypes. In a paradigmatic case, altruists
            will distribute benefits to other members of the group at some cost to themselves.
            The costs and benefits will then be cashed out during the death and reproduction phase of the
            life cycle, managed by method deathAndReproduction.
        
        Description, default implementation of _playGameAsexual: 
            Each member of the group plays one turn. If of the selfish phenotype, no action is taken.
            If of the altruistic phenotype, a member of the group is randomly selected and is granted 
            one additional reproduction opportunity (Individual.extraReproductionChances += 1). If of the
            reciprocating phenotype, a member of the group is randomly selected and if that member is also
            of the reciprocating phenotype, then that other member is granted one additional reproduction
            opportunity. If keyword argument prosocialityType has value socialunits.enums.ProsocialityType.strong, 
            then the prosocial individual currently playing will be excluded from the group of potential beneficiaries. 
            Otherwise if prosocialityType has the value soialunits.enums.ProsocialityType.weak, the currently playing 
            prosocial individual is a potential beneficiary. Regardless of prosociality type, the prosocial individual
            will incur a cost by adding value of keyword argument costOfProsociality to 
            Individual.prosocialityCostIncurred. This social game, and the accompanying default behavior of 
            deathAndReproduction, is adapted from a model presented in "Unto Others: The Evolution and Psychology of 
            Unselfish Behavior" by Elliott Sober and David Sloan Wilson, London: Harvard University Press, 1998, pg 19-21.
            
        Description, default implementation of _playGameSexual:
            --not yet implemented--
        
        Parameters, generally:
            # **kwargs: key words args are used to provide maximum flexibility
                
        Keyword args, default implementation of _playGameAsexual:
            # prosocialityType: of type socialunits.enums.ProsocialityType (strong or weak). In strong prosociality
                prosocial individuals are potential beneficiaries of their own beneficence (although the 
                expected benefit from one's own prosociality should outweigh the expected cost) 
            # costOfProsociality: cost incurred by each prosocial individual. Value is added to 
                Individual.ProsocialityCostIncurred, diminishing reproductive potential in death and 
                reproduction phase
                
        Keyword args, default implementation of _playGameSexual:
            --not yet implemented--
        
        Errors:
        # TypeError: raised if prosocialityType not of type socialunits.enums.ProsocialityType 
        '''
        
        if self.reproduction == ReproductionType.asexual:
            self._playGameAsexual(**kwargs)
        elif self.reproduction == ReproductionType.sexual:
            self._playGameSexual(**kwargs)
    
    def _playGameAsexual(self, **kwargs):
        
        '''subsidiary method of playSocialGame. Called for asexually reproducing group'''
        
        typeProsociality = kwargs['typeProsociality']
        if not isinstance(typeProsociality, ProsocialityType):
            raise TypeError('typeProsociality must of type socialunits.enums.ProsocialityType') 
        # every member plays once, except if group has less than 2 members, in which case no one plays
        if self.size() > 1:
            for memberIndex, member in enumerate(self.members):
                if member.phenotype == Phenotype.altruistic:                
                    beneficiary = (self._randomOther(memberIndex) if typeProsociality == ProsocialityType.strong
                                   else choice(self.members))
                    beneficiary.extraReproductionChances += 1                    
                    member.prosocialCostIncurred += kwargs['costOfProsociality']
                # selfish members do not act in this game
                elif member.phenotype == Phenotype.selfish:
                    pass
                elif member.phenotype == Phenotype.reciprocating:
                    beneficiary = (self._randomOther(memberIndex) if typeProsociality == ProsocialityType.strong
                                  else choice(self.members)) 
                    if beneficiary.phenotype == Phenotype.reciprocating:
                        beneficiary.extraReproductionChances += 1
                        member.prosocialCostIncurred += kwargs['costOfProsociality']
            
    def _randomOther(self, memberIndex):
        
        '''selects and returns a random individual from members excluding individual at memberIndex'''
        
        # randomIndex gets the index of a randomly selected groupmate
        randomIndex = randint(0, self.size() - 2)
        # index adjusted to disallow selection of one's own index
        if randomIndex >= memberIndex:
            randomIndex += 1
        return self.members[randomIndex]

    def _playGameSexual(self):
        
        '''subsidiary method of playSocialGame. Called for sexually reproducing group'''
        
        raise RuntimeError('sexual reproduction not yet implemented')
    
    def deathAndReproduction(self, **kwargs):
        
        '''
        Description, generally: 
            Executes a round a death and reproduction for the group. This is a wrapper method that
            calls a different private subsidary method--_deathAndReproductionAsexual or 
            _deathAndReproductionSexual depending on group's reproduction type. It is recommended 
            that one override these subsidiary methods to change the behavior of deathAndReproduction. 
            
            Broadly, the intent is that during deathAndReproduction, some members of the group will 
            attempt to reproduce, and others will perish. Hence individuals will be added and removed
            from self.members. Furthermore, the outcome of playSocialGame, which is intended to affect
            instance variables of the Individual class, should influence the outcome of deathAndReproduction,
            e.g. by reducing the reproduction potential of prosocial individuals.
        
        Description, default implementation of _deathAndReproductionAsexual: 
            Each member of the group takes a turn attempting reproduction. Each member has 
            baseReproductionChances to produce +1 offspring at baseReproductionProbability minus 
            prosocialCostIncurred probability, and then member.extraReproductionChances to produce
            +1 offspring at the probability of extraReproductionProbability each time. ALl produced progeny
            are collected into a list, and then entirely supplant the parent generation. Thus all parents
            perish in this default implementation.
            
        Description, default implementation of _playGameSexual:
            --not yet implemented--
        
        Parameters, generally:
            # **kwargs: key words args are used to provide maximum flexibility
                
        Keyword args, default implementation of _deathAndReproductionAsexual:
            # baseReproductionChances: the number of chances at producing +1 offspring each individual is 
                guaranteed 
            # baseReproductionProbability: base probability of producing +1 offspring for each chance to 
                reproduce in baseReproductionChances. Value is modulated by Individual.costOfProsociality, the 
                cost incurred by the individual as the result of prosocial behavior (will be zero selfish
                types)
            # extraReproductionProbability: probability of producing +1 offspring for each chance to 
                reproduce in instance variable extraReproductionChances of Individual class.
                
        Keyword args, default implementation of _deathAndReproductionSexual:
            --not yet implemented--
        '''
        
        if self.reproduction == ReproductionType.asexual:
            self._deathAndReproductionAsexual(**kwargs)
        elif self.reproduction == ReproductionType.sexual:
            self._deathAndReproductionSexual(**kwargs)
    
    def _deathAndReproductionAsexual(self, **kwargs):
        
        '''subsidiary method of deathAndReproduction. Called for asexually reproducing group'''
        
        allProgeny = SocialGroup(self.reproduction)
        for member in self.members:
            for _ in range(kwargs['baseReproductionChances']):
                newProgeny = member.attemptReproduction(kwargs['baseReproductionProbability'] - member.prosocialCostIncurred)
                if not newProgeny == None:
                    allProgeny.addMember(newProgeny)
            for _ in range(member.extraReproductionChances):
                newProgeny = member.attemptReproduction(kwargs['extraReproductionProbability'])
                if not newProgeny == None:
                    allProgeny.addMember(newProgeny)
        
        '''copy all essential instance variables from allProgeny to self. In this way the 
           death of the entire parent generation is implicit'''
        self._supplantGroup(allProgeny)
        
    def _supplantGroup(self, supplantingGroup):
        
        '''
        Description: for other group of same reproduction type, replaces essential 
            instance variables of self with that of other group. This is useful for 
            replacing current generation of group members with a group of progeny
            
        Parameters: 
        # supplantingGroup, an instance of Social Group
        
        Errors: 
        # Type Error: raised if supplantingGroup not of type SocialGroup
        # RuntimeError: raised if supplanting group has reproduction type
            that differs from that of self
        '''
        
        if not (isinstance(supplantingGroup, SocialGroup)):
            raise TypeError('can only supplant with instance of type SocialGroup')
        if not supplantingGroup.reproduction == self.reproduction:
            raise RuntimeError('can only supplant with group that has same value for self.reproduction')
        
        self.members = supplantingGroup.members
        self.countProsocial = supplantingGroup.countProsocial
        self.countSelfish = supplantingGroup.countSelfish
        
    def _deathAndReproductionSexual(self):
        
        '''subsidiary method of deathAndReproduction. Called for sexually reproducing group'''
        raise RuntimeError('Sexual Reproduction not yet implemented')
