function [XAA] = mainspa(sec,tot,nsec)
clc;
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
    global a;
    global m;
    f = 1;
    v=1;
    s=nsec;   
    sector = sec;
    total = tot;
    th = 0.0005;
    fvp=sec;
    fvp1=0;
    fvnodeno=0;
    fv=f;
    fvres2=f*m(sec);
    spa_calc();
    spa_sort(1,length(res2));
    spa_print();
    spa_print2();
    %XAA = spa_buildmatrix();
   
    end

