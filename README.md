# sorcery
A code path and code generator for Dis that is esoteric in itself.  
It outputs a code path you can follow to write the Dis program yourself.  
Or it can output intermediate Dissent code which can be transpiled using Dissent.  
It is only able to generate code for printing out a short string of text. 

### Uses

- You need a value in Dis and don't now how to get it
- Generate a Dis program to print some text for you

### How does it work

Given an initial string of memory (the 7 operators in Dis) it uses 2 lookup tables 
to try to generate a combination of shift and subtract operators that result in
the required memory values and then prints them out. *IF* a solution is found,
it will shuffle the memory to try to shorten the outputted translated Dis code.
The intermediate Dissent code will remain the same except for the `SET` instructions.  
The full process to get Dis code would be:   
`text input -> code path -> Dissent code -> Dis code`  

### Setup

Make a copy of Dissent from https://github.com/intangere/dissent into `dissent/`

Change `full_goal` in path.py to the text value you want.  

Run `python3 path.py`.
If this fails you can try `python3 path.py --optimize` which tries to reuse the data space  
instead of expanding the data space.  

### Example
Let's say we want to print out `h` so we set `full_goal ='h'` and run `path.py`.  
Output code path:
`
Starting values [42, 62, 95, 33, 123, 125, 94, 124]
62->186 via 9 > ops. Memory space must contain: 62
33->11 via 1 > ops. Memory space must contain: 33
11->0 via 0 LOAD ops. Memory space must contain: 11
['a=', 11, 'd=', 186]->104 via 1 | ops. Memory space must contain: ['a=', 11, 'd=', 186]
104->STDOUT via 1 { ops. Memory space must contain: 104
`  
Output dissent code:  
`
;data
SET 35, 62
SET 36, 33
JUMP
IS_C 95
SUB 34
SUB 34
;runnable code
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 35
SHIFT 36
SHIFT 34
SUB 36
SHIFT 34
SUB 36
SUB 35
A_OUT
`  
And if we transpile the dissent code:  
`^!_________________________________!>!_________________________________________________________*|*|*__>*__>*__>*__>*__>*__>*__>*__>*__>*_>_*>|_*>||{!`
### Problems

- There is only about 60 cells available to be used for memory which means only short text programs will be successfully generated.

### Future?

- [ ] This needs an entire rewrite to become truly useful. It was a proof of concept to see if it was even doable.
- [ ] Expanding the memory space to allow for longer texts to be successfully found. This isn't that hard. You just need to insert a jump instruction that goes further than the data space which is currently about 34-95 and adjust the internal data_pointer accordingly.
- [ ] Data space chaining needs to be redone properly which would make --optimize work significantly better. 
- [ ] by default only output code path
- [ ] --generate-code and --code-path to output only Dissent code generated or both
- [x] Move zero pointer to start of data space (34)
- [ ] Proper command line arguments
- [ ] Command line arg to specify input instead of modifying code
### Info

- Dis is a variant of malboge 
