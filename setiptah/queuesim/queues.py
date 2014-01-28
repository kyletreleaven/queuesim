
# simulation interface is implicit;
from setiptah.eventsim.signaling import Signal, Message

class token : pass


class GatedQueue :
    def __init__(self) :
        self._queue = []
        self._pending = []
        
        self.output = Signal()
        
    def join_sim(self, sim ) :
        self.sim = sim
        
    """ slot """
    def arrival(self, arrival ) :
        self._queue.append( arrival )
        self._try_release()
        
    def requestRelease(self) :
        self._pending.append( token() )
        self._try_release()
        
    def _try_release(self) :
        if len( self._queue ) <= 0 or len( self._pending ) <= 0 : return
        # otherwise, we have an annihilation
        
        self._pending.pop(0)        # burn a token
        msg = Message( self.output, self._queue )
        self.sim.schedule( msg )
        
        self._queue = []




class MultiGatedQueue :
    def __init__(self) :
        self.demands = []
        self.pending = []
        
    def join_sim(self, sim ) :
        self.sim = sim
        
    class ServerInterface :
        def __init__(self, parent ) :
            self.parent = parent
            
            """ signal """
            self.batch_out = Signal()
        
        """ slot """
        def request_in( self ) :
            self.parent.request_in( self )
            
    def spawn_interface(self) :
        return self.ServerInterface( self )
    
    """ slot """
    def demand_arrived(self, demand ) :
        self.demands.append( demand )
        self._try_dispatch()
        
    """ slot, collected from interfaces """
    def request_in(self, interface ) :
        self.pending.append( interface )
        self._try_dispatch()
        
    """ utility """
    def _try_dispatch(self) :
        if len( self.demands ) == 0 or len( self.pending ) == 0 : return
        # otherwise, we have an annihilation!
        
        interface = self.pending.pop(0)       # get the next pending request
        msg = Message( interface.batch_out, self.demands )
        self.sim.schedule( msg )
        
        self.demands = []
        
        
        