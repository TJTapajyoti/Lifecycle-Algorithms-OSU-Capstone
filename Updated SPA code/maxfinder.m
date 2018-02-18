function [ temp ] = maxfinder(m)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
global s;
temp = 0;    
for i=1:s
    if(m(i)> temp)   
        temp = m(i);
    end
end


