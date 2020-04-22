# Devo FileIO

## Features
- Read easily from a csv gziped or not
- Unit tests for use in python >= 3.5

## Class
### FileReader

Lee un fichero y genera un iterador para ir leyendo líneas del fichero.
Permite leer ficheros en formato csv y gzip. Los parámtreos son:

* **src_file:** fichero a leer
* **is_csv:** si el fichero a leer es csv, por defecto a False, si se indica a
True, se pueden indicar parámetros adicionales para el parseo del csv. Si es
csv retorna cada línea en una lista. Los parámetros opcionales para csv son:
  * **delimiter:** Delimitador a usar en el csv, por defecto ,
  * **quotechar:** Caracter para escapar delimitadores.
* **is_gzip:** Si el fichero a leer es gzip, por defecto a False.
* **mode:** modo de lectura del fichero, por defecto 'r'

_Ejemplo de uso:_
```python
from devoutils.fileio import FileReader
# Lee un csv que a su vez esta en formato gzip
reader = FileReader("file.csv.gz", iscsv=True, isgzip=True)
data = []
for d in reader:
    print (d)
```

### FileWriter

Escribe un fichero, al instanciarlo no escribe, retorna un objeto con el
método write que va escribiendo evento a evento. Los parámtreos son:

* **dest_file:** fichero a escribir
* **is_csv:** si el fichero a escribir es csv, por defecto a False, si se indica a
True, se pueden indicar parámetros adicionales para el parseo del csv.
Los parámetros opcionales para csv son:
  * **delimiter:** Delimitador a usar en el csv, por defecto ,
  * **quotechar:** Caracter para escapar delimitadores.
* **is_target_gzip:** Si el fichero a escribir es gzip, por defecto a False.
* **mode:** modo de escritura del fichero, por defecto 'w'

_Ejemplo de uso:_
```python
from devoutils.fileio import FileWriter
# escribe un csv que a su vez esta en formato gzip
writer = FileWriter("file.csv.gz", iscsv=True, istargetgzip=True)
__DATA_CSV = [['id', 'val'],
                  ['1', 'uno'],
                  ['2', 'dooss'],
                  ['3', 'treeeee']]
for d in __DATA_CSV:
    writer.write(d)
```

### FileSortedJoin

Realiza el join de varios ficheros ordenados. El objeto que genera es
un iterador para poder ir obteniendo siempre el siguiente elemento ordenado.
Los parámetros son:

* **part_files:** Listado de los ficheros parciales ordenados.
* **reverse:** Inidica si la ordenación es en orden inverso, por defecto False
* **comp:** Comparador a usar para ir recuperando el siguiente elemento de
los ficheros ordenados. (From lt-sorter)

_Ejemplo de uso:_
```python
from devoutils.sorter import Sorter
from devoutils.fileio import FileSortedJoin

sorter = Sorter()
c = FileSortedJoin(["file1.txt", "file2.txt"],
        comp=sorter.comparator.comparenum(sorter.parser.parser_delimiter(",", 1)))
```