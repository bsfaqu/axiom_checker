# axiom_checker
Command line utility to check various transit function axioms.

## Installation

Make sure to have a python 3.x installation with networkx installed. The networkx package can be installed with the following command:

```pip install networkx```

## Usage

### make_csv.py

This script creates a tsv file for a chosen number of vertices. Call it with

```make_tsv.py [vertices] [filename]```

For example, to create an empty .tsv for a transit function of vertices u,v,w and save it to example.tsv:
```make_tsv.py u,v,w example.tsv```

The script will output the following table, that is also saved to example.tsv:
```
        u       v       w
u       x       x       x
v       x       x       x
w       x       x       x
```

You can then use a text-editor, or spreadsheet-editor of your choice to alter the transit function.
The columns of the .tsv are the first "argument" of the transit function, and the rows are the second
"argument of the transit function. Consider the following .tsv:

```
        u       v       w
u       x       u,v,w   u,w
v               x       
w               w,v     x
```
The transit function it describes is defined on V={u,v,w} where R(u,w)={u,w}, R(w,v)={w,v}, R(u,v)={u,w,v},
R(u,u)={u}, R(w,w)={w}, R(v,v)={u}, and the transit function of every other pair of vertices is the empty set.

Note that the "x" in the u,u/v,v/w,w colums defaults to the transit set that is given by (t0).



### check.py

This script reads a supplied .tsv file and checks it for a selected set of axioms. 
Call it with 

```check.py [axioms] [filename]```.

