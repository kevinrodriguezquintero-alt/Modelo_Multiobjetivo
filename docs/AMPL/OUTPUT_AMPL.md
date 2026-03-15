ampl: model 'C:\Users\kevin\OneDrive\Escritorio\Modelo.mod';
ampl: data 'C:\Users\kevin\OneDrive\Escritorio\Datos.dat';
ampl: option solver cplex;
ampl: solve;
CPLEX 22.1.1.0: optimal integer solution; objective 196114857.7
25 MIP simplex iterations
0 branch-and-bound nodes
ampl: printf "\n\n*************************************\n";
printf "RESULTADOS DEL PROBLEMA \n";
printf "*************************************\n\n";

printf "\nCOSTO  = \t%9.1f", costo;

printf "\n\nCantidad de producto a enviar del produtor al intermediario =\n\n";
display X;

printf "\nCantidad de producto a enviar del intermediario al detallista =\n\n";
display Y;

printf "\nNumero de viajes del productor al intermediario =\n\n";
display Z;

printf "\nNumero de viajes del intermediario al detallista =\n\n";
display ZZ;

printf "\nCantidad de Hectareas =\n\n";
display W;

printf "\nNunmero de personas a contratar en el intermediario  =\n\n";
display S;

printf "\nNunmero de personas a contratar en el detallista  =\n\n";
display SS;

printf "\nVariable binaria 1 si se abre el productor  =\n\n";
display B;

*************************************
ampl: RESULTADOS DEL PROBLEMA 
ampl: *************************************

ampl: 
COSTO  = 	196114857.7ampl: 

Cantidad de producto a enviar del produtor al intermediario =

X :=
1 1   1100
1 2    850
1 3    713
1 4   4500
1 5   3009
1 6   5340
1 7   1290
;

ampl: 
Cantidad de producto a enviar del intermediario al detallista =

ampl: Y [*,*]
:      1          2        3        4        :=
1      0          0          0   1147.83
2    158.471      0          0    658.204
3      0          0          0    713
4      0       3896.91       0      0
5      0          0          0   3071.69
6   2831.53     163.093   1080   1104.95
7      0          0          0   1304.33
;

ampl: 
Numero de viajes del productor al intermediario =

Z :=
1 1   1
1 2   1
1 3   1
1 4   2
1 5   4
1 6   6
1 7   2
;

ampl: 
Numero de viajes del intermediario al detallista =

ampl: ZZ [*,*]
:   1   2   3   4    :=
1   1   0   0   0
2   1   0   0   0
3   1   0   0   0
4   1   0   0   0
5   4   0   0   0
6   6   0   0   0
7   2   0   0   0
;

ampl: 
Cantidad de Hectareas =

W [*] :=
1  50.7
;

ampl: ampl: 
Nunmero de personas a contratar en el intermediario  =

ampl: S [*] :=
1   55
2   34
3   31
4  250
5  177
6  267
7   43
;

ampl: 
Nunmero de personas a contratar en el detallista  =

ampl: SS [*] :=
1  23
2  29
3   9
4  80
;

ampl: ampl: 
Variable binaria 1 si se abre el productor  =