{*********************************************************************}

UNIT op_mut;

INTERFACE
 USES varglo,utility;

 PROCEDURE mutshift(VAR p1:cromosoma);
 FUNCTION flip(probability:real):boolean;

 PROCEDURE mutacion(VAR crom:cromosoma);
(* Realiza permutacion de a pares - Selecciona dos posiciones aleatorias
   e intercambia su contenido *)

IMPLEMENTATION

PROCEDURE mutShift(VAR p1:cromosoma);
(* mutacion de Reeves *)
VAR
 posmut,      (* Posicion original del elemento *)
 posShift,    (* Posicion en la cual se va a colocar el elemento
              que esta en posmut *)
 shift: byte; (* Cantidad de posiciones que se desplazara el elemento
              a partir de posmut *)
 aux:byte;

 PROCEDURE MakeShiftRight(VAR p1: cromosoma; desde,hasta: byte);
 (* Realiza el desplazamiento de los elementos hacia la derecha *)
 VAR i: byte;
 BEGIN
  FOR i:= desde DOWNTO hasta DO
      p1[i+1] := p1[i]
 END; (* MakeShiftRight *)

 PROCEDURE MakeShiftLeft(VAR p1: cromosoma; desde,hasta: byte);
 (* Realiza el desplazamiento de los elementos hacia la izquierda *)
 VAR i: byte;
 BEGIN
  FOR i:= desde TO hasta DO
      p1[i-1] := p1[i]
 END; (* MakeShiftLeft *)

BEGIN
posmut := rnd(1,maxcrom);
shift := rnd(1,maxcrom-1);

IF flip(0.5) THEN { ir a la izquierda de posmut}
       (* No es circular *)
       IF shift < posmut THEN BEGIN
                               posShift := posmut - shift;
                               aux := p1[posmut];
                               MakeShiftRight(p1,posmut-1,posShift);
                               p1[posShift] := aux
                              END
       (* Es circular *)
                         ELSE BEGIN
                               posShift := maxcrom - (shift-posmut);
                               aux := p1[posmut];
                               MakeShiftRight(p1,posmut-1,1);
                               p1[1] := p1[maxcrom];
                               MakeShiftRight(p1,maxcrom-1,posShift);
                               p1[posShift] := aux;
                              END
             ELSE  { ir a la derecha de posmut }
               (* No es circular *)
               IF shift <= maxcrom-posmut THEN BEGIN
                                               posShift := posmut + shift;
                                               aux := p1[posmut];
                                               MakeShiftLeft(p1,posmut + 1,posShift);
                                               p1[posShift] := aux
                                              END
               (* Es circular *)
                                         ELSE BEGIN
                                               posShift := shift - (maxcrom-posmut);
                                               aux := p1[posmut];
                                               MakeShiftLeft(p1,posmut+1,maxcrom);
                                               p1[maxcrom] := p1[1];
                                               MakeShiftLeft(p1,2,posShift);
                                               p1[posShift] := aux;
                                              END;
END; (* MutShift *)

(************************************************************************)
function flip (probability: real): boolean;

begin

     if probability = 1.0 then flip := true
                          else flip := (random <= probability)
end;

(************************************************************************)

PROCEDURE mutacion(var crom:cromosoma);
(* exchange mutation  -->  Seleccina dos posiciones aleatorias
   e intercambia su contenido *)
VAR

semilla,posmut,posmut2:integer;
aux:integer;

BEGIN
posmut := rnd(1,maxcrom);

REPEAT
  posmut2 := rnd(1,maxcrom);
UNTIL posmut <> posmut2;
aux := crom[posmut];
crom[posmut]  := crom[posmut2];
crom[posmut2] := aux;
END;
(*-----------------------------------------------------*)

END.
