unit varglo;  {Definiciones globales, usadas por el main y unidades}

interface
const
  maxcrom   = 100; {Anterior codigo}
  maxmaq    = 5;   {Anterior codigo}
  COSTOgy = 400000;  {Costo de la turbina por aÃ±o}
  filas = 10;        {Filas del campo}
  columnas = 10;     {Columnas del campo}

type
      alelotv = array [1..columnas] of byte; {Vector xi fila del campo}
      individuotv = RECORD

                    END;
      turbinas_viento =  array [1..filas, 1] of byte;  {Estructura que mantiene el campo de turbinas}

      alelo     = byte;  {posicion de bit}
      cromosoma = array[1..maxcrom] of alelo;

      individuo = RECORD
                   cromosoma : cromosoma;
                   objective,
                   fitness :real;
                  END;

      individuot = RECORD

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



