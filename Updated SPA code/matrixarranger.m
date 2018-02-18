function [r] = matrixarranger(a)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
c=1;
for i = 1:82
  for j = 1:82
      r(i,j) = a(c);
      c=c+1;
  end
end
end

