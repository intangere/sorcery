from json import loads
from dissent.dissent import Assembler, parse_program, mem_to_program, fill_noops
import sys
import random

"""IMPORTANT NOTE
goal should be the full string in question i.e 'hello world!'
base loop_vals = ['*','>','_','!','{','}','^','|']
shift each one and see if it equals 'h', if not, for each one see if we can 
take the resulting values from piping to together (maybe shifted) which creates a value we can use to get 'h',
then add that resulting value to the loop_values and repeat outputting an array of the order of operations required.
"""

DEBUG = False
CHAIN = False

with open('tables/pipe_table.json', 'r') as f:
     pipe_table = loads(''.join(f.readlines()))


with open('tables/shift_table.json', 'r') as f:
     shift_table = loads(''.join(f.readlines()))

print('Loaded > operator table')

def subtract(a, d):
  i = ( a // 1 % 3 - d // 1 % 3 + 3 ) % 3 * 1;
  i += ( a // 3 % 3 - d // 3 % 3 + 3 ) % 3 * 3;
  i += ( a // 9 % 3 - d // 9 % 3 + 3 ) % 3 * 9;
  i += ( a // 27 % 3 - d // 27 % 3 + 3 ) % 3 * 27;
  i += ( a // 81 % 3 - d // 81 % 3 + 3 ) % 3 * 81;
  i += ( a // 243 % 3 - d // 243 % 3 + 3 ) % 3 * 243;
  i += ( a // 729 % 3 - d // 729 % 3 + 3 ) % 3 * 729;
  i += ( a // 2187 % 3 - d // 2187 % 3 + 3 ) % 3 * 2187;
  i += ( a // 6561 % 3 - d // 6561 % 3 + 3 ) % 3 * 6561;
  i += ( a // 19683 % 3 - d // 19683 % 3 + 3 ) % 3 * 19683;
  return i

def shift(num):
    return num // 3 + num % 3 * 19683

def shift_10(num):
    shifts = []
    prev = num
    for i in range(10):
        shifts.append(prev)
        prev = shift(prev)
    return shifts


class Op(object):
   def __init__(self, initial_value, op, result, count):
       self.op = op
       self.initial = initial_value
       self.result = result
       self.count = count
   def __str__(self):
       return '%s->%s via %s %s ops. Memory space must contain: %s' % (self.initial, self.result, self.count, self.op, self.initial)

def find_cycle(goal, loop_vals):

    print('Starting values', loop_vals)

    for val in loop_vals:

        #something should be done about this
        #if val == goal:
        #   die
        #   op = Op(val, '{', 0, 0)
        #   op_path.append(op)

        shifts = shift_10(val)
        if goal in shifts: #Fully correct
           print('Shifts needed:', shifts.index(goal), 'from', val, 'to get', goal)
           print(val, shifts)
           op = Op(val, '>', goal, shifts.index(goal))
           op_path.append(op)
           op = Op(goal, '{', 'STDOUT', 1)
           op_path.append(op)

           if CHAIN:
              loop_vals[loop_vals.index(val)] = goal
           #loop_vals.append(goal)
           return loop_vals

        for pair in subtracts:
            for shifted in shifts:
                if shifted in pair:
                   #print('Shift from', val, 'to', shifted, 'for', pair)
                   op = Op(val, '>', shifted, shifts.index(shifted))
                   possible_pairs.append((shifted, pair, op))


    #print('Possible pairs', possible_pairs)

    for vals in possible_pairs:
        have_val = vals[0]
        need = vals[1][:]
        need.remove(have_val)
        need = need[0]
        for val in loop_vals:
            ops = []
            shifts = shift_10(val)
            for shifted in shifts:
                if shifted == need:
                   #ops.append([val, (shifts.index(shifted)+1)*'>'])
                   print('Found shift from', val, chr(val), shift_10(val).index(need)*'>')
                   print('Shift table:', shift_10(val))
                   print('We have', have_val, 'and acquire', need, 'by above shift')
                   print(vals)
                   #ops.append([vals[1], '|'])
                   if need == vals[1][1]:
                      op_path.append(vals[2])


                      if CHAIN:
                         loop_vals[loop_vals.index(vals[2].initial)] = vals[2].result

                      print('Since val we need(%s) is in d, we are good' % need)
                      print('By subtracting',have_val,'|',need, 'we get', subtract(have_val,need),'=',goal)

                      op = Op(val, '>', shifted, shifts.index(shifted)) #This is wrong
                      op_path.append(op)

                      if CHAIN:
                            loop_vals[loop_vals.index(val)] = shifted

                      op = Op(have_val, 'LOAD', 0, 0)
                      op_path.append(op)

                      op = Op(['a=',have_val, 'd=',need], '|', subtract(have_val,need), 1)
                      op_path.append(op)

                      op = Op(subtract(have_val, need), '{', 'STDOUT', 1)
                      op_path.append(op)

                      if CHAIN:
                         loop_vals[loop_vals.index(need)] = subtract(have_val, need) #used to index shifted
                      #loop_vals.append(subtract(have_val, need))
                      return loop_vals
                   else:
                      print('Since val we need(%s) is in a, we need to swap a and d first' % need)
                      print('By subtracting',need,'|',have_val,'we get', subtract(need,have_val),'=',goal)
                      print('Swapping a and d may be non trivial so we ignore this case')
                      #If we implement this case, more options would be possible

                      op_path.append(vals[2]) #This was fucking missing fuck me

                      if CHAIN:
                         loop_vals[loop_vals.index(vals[2].initial)] = vals[2].result

                      #Need to setup for need=shifted | have_val

                      op = Op(val, '>', shifted, shifts.index(shifted)) #This is wrong
                      op_path.append(op)

                      #Where the fuck is have_val coming from

                      if CHAIN:
                         loop_vals[loop_vals.index(val)] = shifted

                      op = Op(need, 'LOAD', 0, 0)
                      op_path.append(op)

                      op = Op(['a=',need, 'd=',have_val], '|', subtract(need,have_val), 1)
                      op_path.append(op)

                      op = Op(subtract(need,have_val), '{', 'STDOUT', 1)
                      op_path.append(op)

                      if CHAIN: #This is probably an illegal op and the source of memory corruption
                            #if have_val in loop_vals:
                               loop_vals[loop_vals.index(have_val)] = subtract(need,have_val) #used to be shifted
                            #else: #have_val must have been shifted, this is a problem
                            #   loop_vals[loop_vals.index(shifted)] = subtract(need,have_val) #used to be shifted
                      #loop_vals.append(subtract(have_val, need))
                      return loop_vals
                else:
                     #continue #ignore all this
                     if subtract(val, shifted) == need:
                       if need == vals[1][1]:

                          op_path.append(vals[2])
                          print('FOUND! 1')

                          if CHAIN:
                             loop_vals[loop_vals.index(vals[2].initial)] = vals[2].result

                          op = Op(val, '>', shifted, shifts.index(shifted))
                          op_path.append(op)  #We have 2 shifts in a row. this is the problem

                          if CHAIN:
                             loop_vals[loop_vals.index(val)] = shifted

                          op = Op(val, 'LOAD', 0, 0) #Used to load shifted which is wrong
                          op_path.append(op)

                          op = Op(['a=',val, 'd=',shifted], '|', need, 1)
                          op_path.append(op)

                          if CHAIN:
                             loop_vals[loop_vals.index(shifted)] = subtract(val, shifted)

                          op = Op(have_val, 'LOAD', 0, 0)
                          op_path.append(op)

                          op = Op(['a=',have_val, 'd=',need], '|', subtract(have_val, need), 1)
                          op_path.append(op)

                          op = Op(subtract(have_val, need), '{', 'STDOUT', 1)
                          op_path.append(op)

                          if CHAIN: #sus attempt here
                             #loop_vals[loop_vals.index(need)] = subtract(have_val, need)
                             #if need in loop_vals:
                                loop_vals[loop_vals.index(need)] = subtract(have_val, need) #used to be shifted
                             #else: #have_val must have been shifted, this is a problem
                             #   print('need not in loop_vals found 1. need and shifted are in same position')
                             #   loop_vals[loop_vals.index(shifted)] = subtract(have_val,need) #used to be shifted

                          return loop_vals
                       else:
                          print('Swap of a and d would be required.. ignoring') #have_val,need are swapped to need, have_val
                          #continue
                          op_path.append(vals[2])
                          print('FOUND! 1 swapped')

                          if CHAIN:
                             loop_vals[loop_vals.index(vals[2].initial)] = vals[2].result

                          op = Op(val, '>', shifted, shifts.index(shifted))
                          op_path.append(op)  #We have 2 shifts in a row. this is the problem

                          if CHAIN:
                             loop_vals[loop_vals.index(val)] = shifted

                          op = Op(val, 'LOAD', 0, 0) #Used to load shifted which is wrong
                          op_path.append(op)

                          op = Op(['a=',val, 'd=',shifted], '|', need, 1)
                          op_path.append(op)

                          if CHAIN:
                             loop_vals[loop_vals.index(shifted)] = subtract(val, shifted)

                          op = Op(need, 'LOAD', 0, 0)
                          op_path.append(op)

                          op = Op(['a=',need, 'd=',have_val], '|', subtract(need, have_val), 1)
                          op_path.append(op)

                          op = Op(subtract(need, have_val), '{', 'STDOUT', 1)
                          op_path.append(op)

                          if CHAIN:
                             #loop_vals[loop_vals.index(have_val)] = subtract(need, have_val)
                             #if have_val in loop_vals:
                                loop_vals[loop_vals.index(have_val)] = subtract(need,have_val) #used to be shifted
                             #else: #have_val must have been shifted, this is a problem
                             #   print('have_val not in loop_vals found 1 swapped')
                             #   loop_vals[loop_vals.index(shifted)] = subtract(need,have_val) #used to be shifted

                          return loop_vals
                          #continue
                     elif subtract(shifted, val) == need:
                       #continue
                       if need == vals[1][1]:

                          op_path.append(vals[2])
                          print('FOUND! 2')

                          if CHAIN:
                             loop_vals[loop_vals.index(vals[2].initial)] = vals[2].result

                          op = Op(val, '>', shifted, shifts.index(shifted))
                          op_path.append(op)  #We have 2 shifts in a row. this is the problem

                          if CHAIN:
                             loop_vals[loop_vals.index(val)] = shifted

                          op = Op(shifted, 'LOAD', 0, 0) #Used to load shifted which is wrong
                          op_path.append(op)

                          op = Op(['a=',shifted, 'd=',val], '|', need, 1) #Technically val no longer exists so how is this even possible ;_;
                          op_path.append(op)

                          if CHAIN:
                             loop_vals[loop_vals.index(shifted)] = subtract(shifted, val) #val=shifted so val no longer exists

                          op = Op(have_val, 'LOAD', 0, 0)
                          op_path.append(op)

                          op = Op(['a=',have_val, 'd=',need], '|', subtract(have_val, need), 1)
                          op_path.append(op)

                          op = Op(subtract(have_val, need), '{', 'STDOUT', 1)
                          op_path.append(op)

                          if CHAIN:
                             loop_vals[loop_vals.index(need)] = subtract(have_val, need)

                          return loop_vals
                       else:
                          print('Swap of a and d would be required.. ignoring')

                          op_path.append(vals[2])
                          print('FOUND! 2 swapped')

                          if CHAIN:
                             loop_vals[loop_vals.index(vals[2].initial)] = vals[2].result

                          op = Op(val, '>', shifted, shifts.index(shifted))
                          op_path.append(op)  #We have 2 shifts in a row. this is the problem

                          if CHAIN:
                             loop_vals[loop_vals.index(val)] = shifted

                          op = Op(shifted, 'LOAD', 0, 0) #Used to load shifted which is wrong
                          op_path.append(op)

                          op = Op(['a=',shifted, 'd=',val], '|', need, 1) #Technically val no longer exists so how is this even possible ;_;
                          op_path.append(op)

                          if CHAIN:
                             loop_vals[loop_vals.index(shifted)] = subtract(shifted, val) #val=shifted so val no longer exists

                          op = Op(need, 'LOAD', 0, 0)
                          op_path.append(op)

                          op = Op(['a=',need, 'd=',have_val], '|', subtract(need, have_val), 1)
                          op_path.append(op)

                          op = Op(subtract(need, have_val), '{', 'STDOUT', 1)
                          op_path.append(op)

                          if CHAIN:
                             loop_vals[loop_vals.index(have_val)] = subtract(need, have_val)

                          return loop_vals
                         #continue

                   #print(ops)
                   #return

    print('Could not find a way to acquire the value:', goal)
    sys.exit(1)

def shift_self(val, count):
    new_val = val
    i = 0
    while i < count:
      new_val = shift(new_val)
      i += 1
    return new_val

def can_shift_to(val, need):
    new_val = val
    i = 1
    for _ in range(10):
        new_val = shift(new_val)
        if new_val == need:
           return i+1 #Since 0 index

def generate_code(ops, base_vals, reset_mem=True):
    data_space_start = 35
    data_space_ptr = 35

    #seperated generating the memory space from generating code
    #so that in can be optimized during code path generation

    code_start = 95

    program = [';data']


    #We use 34 for 0 to shorten swapping code
    zero_ptr = 34
    #data_space_ptr += 1

    for val in base_vals:
        program.append('SET %s, %s' % (data_space_ptr, val))
        data_space_ptr += 1

    #Setup initial jump
    program.append('JUMP')
    program.append('IS_C 95')
    if data_space_ptr >= 95:
       print('FAILED. Data space pointer %s extends into runnable code %s. This code will not run' % (data_space_ptr, 95))
       sys.exit(1)

    #here is where we would insert a jump greater than 95 if needed. unimplemented
    #   i = 95
    #   while i <= data_space_ptr:
    #     program.append('NOOP')
    #     i += 1

    #load a 0 for swapping
    program.append('SUB %s' % 34)
    program.append('SUB %s' % 34)

    #replace shift_10 with shift 0, sub, shift 0, sub
    #d and a values need to be in place for sub. this is missing

    #Code
    program.append(';runnable code')
    for idx, op in enumerate(ops):
     try:
        print(base_vals)
        if op.op == '>': #oooooh nooooo the d count is missing
           required_d = data_space_start + base_vals.index(op.initial)

           if op.count == 10:
              program = program + ['SHIFT %s' % zero_ptr]
              program = program + ['SUB %s' % required_d]
              program = program + ['SHIFT %s' % zero_ptr]
              program = program + ['SUB %s' % required_d]
              print('Using zero swap instead of shift_10')
           elif op.count == 0: #Simply load value into a
              program = program + ['SHIFT %s' % zero_ptr]
              program = program + ['SUB %s' % required_d]
              program = program + ['SHIFT %s' % zero_ptr]
              program = program + ['SUB %s' % required_d]
           else:
              program = program + ['SHIFT %s' % (required_d) for _ in range(op.count)]
              base_vals[base_vals.index(op.initial)] = shift_self(op.initial, op.count)
        if op.op == '|':
           required_d = data_space_start + base_vals.index(op.initial[-1])
           #program = program + ['GOTO_D %s' % required_d]
           #program = program + ['IS_D %s' % required_d]
           program = program + ['SUB %s' % (required_d) for _ in range(op.count)]
           print(op.initial)
           base_vals[base_vals.index(op.initial[-1])] = subtract(op.initial[1], op.initial[3])
        if op.op == '{':
           program.append('A_OUT')
        if op.op == 'LOAD':
           required_d = data_space_start + base_vals.index(op.initial)
           # program = program + ['GOTO_D %s' % required_d]
           #program = program + ['IS_D %s' % required_d]
           #Need to load d into a
           program = program + ['SHIFT %s' % zero_ptr]
           program = program + ['SUB %s' % required_d]
           program = program + ['SHIFT %s' % zero_ptr]
           program = program + ['SUB %s' % required_d]

     except Exception as e:
       print(e)
       print('Failed',idx, op)
       print('Memory space', base_vals)
       sys.exit(1)
    program.append('EXIT')

    return '\n'.join(program), base_vals

if __name__ == '__main__':
   loop_vals = ['*','>','_','!','{','}','^','|']
   loop_vals = [ord(val) for val in loop_vals]
   base_loop_vals = loop_vals[:]

   full_goal = 'Hello, world!'
   full_goal = [ord(c) for c in full_goal]

   if '--optimize' in sys.argv:
      CHAIN = True

   #Order of operations required to reach result
   op_path = []

   for goal in full_goal:

      #Possible subtractables to get into a useful shift cycle
      subtracts = pipe_table[chr(goal)]
      possible_pairs = []

      print('Subtract combinations for', goal, 'available:', len(subtracts))

      loop_vals = find_cycle(goal, loop_vals)

   #loop_vals = [ord(_) for _ in ['*','>','_','!','{','}','^','|']]
   loop_vals = []
   for op in op_path:
       if op.initial in [ord(_) for _ in ['*','>','_','!','{','}','^','|']] and len(loop_vals) < 93-33:
          loop_vals.append(op.initial)
       elif type(op.initial) == list:
          if op.initial[3] in [ord(_) for _ in ['*','>','_','!','{','}','^','|']] and len(loop_vals) < 93-33:
             loop_vals.append(op.initial[3])
       elif len(loop_vals) > 94-33:
         print('Data memory space exceeded!', loop_vals)
         #sys.exit(1)

   base_loop_vals = loop_vals[:]

   #We need to remove unused values from loop_vals (but there should be none)

   print('Code path for:',full_goal)
   print('-'*20)
   for op in op_path:
      print(op)
   print('-'*20)
   print('Suggested initial data space:')
   memory = []
   output = []
   for op in op_path:
       if op.op == '>':
          if type(op.initial) == list:
             memory.append(str(op.initial[-1]))
          else:
             memory.append(str(op.initial))
       if op.op == '{':
          output.append(chr(op.initial))

   print(','.join(memory))
   print('Output:', ''.join(output))
   print('Ops required (without no ops):', len(op_path))
   print('Initial values:', base_loop_vals)

   new_loop_vals = base_loop_vals

   good_program = None
   good_code = None
   lens = []

   for x in range(100):
      try:
       random.shuffle(new_loop_vals)
       assembler = Assembler()
       rand_loop_vals = new_loop_vals[:]
       random.shuffle(rand_loop_vals)
       program, _ = generate_code(op_path, rand_loop_vals[:])
       code, macros = parse_program(program.split('\n'))
       codex = mem_to_program(fill_noops(assembler.assemble(code)))
       print('Generated code', codex)
       print('Iter', x)

       lens.append(len(codex))

       if not good_program and codex:
          good_program = program
          good_code = codex
       elif len(codex) < len(good_code) and codex:
          print('Shorter program found', len(codex))
          good_program = program
          good_code = codex
      except Exception as e:
       print(e, 'loop', x, 'failed')
      print('new loop vals', new_loop_vals)
   print(good_program, lens)
   print('Final length:', len(good_code))

   #Need to actually compile the code to check this lmao

  #To optimize this we need to replace memory CHAIN ing with
  #proper d counter per operation or something so we do not have to
  #repeat thing in the data space
