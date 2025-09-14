{*********************************************************************}

UNIT Utility;

INTERFACE
Uses varglo;


PROCEDURE showopt(v:cromosoma);

FUNCTION RND (low,high: integer): integer;
(* Devuelve un entero random entre low y high *)

PROCEDURE GenCutPoints(cant: integer; VAR ptocorte1,ptocorte2: integer);
 (* Genera dos puntos de corte para un cromosoma *)

FUNCTION valid_crom(v:cromosoma;VAR fila:cromosoma):boolean;

FUNCTION validacrom(v:cromosoma):boolean;

function flip (probability: real): boolean;

IMPLEMENTATION

PROCEDURE showopt(v:cromosoma);
VAR
 i:integer;
BEGIN
  FOR i := 1 to maxcrom DO write(v[i]);
  writeln(' ');
END;

{------------------------FUNCTION RND  -------------------------}

FUNCTION RND (low,high: integer): integer;
(* Devuelve un entero random entre low y high *)

VAR i: integer;
BEGIN

     if low >= high then i := low
                    else begin
                              i := trunc(random * (high - low + 1) + low);
                              if i > high then i := high;
                         end;
     rnd := i;
END; (* RND *)

{------------------------ FUNCTION GetCutPoints -------------------------}

PROCEDURE GenCutPoints(cant: integer; VAR ptocorte1,ptocorte2: integer);
 (* Genera dos puntos de corte para un cromosoma *)
 VAR
  semilla,auxi: integer;
 BEGIN
  ptocorte1:= RND(2,cant-1);
  REPEAT
   ptocorte2:= RND(2,cant-1);
   IF ptocorte2 < ptocorte1 THEN
     BEGIN
      auxi := ptocorte1;
      ptocorte1 := ptocorte2;
      ptocorte2 := auxi
     END;
  UNTIL ptocorte2 <> ptocorte1;
 END; (* GenCutPoints *)
(* ------------------------------- GenCutPoints -----------------*)


FUNCTION valid_crom(v:cromosoma;VAR fila:cromosoma):boolean;

VAR
i:integer;


  PROCEDURE ordshell(v:cromosoma;var fila:cromosoma);
  (* ordena de < a > *)

  VAR

  salto,m,n:1..maxcrom;
  temp:integer;
  hechotodo:boolean;

  BEGIN
   fila := v;
   salto:= maxcrom;
  WHILE salto > 1  DO
   BEGIN
     salto := salto div 2;
     REPEAT
       hechotodo := true;
       FOR m := 1 TO maxcrom - salto DO
           BEGIN
              n := m + salto;
              IF fila[m] > fila[n]  (*ordena de < a > *)
                 THEN  BEGIN
                         temp := fila[m];
                         fila[m] := fila[n];
                         fila[n] := temp;
                         hechotodo := false
                       END;
           END; {for}
      UNTIL hechotodo;
   END;
   END;
   (* ordshell *)
BEGIN
ordshell(v,fila);
FOR i := 1 TO  maxcrom DO IF fila[i] <> i THEN
    valid_crom := false
    ELSE valid_crom := true;

END;

FUNCTION validacrom(v:cromosoma):boolean;
var
   i,k: integer;
   cromaux: cromosoma;
   sn: boolean;
begin
     sn:= true;
     for i:= 1 to maxcrom do
         cromaux[i]:= 0;
     for i:= 1 to maxcrom do
         begin
            if v[i] <= maxcrom then
               cromaux[v[i]]:= 1
            else
               sn:= false
         end;
     for i:= 1 to maxcrom do
       begin
         if cromaux[i] = 0 then
             sn:= false;
       end;
     validacrom:= sn;
end;


function flip (probability: real): boolean;

begin

     if probability = 1.0 then flip := true
                          else flip := (random <= probability);

end;



END.
