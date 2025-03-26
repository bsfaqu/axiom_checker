# axiom_checker
Command line utility to check various transit function axioms.

## Installation

Make sure to have a python 3.x installation with networkx installed. The networkx package can be installed with the following command:

```pip install networkx```

## Usage

The general workflow of using axiom_checker is to first generate a .tsv file template with ```make_tsv.py``` that allows you to define your transit function,
and then to supply this file to ```check.py``` for axiom checking. In the following we outline how to use these individual scripts.

### make_csv.py

This script creates a tsv file for a chosen number of vertices. Call it with

```python make_tsv.py [vertices] [filename]```

For example, creating an empty .tsv for a transit function on V={u,v,w} and saving it to example.tsv can be done with:
```python make_tsv.py u,v,w example.tsv```

The script then outputs the following table which is also saved to ```example.tsv```:
```
        u       v       w
u       x       x       x
v       x       x       x
w       x       x       x
```

You can then use a text editor or spreadsheet editor of your choice to alter the transit function table.
The rows of the .tsv are the first "argument" of the transit function, and the columns are the second
"argument" of the transit function. Consider the following .tsv:


```
        u       v       w
u       x       u,v,w   u,w
v               x       
w               w,v     x
```
The transit function it describes is defined on V={u,v,w} where R(u,w)={u,w}, R(w,v)={w,v}, R(u,v)={u,w,v},
R(u,u)={u}, R(w,w)={w}, R(v,v)={u}, and the transit function of every other pair of vertices is the empty set.

Note that the "x" in the u,u/v,v/w,w colums defaults to the transit set that is given by (t0).

Furthermore, any other field that is filled with "x" will default to include the transit set that corresponds to the shortest paths in G_R. If no such path exists in G_R, the transit function of this pair is set to the empty set. Take care that fields contains no character (no space) for transit sets that are supposed to be empty to avoid them being defaulted to the vertices of shortest paths in G_R.

For an example of utilizing "x" in the different fields, replacing the field that corresponds to R(u,v) with "x", and all the empty fields with "x", will yield the same transit function for the example above:


```
        u       v       w
u       x       x       u,w
v       x       x       x
w       x       w,v     x
```


### check.py

This script reads a supplied .tsv file and checks it for a selected set of axioms. 
Call it with 

```python check.py [axioms] [filename]```.

For example, checking the exampe above for axioms (b1), (b3), and (tr2) can be achieved by the following command:

```python check.py b1,b3,tr2 example.tsv```.

Take note that the axioms supplied as the second argument have to be separated by "," and cannot include spaces.

The axioms that are supported as of now are exactly the axioms that appear in the manuscript "Directed Interval Transit Functions" [link to manuscript will be included once published].
The arguments to supply to ```check.py``` are:


| Axiom in manuscript    | check.py alias |
| -------- | ------- |
| (t0)  | t0    |
| (t1) | t1    |
| (t2s)    | t2s    |
| (t2a)    | t2s    |
| (t3)    | t3   |
| (tr2)    | tr2    |
| (b1_1)    | b1    |
| (b1_2)    | b1    |
| (b2)    | b2   |
| (b3_1)    | b3    |
| (b3_2)    | b3    |
| (b4)    | b4    |
| (b6_1)    | b6    |
| (b6_2)    | b6    |
| (b6_3)    | b6    |
| (j2)    | j2   |
| (F)    | F    |
| (G)    | G    |
| (co0)    | co0    |
| (co1)    | co1    |
| (co2)    | co2    |
| (co3)    | co3    |
| (g)    | g    |
| (p)    | p    |
| (Mod)    | Mod    |
| (Med)    | Med    |
| (b5)    | b5    |






