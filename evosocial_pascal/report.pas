{***************************************************************}
unit report;

interface

uses varglo;

PROCEDURE cabResumen;
PROCEDURE cabDetalle;
procedure impDetalle;
PROCEDURE impResumen;

Implementation


(*-----------------------------------------------------------*)

Procedure cabResumen;

{ imprime la cabecera del archivo Resumen}


BEGIN
  write(resum,'Upperb ',upperb:6);
  writeln(resum,' Pc:',pcross:4:2,' Pm:',pmutacion:4:2,' Maxgen:',maxgen,' Popsize:',popsize);
end;


Procedure cabDetalle;

{ imprime la cabecera del archivo Detalle}

BEGIN
  write(det,'Upperb ',upperb:6);
  writeln(det,' Pc:',pcross:4:2,' Pm:',pmutacion:4:2,' Maxgen:',maxgen,' Popsize:',popsize);

end;


PROCEDURE impDetalle;
 begin
 writeln(det,gen:4,'  ',mingl:6:2,' ',evals);
end;

PROCEDURE impResumen;
BEGIN
  write(Resum,indcorr:2,' ',ebest:5:2,' ');
  writeln(Resum,epop:5:2,' ',mingl:6:2,' ',genmax:4);

END;


END.
