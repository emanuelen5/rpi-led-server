# Benchmarking the rendering loop

## How

```bash
$ apt install graphviz imagemagick
$ pip install gprof2dot
```

Using basic profiling:
```bash
$ python -m cProfile -o profile.dat main_oled.py
$ gprof2dot -f pstats profile.dat | dot -Tpng | display
```

Loop timing was added to the script to give an overview of the mean time for each loop.

## Before any optimizations
Commit: 7e312ac61e379097ec5d04585f0256dc3bd215aa
```
Render times:
 -   mean:   5.0968 ms
 -    min:   4.3306 ms
 -    std:   0.6867 ms
 -  (max):   9.8155 ms
```


## Splitting to boolean loop without bitshifts
Commit: 9b7916e332da256ebc522a85059aa50c17b9953f
```
Render times:
 - samples: 100
 -    mean: 5.0899 ms
 -     min: 4.3638 ms
 -     std: 0.5842 ms
 -   (max): 8.1284 ms
```


## Pre-calculation of bitmap masks
Commit: 7c0c31d84c0f1d9a1ecf56b7b4659c75a940b5b4
```
Render times:
 - samples: 100
 -    mean: 3.6226 ms
 -     min: 2.9545 ms
 -     std: 0.5357 ms
 -   (max): 5.2145 ms
```


## Matrix operations
Commit: ac5a095348af62076b540840407e045df15d7d1b
```
Render times:
 - samples: 100
 -    mean: 1.9301 ms
 -     min: 1.3750 ms
 -     std: 0.4637 ms
 -   (max): 3.1466 ms
```
