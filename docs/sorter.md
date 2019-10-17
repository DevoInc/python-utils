# Sort Library

Generic tool for order events. The library is composed of
the 'sorter' sorting class and utility submodules for the library.

The sorter class contains the sort_file function that receives the parameters
necessary to carry out the proper arrangement.

The covered functionality is:
* Sorting a file
* Sorting a iterator
* Sorting of several files that meet a certain regex for a
directory, joining the result
* Sorting and unification of a list of files passed as an argument
* Origin and Destination in CSV format
* Origin and destination compressed with gzip
* Result in destination file or return an iterator
* Reverse ordering
* Sorting by data of numeric type, string or date
* Sorting files or iterators based on a field obtained by separator
* Sorting files or iterators based on a field obtained by object key
* Sorting files or iterator based on a field obtained by regular expression
* Sort with Memory Safe option, avoid that all RAM is consumed
use divide and conquer, recording multiple temporary files
  * Memory safe by default 40% of RAM available at the time of
  call to function
  * Memory safe indicating % of the available memory that you want to use
  * Memory safe indicating maximum memory to use in bytes.


## Library modules
 
The modules have the following relationship

```
 _________           _________
|         |         |         |
| sorter  |-------> | reader  |
|_________|         |_________|
     |
     |
     |
 ____V________           _________
|             |         |         |
| comparator  |-------> | parser  |
|_____________|         |_________|

```

The main module has the sort_file or sort_iterator function that based on the parameters of
entry decides which reader you should use. One is the parameters of the function is
the comparator to use in the ordering of files.

The comparators compare 2 events. The events have a format defined by
what to be able to compare 2 events you must extract the value that you want
compare each of the events. In order to obtain the value, they are used
the functions of parser. comarator functions return functions to use
in sorting, in the same way the parser functions return a parser to
use in the comparison function.

### Parser module

Contains functions that are used to parse events in the comparison of
events. The functions receive parameters and return the functions to be used
in the comparators.

Functions:
* **parser_list(position):** returns the element of the position position of
   the list that makes up the event.
  
  _Example of use:_
  ```python
  from devoutils.sorter import Sorter

  sorter = Sorter()
  sorter.parser.parser_list(10)
  ```
* **parser_delimiter(delimiter, position):** returns the element of the position
`position` once the event is separated by the delimiter.

  _Example of use:_
  ```python
  from devoutils.sorter import Sorter

  sorter = Sorter()
  sorter.parser.parser_delimiter(",", 1)
  ```
* **parser_regex(regex, group, ignore_case=False):** returns the element of
`group` group of the regular expression.

  _Example of use:_
  ```python
  from devoutils.sorter import Sorter

  sorter = Sorter()
  sorter.parser.parser_regex("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})" ,0)
  ```

### Comparator module

It contains a series of comparators that can be used in sorting. The
module functions return the comparator function that will be used in the
ordering of files. The comparators need the parser that is going to
use to obtain the value to be compared.

The existent comparators are:
* **compare_date(date_format, parser):** compare dates in the given format,
receives a parser to obtain the date to be compared. The date_format must
follow the formats explained in: 
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

  _Example of use:_
  ```python
  from devoutils.sorter import Sorter

  sorter = Sorter()
  sorter.comparator.compare_date('%Y-%m-%d %H:%M:%S.%f',
                            sorter.parser.parser_regex(
                                "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"
                                ,0))                        
  ```
  
* **compare_num(parser):** compare numbers. Receive a parser to get
the number to compare.

  _Example of use:_
  ```python
  from devoutils.sorter import Sorter

  sorter = Sorter()
  sorter.comparator.compare_num(sorter.parser.parser_delimiter(",", 1))
  ```
  
  _Example of use:_
  ```python
  from devoutils.sorter import Sorter, compare_num, parser_list

  sorter = Sorter()
  sorter.sort_iterator(data_json_iterator, 
                       comp=compare_num(parser_list('bytesTransferred')),
                       dst_file="/tmp/somefile_orderer.txt",
                       memory_safe=True)
  ```
  
* **compare_str(parser):** compare strings. Receive a parser to get
the strings to compare.

  _Example of use:_
  ```python
  from devoutils.sorter import Sorter

  sorter = Sorter()
  sorter.comparator.compare_str(sorter.parser.parser_delimiter(",", 2))
  ```

### Sorter class - Main module

The sorter module is the main module of the library and only has one
public function to be used. Depending on the parameters that are passed to the
function will take different strategies of reading and sorting files.

**sort_file(self, src, dst_file=None, **kwargs)_** can receive this arguments:

* ** src: ** Source to sort, it can be a file, a list of files
or a path in which the regex of _file_pattern_ will be applied to read several
files to unify and order
* ** dst_file: ** Destination file in which to write the result. Default
its value is None, if it is not indicated the function will return an iterator to be able to
iterate over the sorted data.
* ** file_pattern: ** Regular expression to search the files to be sorted inside
of the _src_ directory
* ** is_csv: ** if the file to be read is csv, by default False, if it is indicated to
True, additional parameters for csv parsing can be indicated. Yes it is
csv returns each line in a list. The optional parameters for csv are:
  * ** delimiter: ** Delimiter to be used in the csv, by default,
  * ** quote_char: ** Character to escape delimiters.
* ** is_target_gzip: ** If the file to be written is gzip, by default False.
* ** reverse: ** Initiate if the sort is in reverse order, default False
* ** comp: ** Comparator to use to recover the next element of
the files ordered.
* ** memory_safe: ** If you are going to use memory safe techniques to avoid consuming all
the RAM memory of the machine. By default it would use 40% of the memory
available on the machine at the time of execution. You can indicate
additional parameters to the memory safe to manage the behavior. These
Parameters are:
  * ** tmp_dir: ** temporary directory in which to save temporary files
  * ** max_mem: ** maximum memory in butes per temporary file
  * ** av_mem_perc: ** percentage of available memory to use in each file
* ** rows_to_skip: ** number of rows to jump on the header of each file.
* ** transform: ** event transformation function. If you want to transform
the event before ordination


_Simple ordination example_
```python
from devoutils.sorter import Sorter
sorter = Sorter()
sorter.sort_file("src.log", "dst.log", reverse=True)
```

_Regex ordination example_
```python
from devoutils.sorter import Sorter

sorter = Sorter()
sorter.sort_file("src.log", "dst.log",
                 comp=sorter.comparator.compare_date(
                    '%Y-%m-%d %H:%M:%S.%f',
                    parser_regex(
                        "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"
                        ,0)))                     
```

_Example of memory ordination safe reading multiple files_
```python
from devoutils.sorter import Sorter, compare_date, parser_regex

sorter = Sorter()
data = sorter.sort_file("./", file_pattern="testData.*\\.log",
                        comp=compare_date(
                            '%Y-%m-%d %H:%M:%S.%f',
                            parser_regex(
                                "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"
                                ,0)), memory_safe= True, max_mem=5000000)
```

_List of files ordination example_
```python
from devoutils.sorter import Sorter, compare_date, parser_regex

data = Sorter.sort_file(['data/file1.log', 'data/file2.log'],
                       comp=compare_date(
                           '%Y-%m-%d %H:%M:%S.%f',
                           parser_regex(
                               "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:"
                               "\d{2}\.\d{6})"
                               , 0)), 
                               memory_safe=True, max_mem=5000000)
```

_Ordination with transformation example_
```python
from devoutils.sorter import Sorter
import re
sorter = Sorter()
sorter.sort_file("src.log", "dst.log", 
                 transform=lambda x:re.search("(\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})", x).groups()[0] + "##" + x)
```

## RECOMMENDATIONS

Sorting by parsing can be very heavy, for example with a regex
would apply the regex 2 * NlogN times in the comparisons what can be
computationally very heavy. To optimize a transformation can be used
placing the chain to compare and compare strings at the beginning of the log. This
applies to string and some date formats, but not for numbers.
Another option would be for the transformer to generate a tuple with the first element
the element to be compared and the second the event. At the time of purchase,
I would compare the first element. This option would be valid for the case in which
it is not written to a file and an iterator is returned

## TODO
* Include sort_stream function that receives an iterator and returns an iterator,
the parameters would be the same as sort_file without source / destination file
* Create writer that you send to Devo.
* More complex and complete tests.