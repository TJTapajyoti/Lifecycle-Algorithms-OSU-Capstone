function [] = spa_print()
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
   c2=1;
    global nans;
    global list1;
    global list2;
    sum1=0;
    x= sym('%'); 
    x = char(x);
    list1 = zeros(1);
    list2 = zeros(1);
    %fprintf(fileID,'%d   %d----%d    zero order       %f %s   \n',fvres2,mod(fvnodeno,s),(fvp-fvnodeno),fvres2/total*100);
    fprintf(fileID,'\n');
    for i=length(res2):-1:1
      if(res2(i)~=0)
         if((res2(i)>th))              
            if(node_no(i) <= (s^2-1)/(s-1)-1) 
                  fprintf(fileID,'%d %s   %d\r\n',mod(node_no(i),s),res2(i));
                  fprintf(fileID,'\r\n');
                  list1(c2)=mod(node_no(i),s);
                  list2(c2)=res2(i);  c2=c2+1;             
           else if(node_no(i)<= ((s^3)-1)/(s-1)-1)           
                  fprintf(fileID,'%d %s    %d\r\n',mod(node_no(i),s),res2(i));   
                  fprintf(fileID,'\r\n');
                  list1(c2)=mod(node_no(i),s);
                  list2(c2)=res2(i); c2=c2+1;
            else if(node_no(i)<=((s^4)-1)/(s-1)-1)
                  fprintf(fileID,'%d %s   %d\r\n',mod(node_no(i),s),res2(i)); 
                  fprintf(fileID,'\r\n');
                  list1(c2)=mod(node_no(i),s);
                  list2(c2)=res2(i); c2=c2+1;
            else if(node_no(i)<=((s^5)-1)/(s-1)-1)
                  fprintf(fileID,'%d %s   %d\r\n',mod(node_no(i),s),res2(i));    
                  fprintf(fileID,'\r\n');
                  list1(c2)=mod(node_no(i),s);
                  list2(c2)=res2(i);  c2=c2+1;
                else
                list1(c2)=mod(node_no(i),s);
                list2(c2)=res2(i);  c2=c2+1;
               %disp('Tapa');   
                       end 
                   end
                end
            end 
         end
      end
    end
    c2 =c2-1;
fileID3 = fopen('myfile5.txt','w');
for i=length(res2):-1:1
    sum1=sum1+res2(i);
    end
disp(sum1+fvres2);

for i=1:s
    sum2=0;
    for j = 1:c2
        if(i==list1(j))
            sum2=sum2+list2(j);
        end
    end
         fprintf(fileID3,'%d   %d\r\n',i,sum2);      
    
    
end
      
                
