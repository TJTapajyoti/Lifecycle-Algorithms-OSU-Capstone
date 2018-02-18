function [] = runprog(sec1,tot1,a1,m1,nsec)
%UNTITLED8 Summary of this function goes here
%   Detailed explanation goes here
clc;
  clearvars -except a m a1 m1 sec1 tot1 fileID i nsec;
    global res;
    global res2; 
    global node_no;
    global p;
    global p1;
    global fv;
    global th;
    global d;
    global v;    
    global cc;
    global s;
    global sector;
    global total;
    global fvres2;
    global fvp;
    global fvp1;
    global fvnodeno;
    global counter;
    global a;
    global m;
    global c2;
    a = a1;
    m = m1;
    global fileID;
    global fileID2;
    global nans;
    fileID = fopen('myfile3.txt','w');
        fileID2 = fopen('myfile4.txt','w');

    for i = 1:1
        clearvars -global res res2;
        res = zeros(1);
res2 = zeros(1);
p = zeros(1);
p1 = zeros(1);
node_no = zeros(1);
         fvres2=0;
    fvp=0;
    fvp1=0;
     fvnodeno=0;

        clearvars -except a m a1 m1 sec1 tot1 fileID fileID2 i c2 nans nsec;
        fprintf(fileID2,' \r\n %d           \r\n',sec1);
        mainspa(sec1,tot1,nsec);
         fprintf(fileID,'           \r\n');
         clearvars -except a m a1 m1 sec1 tot1 fileID fileID2 c2 nans i nsec;
        
    end    
end

