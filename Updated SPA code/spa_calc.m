function [] = spa_calc()
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
    cc = 0;
    v=1;
    d=0;
    for l = 0:20000
    if(l==0)%calculation for the first parent level
          for i = 1:s                
              if(a(i,sector)*fv*maxfinder(m)>th)
                    res(s*l+i-cc) = a(i,sector)*fv;%calculation of path value
                    node_no(s*l+i-cc)=s*fvp1+i;
                    res2(s*l+i-cc) = res(s*l+i-cc)*m(i);%//calculation of path value for the EEIO model
                    p(s*l+i-cc)=i;%//calculation of the node number
                    p1(v)=s*fvp1+i;                   
                    v=v+1;           
                 
               else                 
                  cc=cc+1;               
               end
           end
        
    else%//calculation for all other parent levels        
       for i = 1:s 
          if(mod(p1(d),s)==0)             
                if((a(i,s)*res(l))*maxfinder(m)>th)
                    res(s*l+i-cc) = a(i,s)*res(l);
                    node_no(s*l+i-cc)=s*p1(d)+i; 
                    res2(s*l+i-cc) = res(s*l+i-cc)*m(i);
                    p(s*l+i-cc)=i;
                    p1(v)=s*p1(d)+i;
                    v=v+1;        
                else
                   cc=cc+1;
                end            
          else
                    if((a(i,mod(p1(d),s))*res(l))*maxfinder(m)>th)                          
                    res(s*l+i-cc) = a(i,mod(p1(d),s))*res(l);
                    node_no(s*l+i-cc)=s*p1(d)+i; 
                    res2(s*l+i-cc) = res(s*l+i-cc)*m(i);
                    p(s*l+i-cc)=i;
                    p1(v)=s*p1(d)+i;
                    v=v+1;
            else
                     
                    cc=cc+1;
            end
         end
      end
    end
          
 d = d+1;
  if(d==v)
     break;
  end 
end
 

