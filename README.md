# maxr - Third-order integrator for the Maxey-Riley equations, in Python

author: [@jesserobertson](http://twitter.com/jesserobertson)

### What happen?!

This uses a third-order (in time) scheme from [Daitsche (2013)](http://arxiv.org/pdf/1210.2576.pdf). 
The equations solved are a rewritten version of the Maxey-Riley equations, _sans_ the Faxen correction terms.

![$$ w(t + \delta t) = w(t) + \int_t^{t+\delta t}G(\tau)d\tau + H(t + \delta t) - H(t) $$](http://mathurl.com/pyoxoal.png)

and

![$$ \frac{dr}{dt} = w + u $$](http://mathurl.com/nqeyj8e.png)

where ![$r$](http://mathurl.com/375ggas) is the particle location, $w$ is the difference between the particle velocity $v$ and the fluid velocity $u$, $G(t)$ is the 'velocity term' (the part of the Maxey-Riley equation corresponding to the instantaneous effects of the local fluid flow), and $H(t)$ is the 'history term'. The velocity term is given by

![$$ G(t) = (R - 1)\frac{du}{dt} - Rw\cdot\nabla u - \frac{R}{S}w $$](http://mathurl.com/nnc8vhn.png)

and the history term by

![$$ H(t) = -R\sqrt{\frac{3}{\pi S}}\int_{0}^{t+\delta t}\frac{w(\tau)}{\sqrt{t - \tau}}d\tau $$](http://mathurl.com/pcox2xa.png)

and ![$R=3\rho_f/(\rho_f + 2\rho_p)$](http://mathurl.com/q3dkzm3) is a density ratio, and ![$S=a^2/3\nu T$](http://mathurl.com/qjbnj34) is the relaxation timescale.