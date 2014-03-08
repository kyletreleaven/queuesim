
# simulation interface is implicit;
from setiptah.eventsim.signaling import Signal


class Dispatch :
    """ an abstract dispatcher pattern """
    def join_sim(self) :
        raise NotImplementedError('implement join_sim')
        
    class Interface :
        """ a dispatcher-agent interface; do no instantiate directly """
        def __init__(self, parent ) :
            self.dispatch = parent
            
            """ signal """
            self.output = Signal()
            
        # slot
        def input(self, *args, **kwargs ) :
            #print args, kwargs
            self.dispatch.input( self, *args, **kwargs )
            
    def newInterface(self) :
        return self.Interface( self )
            
    # slotoid
    def input(self, interface, *args, **kwargs ) :
        """
        when input is called, interface has received input (args,kwargs)
        interface may be used by dispatcher to customize behavior
        """
        raise NotImplementedError('implement "input" for dispatch')


