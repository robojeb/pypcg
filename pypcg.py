# coding=utf-8

from cffi import FFI
from random import SystemRandom, Random
from os.path import join, dirname, abspath

__all__ = ['PCG32']

ffi = FFI()

#REMEMBER TO UPDATE THESE AS THINGS CHANGE OR STUFF MIGHT NOT REBUILD RIGHT
VERSION = '0_0_1'
PCG_VERSION = '0_94'

def makeModuleName():
  return 'pcg_c' + '_' + VERSION + '_' + PCG_VERSION

#
# Extracted from pcg_basic.h
#
header ="""
struct pcg_state_setseq_64 {    // Internals are *Private*.
    uint64_t state;             // RNG state.  All values are possible.
    uint64_t inc;               // Controls which RNG sequence (stream) is
                                // selected. Must *always* be odd.
};
typedef struct pcg_state_setseq_64 pcg32_random_t;

// pcg32_srandom(initstate, initseq)
// pcg32_srandom_r(rng, initstate, initseq):
//     Seed the rng.  Specified in two parts, state initializer and a
//     sequence selection constant (a.k.a. stream id)

void pcg32_srandom(uint64_t initstate, uint64_t initseq);
void pcg32_srandom_r(pcg32_random_t* rng, uint64_t initstate,
                     uint64_t initseq);

// pcg32_random()
// pcg32_random_r(rng)
//     Generate a uniformly distributed 32-bit random number

uint32_t pcg32_random(void);
uint32_t pcg32_random_r(pcg32_random_t* rng);

// pcg32_boundedrand(bound):
// pcg32_boundedrand_r(rng, bound):
//     Generate a uniformly distributed number, r, where 0 <= r < bound

uint32_t pcg32_boundedrand(uint32_t bound);
uint32_t pcg32_boundedrand_r(pcg32_random_t* rng, uint32_t bound);
"""

ffi.cdef(header)
#TODO: load the shared object in a better way
#C_interface = ffi.dlopen(join(dirname(abspath(__file__)),'c_pcg.so'))
with open(join(dirname(abspath(__file__)), 'pcg_basic', 'pcg_basic.c')) as source:
  c_interface = ffi.verify(source.read(),
                          include_dirs=[join(dirname(abspath(__file__)),'pcg_basic')],
                          modulename=makeModuleName())

DEFAULT_SEQUENCE = 184628983

class PCG32(Random):
  '''
  An object that wraps a pcg32 engine from the c_pcg_basic library
  '''
  def __init__(self, state=None, seq=DEFAULT_SEQUENCE):
    '''
    Initialize a new PCGRandom engine. If no seed is specified use urandom and
    if no sequene is specified use an arbitrary sequece
    '''
    self._rng_state = ffi.new("pcg32_random_t*");
    #If the state is none then get a random state from system entropy
    if state == None:
      system_random = SystemRandom()
      state = system_random.getrandbits(64)
    c_interface.pcg32_srandom_r(self._rng_state, state, seq)

  def random(self):
    return float(c_interface.pcg32_random_r(self._rng_state))/float(2**32-1)

  def boundedrand_r(self, bound):
    return int(c_interface.pcg32_boundedrand_r(self._rng_state, bound))

  def seed(self, a=None, seq=DEFAULT_SEQUENCE, version=2):
    #TODO support version 2 so we can support python3
    if type(a) != int:
      a = hash(a)
    c_interface.pcg32_srandom_r(self._rng_state, a, seq)

  def getstate(self):
    return self._rng_state

  def setstate(self):
    return self._rng_state

  def jumpahead(self, n):
    raise NotImplementedError

  def getrandbits(self, k):
    num_rand = k//32
    num_extra = k%32
    out = 0
    i = -1
    for i in range(num_rand):
      out |= c_interface.pcg32_random_r(self._rng_state) << (32*i)
    out |= (c_interface.pcg32_random_r(self._rng_state) & (2**num_extra-1)) << (32*(i+1))

    return out
