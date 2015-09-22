# maxr - Third-order integrator for the Maxey-Riley equations, in Python

author: [@jesserobertson](http://twitter.com/jesserobertson)

### What happen?!

This uses a third-order (in time) scheme from [Daitsche (2013)](http://arxiv.org/pdf/1210.2576.pdf). 
The equations solved are a rewritten version of the Maxey-Riley equations, _sans_ the Faxen correction terms.

![$$ w(t + \delta t) = w(t) + \int_t^{t+\delta t}G(\tau)d\tau + H(t + \delta t) - H(t) $$](http://mathurl.com/render.cgi?w%28t%20+%20%5Cdelta%20t%29%20%3D%20w%28t%29%20+%20%5Cint_t%5E%7Bt+%5Cdelta%20t%7DG%28%5Ctau%29d%5Ctau%20+%20H%28t%20+%20%5Cdelta%20t%29%20-%20H%28t%29%5Cnocache)

and

$$ \frac{dr}{dt} = w + u $$

where $w$ is the difference between the particle velocity $v$ and the fluid velocity $u$, $G(t)$ is the 'velocity term' (the part of the Maxey-Riley equation corresponding to the instantaneous effects of the local fluid flow), and $H(t)$ is the 'history term'. The velocity term is given by

$$
	G(t) = (R - 1)\frac{du}{dt} - Rw\cdot\nabla u - \frac{R}{S}w
$$

and the history term by

$$
	H(t) = -R\sqrt{\frac{3}{\pi S}}\int_{0}^{t+\delta t}\frac{w(\tau)}{\sqrt{t - \tau}}d\tau
$$

and $R=3\rho_f/(\rho_f + 2\rho_p)$ is a density ratio, and $S=a^2/3\nu T$ is the relaxation timescale.