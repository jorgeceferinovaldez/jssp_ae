program evoSocial;
{se genera cada poblaci¢na partir de un individuo bueno denominado Queen y otros}
{individuos que son generados aleatoriamente}
{cada individuo aleatoria se recombina con Queen y el mejor de sus hijos se guarda}
{luego de popsize iteraciones, si el mejor hijo mejora a Queen, entonces pasa a ser el nuevo Queen}
{para la siguiente iteraci¢n}

Uses
   crt, varglo, report, estadis, utility, crossvs, op_mut;

PROCEDURE setup;
BEGIN
     read(datos,cantcorr);
     read(datos,pmutacion);
     read(datos,pcross);
     read(datos,maxgen);
     read(datos,popsize);
END;
(*-------------------------------------------------------------*)


(*----------------------------------Modelo de Costo --------------------------*)
FUNCTION modelo_costo(N : INTEGER):REAL;
VAR
   costo : REAL;
BEGIN
     costo := COSTOgy*N*(2/3+((1/3)*EXP(-0.00174*N*N)));
     modelo_costo := costo;
END;
(*----------------------------------------------------------------------------*)

(*---------------------------------------InicPesos ----------------------------*)
procedure InicPesos (var cmj:TipoMaqJob);
{Inicializa la lista de jobs con los tiempos correspondientes a cada maquina}
var
 i,j, val: integer;
begin
Reset(Ins);
readln(Ins,upperb);
readln(Ins,lowerb);
for i:=1 to maxmaq do
     begin
     for j:=1 to maxcrom do
         begin
         read(Ins,val);
         cmj[i,j] := val;
         end;
    end;
close(Ins);
end;


(************************genScheduler************************************************)
procedure genScheduler(vdec: cromosoma; cmj: tipoMaqJob; var objective: real; var fitness: real);
type
    tipoPos = array [1..maxMaq, 1..maxcrom] of integer;
var
  i,j, ult,k, indice : integer;
  Pos : tipoPos;

begin
{inicializa la matriz de ultima posicion del job en el scheduler}
for i := 1 to maxmaq do
    for j := 1 to maxcrom do
        pos[i,j] := 0;

{asigna a la primera maquina el scheduler del job}
ult := 0;
for i:= 1 to maxcrom do
    begin
    indice := vdec[i];
    if i=1
       then pos[1,i] := cmj[1,indice]
       else pos[1,i] := pos[1,i-1]+cmj[1,indice];
   end;
   {asigna a las siguientes maquinas el scheduler del job}
   for j:= 2 to maxmaq do
       for i:= 1 to maxcrom do
        begin
        ult := pos[j-1,i];
        indice := vdec[i];
        if (i-1 <> 0) and ( pos[j,i-1] >= ult)
           then ult := pos[j,i-1] + cmj[j,indice]
           else ult := ult + cmj[j,indice];
        pos[j,i]:= ult;
        end;
objective := ult;
fitness := 1/objective;
end;

PROCEDURE evalua(var child:hijos;ch:integer);
var
   i:integer;

begin
for i:= 1 to ch do
    genScheduler(child[i].cromosoma, cmj, child[i].objective,child[i].fitness);
end;



PROCEDURE indAleatorio (var ri: individuo);
{ Genera un individuo aleatorio }

VAR
 j,job: integer;
 C: tipoconj;
 auxcrom:cromosoma;

BEGIN
  WITH ri do  (* generar individuo permutacion *)
      BEGIN
      c:= [ ];
      FOR  j := 1 TO maxcrom DO
          BEGIN
             REPEAT
                job := rnd(1,maxcrom);
             UNTIL NOT(job in C);
             C := C + [job];
             cromosoma[j] := job;
          END;
      IF not validacrom(cromosoma) THEN
         BEGIN
          writeln(' cromosoma invalido en initpop');
          for j:= 1 to maxcrom do
              write(cromosoma[j],' ');
         halt
         END;

      { evaluar }
      genScheduler(cromosoma, cmj, objective, fitness);
       END;  (* With oldpop *)
END;  { indAleatorio }



PROCEDURE NEXT_GENERACION;

VAR
    j, i, k, nroch, mejor: integer;
    sumobjective:real;
    ri : individuo; {ri: random inmigrante, mej: mejor individuo}

BEGIN

  maximo:=0;
  min:= upperb * 10.5;
  sumobjective:= 0;

  j := 0; { primer individuo de la poblacion actual }
  REPEAT
       indchild:=0;
       indAleatorio (ri);
       { realiza crossover OX2}
       if flip(pcross)
         then begin
              crossox(queen.cromosoma, ri.cromosoma);
              evalua(child, 2);
              {elijo el mejor}
              if child[1].objective < child[2].objective
                 then mejor := 1
                 else mejor := 2;
              mej:=child[mejor];

              end {end flip cross}
         else begin

               IF flip(pmutacion) THEN
                    BEGIN
                        mutshift(queen.cromosoma);
                        genScheduler(queen.cromosoma, cmj, queen.objective, queen.fitness);

                    END;
               IF flip(pmutacion) THEN
                       BEGIN
                           mutshift(ri.cromosoma);
                           genScheduler(ri.cromosoma, cmj, ri.objective, ri.fitness);
                       END;

              {elijo el mejor}
              if ri.objective< queen.objective
                 then mej := ri
                 else mej := queen;

             end;

             stats(mej);
             sumobjective:= sumobjective + mej.objective;

             j:= j+ 1;

    UNTIL j > popsize;
    avg := sumobjective/popsize; (* fitness promedio poblacional *)

end;    { NEXT GENERATION }





PROCEDURE EVOSO;

  BEGIN
    randomize;
    evals := 0;
    gen    := 0;

    indAleatorio(Queen);
    mingl := queen.objective;


    maximo   := 0; {fitness }
    min      := upperb * 10.5;


    { Evoluciona  }
    gen := gen + 1;
    WHILE (gen <= maxgen) DO
         BEGIN
           NEXT_GENERACION;
           IF min < mingl THEN
              BEGIN
                 mingl := min;
                 Queen := mej;
                 genmax := gen;

              END; {end then}

           evals:= evals + 250;
           impDetalle;
           writeln('generacion ',gen:4,' ', mingl:6:2,' ');
           gen := gen + 1;
         END; {while}
         ebest := (abs(upperb- mingl)/upperb) * 100;
         epop  := (abs(upperb-avg)/upperb) * 100;
         impResumen;


 END; (* EVOSO *)
(*-----------------------------------------------------------*)




BEGIN
assign(Datos,'datos.dat');
assign(Det,'detalle.txt');
rewrite(Det);
assign(Resum,'resumen.txt');
assign (Ins,'100X5-10.txt');

rewrite(Resum);
reset(Datos);

SETUP;
inicPesos(Cmj);
cabResumen;
cabDetalle;
for indcorr:= 1 to cantcorr do EVOSO;

CLOSE (Det);
CLOSE (Resum);
CLOSE (Datos);

END.
