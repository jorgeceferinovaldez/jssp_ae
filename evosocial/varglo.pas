unit varglo;  {Definiciones globales, usadas por el main y unidades}

interface
const
  maxcrom   = 100;
  maxmaq    = 5;

type

      alelo     = byte;  {posicion de bit}
      cromosoma = array[1..maxcrom] of alelo;

      individuo = RECORD
                   cromosoma: cromosoma;
                   objective,
                   fitness:real;
                  END;
      tipoconj  = set of 1..maxcrom;
      hijos     = array [1..2] of individuo;

      tipoMaqJob= array [1..maxmaq, 1.. maxcrom] of byte;

var
queen, mej : individuo;

Datos, Det, Resum, Ins: text;
indcorr:byte;
child: hijos;
cantcorr, maxgen, popsize, gen, genmax: integer;
indchild:integer;

pmutacion,pcross, mingl, ebest, epop, min, maximo: real;
avg: real;

upperb, lowerb, evals: longint;

Cmj: tipoMaqJob;


implementation

end.



