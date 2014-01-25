
import numpy as np

# simulation interface is implicit;
from setiptah.eventsim.signaling import Signal, Message


class PoissonClock(object) :
    
    def __init__(self, rate=1. ) :
        self.rate = rate
        self._output = Signal()
        
    def _reschedule(self) :
        tau = np.random.exponential( 1. / self.rate )
        self.sim.schedule( self.tick, tau )
        
    def join_sim(self, sim ) :
        self.sim = sim
        self._reschedule()
        
    def tick(self) :
        self._output()
        self._reschedule()
        
    def source(self) :
        return self._output
    
    
    
    
class ScriptSource(object) :
    def __init__(self, script ) :
        self.script = script
        self.next_time = 0.
        self.iter = ( item for item in self.script )
        
        self.output = Signal()
        
    def _reschedule(self) :
        try :
            curr_time = self.next_time
            t, out = self.iter.next()
            
            self.next_demand = out
            self.next_time = t
            self.sim.schedule( self.emit, t - curr_time )
            
        except StopIteration :
            return
        
        
    def join_sim(self, sim ) :
        self.sim = sim
        self._reschedule()
        
    """ auto slotoid """
    def emit( self ) :
        self.output( self.next_demand )
        self._reschedule()
        
    def source(self) : return self.output


    