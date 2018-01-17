function[res] = uncertainty(t1,t2,sa,sb)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
term1 = 0;
for i = 1:387
    if(i<=387)
    term1 = term1+(t1(i)*t1(i))*(sb(i)^2);
    end
  
end
        
        
term2 = 0;
for i = 1:387
for j = 1:387
   if(j<=387)
   term2 = term2+((t2(i)*t1(j))^2)*(sa(i,j)^2);
  end
end
end
res = sqrt(term2+term1);
end

