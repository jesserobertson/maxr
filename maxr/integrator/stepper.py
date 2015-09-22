class StepperBase(object):
    
    """ Base class for integration stepping methods
    """
    
    def __init__(self, flow, params):
        super(Stepper, self).__init__()
        self.flow = flow
        self.params = params

        # Storage
        self.trace = {
            'position': [],
            'vel_difference': []
        }

    def __next__(self):
        """ Advance state
        """
        self.trace['vel_difference'].append(self.wnext())
        self.trace['position'].append(self.rnext())
        return (self.trace['position'], 
                self.trace['vel_difference'])
        
    def rnext(self):
        """ Return next position
        """
        raise NotImplementedError()

    def wnext(self):
        """ Return next velocity difference
        """
        raise NotImplementedError()

    def velocity_kernel(self, x, t):
        """ Return the velocity part of the the Maxey-Riley equations 
        
            The velocity kernel is:

            \[
                G(t) = (R-1)\frac{du}{dt} - Rw\cdot \nabla u - \frac{R}{S}w
            \]
        """
        pass

    def history_kernel(self, x, t):
        """ Return the history part of the Maxey-Riley equations
        
            The history kernel is:

            \[
                H(t) = -R \sqrt{\frac{3}{\pi S}} \int_{t_0}^{t+\delta t} \frac{w(\tau)}{\sqrt{t-\tau}}d\tau
            \]

            (see Daitsche, 2013).
        """
        pass