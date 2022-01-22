# undefinable
A code path and code generator for Dis that is esoteric in itself.  
It outputs a code path you can follow to write the Dis program yourself.  
Or it can output intermediate Dissent code which can be transpiled using Dissent.  
  
It is only able to generate code for printing out a short string of text. 

## How does it work
Given an initial string of memory (the 8 operators in Dis) it uses 2 lookup tables 
to try to generate a combination of shift and subtract operators that result in
the required memory values and then prints them out. *IF* a solution is found,
it will shuffle the memory to try to shorten the outputted translated Dis code.
The intermediate Dissent code will remain the same except for the `SET` instructions.  

## Setup
Make a copy of Dissent from https://github.com/intangere/dissent into `dissent/`

Change `full_goal` in path.py to the text value you want.  

Run `python3 path.py`.
If this fails you can try `python3 path.py --optimize` which tries to reuse the data space  
instead of expanding the data space.  

## Problems
- There is only about 60 cells available to be used for memory which means only short text programs will be successfully generated.

## Future?
- This needs an entire rewrite to become truly useful. It was a proof of concept to see if it was even doable.
- Expanding the memory space to allow for longer texts to be successfully found. This isn't that hard. You just need to insert a jump instruction that goes further than the data space which is currently about 34-95 and adjust the internal data_pointer accordingly.
- Data space chaining needs to be redone properly which would make --optimize work significantly better. 
- by default only output code path
- --generate-code and --code-path to output only Dissent code generated or both

## Info
- Dis is a variant of malboge 