% Script description: 
%   makes several plots to visualize the results of experiment 5    
    
% Created: Spring 2017

% Project: Multilevel_Selection_Simulations
% Course: COSI 210a, Independent study with Professor Jordan Pollack

clear

% read all data from experiment into matrix, omitting row and column
% headings
simulationData = csvread('experiment5_random_redistribution.csv', 1, 1);
% makes plots--see function for description of parameters
plotExperiments4Through6(simulationData, 18, 11, 'altruistic')


