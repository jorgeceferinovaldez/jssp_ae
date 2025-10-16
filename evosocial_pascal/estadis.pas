{*********************************************************************}

unit estadis;

interface

uses varglo;

procedure stats(indi:individuo);

implementation

procedure stats(indi:individuo);
Begin
 with indi do
     begin
     IF objective < min THEN
                  begin
                  min := objective;
                  mej := indi;
                  end;

     if objective > maximo then
                     maximo := objective;
     end;
end;
end.
