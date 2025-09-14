{*********************************************************************}

UNIT Crossvs;

INTERFACE
 USES varglo,utility,op_mut;

 PROCEDURE crossox(p1,p2:cromosoma);
 (* Order crossover *)


IMPLEMENTATION

(* -------------------------------------------------*)

PROCEDURE crossox(p1,p2:cromosoma);
(* Order crossover *)
VAR
ptocorte,ptocorte2:integer; h:cromosoma;

 PROCEDURE GenHijo(maxcrom,ptocorte,ptocorte2: byte; v,w: cromosoma);

 (* Genera un cromosoma hijo *)
 VAR
  i,j,auxi: byte;
  aux: cromosoma;
  conj:tipoconj;

 BEGIN
  conj  := [ ];

  FOR i :=  ptocorte TO ptocorte2 DO
   BEGIN
    h[i] := v[i];
    conj := conj + [h[i]];
   END;

 j:= 0;
 { Armar auxiliar con extremo del 2do corte}
 FOR i := ptocorte2+1 TO maxcrom DO
  IF NOT(w[i] in conj) THEN
     BEGIN
      j:=j+1;
      aux[j]:= w[i];
     END;

 {Completar auxiliar con el segundo padre}

 FOR i:= 1 to ptocorte2 DO
  IF NOT(w[i] in conj) THEN
   BEGIN
    j:= j+1;
    aux[j]:= w[i];
   END;
{ Armar hijo }

 j:=0;
 FOR i := ptocorte2+1 TO maxcrom DO
  BEGIN
   j:= j+1;
   h[i]:= aux[j];
  END;

 FOR i:= 1 TO ptocorte-1 DO
  BEGIN
   j:= j+1;
   h[i]:= aux[j];
  END;

 IF flip(pmutacion) THEN mutacion(h);
 indchild := indchild + 1;
 child[indchild].cromosoma := h;

 END; (* GenHijo *)

BEGIN (* CrossOX *)
 (* Obtiene los dos puntos de corte *)
 GenCutPoints(maxcrom,ptocorte,ptocorte2);
 (* Obtiene el primer hijo *)
 GenHijo(maxcrom,ptocorte,ptocorte2,p1,p2);

(* Obtiene el segundo hijo *)
 GenHijo(maxcrom,ptocorte,ptocorte2,p2,p1);

END;(* CrossOX *)

END.

