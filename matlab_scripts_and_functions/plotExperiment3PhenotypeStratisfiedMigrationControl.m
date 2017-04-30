% Script description: 
%   makes several plots to visualize the results of experiment 3    
    
% Created: Spring 2017

% Project: Multilevel_Selection_Simulations
% Course: COSI 210a, Independent study with Professor Jordan Pollack

clear

% read all data from experiment into matrix, omitting row and column
% headings
simulationData = csvread('experiment3_phenotype_stratisfied_migration_control.csv', 1, 1);
% makes plots--see function for description of parameters
plotExperiments1Through3(simulationData, 18, 11)

