function [] = spa_print2()
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
    global fileID;
    global fileID2;
   c2=1;
    global nans;
    sum1=0;
    fprintf(fileID2,'%f  %d    zero order       %f   \r\n',fvres2,sector,fvres2/total*100);
   
   for i=length(res2):-1:1
   %for i = 1:length(res2)
       crct3=999;
      if(res2(i)~=0)          
         if((res2(i)>th)) 
                           if(mod(node_no(i),s)==0)
                               crct1=s;
                           else
                               crct1 = mod(node_no(i),s);
                           end
                           if(mod(((node_no(i)-crct1)/s),s)==0)
                               crct2 = s;
                           else
                               crct2 = mod(((node_no(i)-crct1)/s),s);
                           end
                           if(mod(((((node_no(i)-crct1)/s)-crct2)/s),s)==0)
                               crct3 = s;
                           else
                               crct3 = mod(((((node_no(i)-crct1)/s)-crct2)/s),s);                                  
                           end
                           if(mod(((((((node_no(i)-crct1)/s)-crct2)/s)-crct3)/s),s)==0)
                               crct4 = s;
                           else
                               crct4 = mod(((((((node_no(i)-crct1)/s)-crct2)/s)-crct3)/s),s); 
                           end
                           if(mod(((((((((node_no(i)-crct1)/s)-crct2)/s)-crct3)/s)-crct4)/s),s)==0)
                               crct5 = s;
                           else
                               crct5 = mod(((((((((node_no(i)-crct1)/s)-crct2)/s)-crct3)/s)-crct4)/s),s); 
                           end
                                  
                              
                           
             
             
            if(node_no(i) <= (s^2-1)/(s-1)-1) 
                  fprintf(fileID2,'%f  %d----%d   first order %f   \r\n',res2(i),crct1,sector,res2(i)/total*100);
                 % fprintf(fileID2,'\n');
            else if(node_no(i)<= ((s^3)-1)/(s-1)-1)           
                  fprintf(fileID2,'%f   %d----%d----%d    second order   %f    \r\n',res2(i),crct1,crct2,sector,res2(i)/total*100);   
                  %fprintf(fileID2,'%d %d\r\n',node_no(i),p(i)); 
                  %fprintf(fileID2,'\n');
            else if(node_no(i)<=((s^4)-1)/(s-1)-1)
                  fprintf(fileID2,'%f   %d----%d----%d----%d    third order   %f     \r\n',res2(i),crct1,crct2,crct3,sector,res2(i)/total*100); 
          % fprintf(fileID2,'%d %d\r\n',node_no(i),p(i)); 
                else if(node_no(i)<=((s^5)-1)/(s-1)-1)
                    fprintf(fileID2,'%f   %d----%d----%d----%d-----%d    fourth order   %f   \r\n',res2(i),crct1,crct2,crct3,crct4,sector,res2(i)/total*100); 
                %  fprintf(fileID2,'%d %d\r\n',node_no(i),p(i)); 
                    else
                      %disp('Tapa');
                    fprintf(fileID2,'%f   %d----%d----%d----%d----%d----%d    fifth order   %f   \r\n',res2(i),crct1,crct2,crct3,crct4,crct5,sector,res2(i)/total*100);   
                    end
                 
                  
                  % fprintf(fileID2,'\n');
           % else if(node_no(i)<=((s^5)-1)/(s-1)-1)
                  %fprintf(fileID2,'%f   %d----%d----%d----%d-----0    fourth order   %f   \r\n',res2(i),mod(node_no(i),s),mod((node_no(i)-p(i))/s,s),(mod((node_no(i)-p(i))/s/s,s)),floor((node_no(i)-p(i))/s/s/s),res2(i)/total*100);    
               % else
                  %fprintf(fileID2,'%f   %d----%d----%d----%d-----%d-----0    fifth order   %f   \r\n',res2(i),mod(node_no(i),s),mod((node_no(i)-p(i))/s,s),(mod((node_no(i)-p(i))/s/s,s)),(mod((node_no(i)-p(i))/s/s/s,s)),floor((node_no(i)-p(i))/s/s/s/s),res2(i)/total*100);   
                  % fprintf(fileID2,'\n');
                end 
                end
            end
            nans(c2)=mod(node_no(i),s);c2=c2+1;
         end
      end


    end

%clearvars -global res res2 p p1 node_no    
end
      
                
