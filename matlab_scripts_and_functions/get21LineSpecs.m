function lineSpecs = get21LineSpecs()
% Name: get21LineSpecs
% Description: returns cell array of 21 unique line specificiations, all 
%   dashed lines with three different marker choices and 7 different color
%   choices
% Format of call: get21LineSpecs()
% Inputs: none
% Output: cell array of line specs
% William Edgecomb, Spring 2017
% Project: Multilevel_Selection_Simulations
% Course: COSI 210a, Independent study with Professor Jordan Pollack
    
    markers = {'o','s','^'};
    colors = {'y','m','c','r','g','b','k'};
    numColors = size(colors,2);
    
    lineSpecs = cell(1,numColors*3);
    
    % creates 21 line varieties by combining elements from cell arrays
    % markers and colors in all possible ways. All lines are dashed lines
    for i = 1:(3*numColors)
        markersIndex = mod(i,3)+1;
        colorsIndex = mod(i,7)+1;
        lineSpecs{i} =  strcat('--', colors{colorsIndex},markers{markersIndex});    
    end
