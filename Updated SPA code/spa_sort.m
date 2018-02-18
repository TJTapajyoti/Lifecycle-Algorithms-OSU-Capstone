function [] = spa_sort(left,right)
    global res;
    global res2; 
    global node_no;
    global p;
    global fv;
    global th;
    global s;
    global sector;
    global total;
    global fvres2;
    global fvp;
    global fvp1;
    global fvnodeno;
    global a;
    global m;
    global p1;

       i = left; j = right;
       if(mod((left + right),2)==0)
                  pivot = res2((left + right)/2);
                  
       else
           pivot = res2((left + right+1)/2); 
       end
 
       while (i <= j)  
            while (res2(i) < pivot)
                  i=i+1;
            end
            while (res2(j) > pivot)
                  j=j-1;
            end
            if (i <= j)  
                                    temp1 = res2(i);
                                    temp2 = node_no(i);
                                    temp3 = p(i);
 
                                    res2(i) = res2(j);
                                    node_no(i) = node_no(j);
                                    p(i)=p(j);
 
                                    res2(j) = temp1;
                                    node_no(j) = temp2;
                                    p(j)=temp3;
                  i=i+1;
                  j=j-1;
            end
      end
 
      %/* recursion */
      if (left < j)
            spa_sort(left, j);
      end
      if (i < right)
            spa_sort(i, right);
      end
end

