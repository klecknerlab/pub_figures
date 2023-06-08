import numpy as np
import matplotlib.pyplot as plt
import pub_figures

plt.style.use('pub_figures.10pt')

x = np.linspace(0, 15, 1000)

fig = pub_figures.ScaledFigure((165, 50))

ax = fig.add_axes((12, 10, 55, 35), '(a)')
ax.plot(x, np.sin(x))
ax.set_xlabel('x')
ax.set_ylabel('sin(x)', labelpad=-1) # The default is often a little sloppy -- bring it in
ax.set_title('Sine')
ax.set_xlim(0, 15)
ax.set_ylim(-1.2, 1.4)

ax = fig.add_axes((80, 10, 55, 35), '(b)')
ax.plot(x, np.sin(x), label='sin')
ax.plot(x, np.cos(x), label='cos')
ax.legend(ncol=2, loc='upper right', borderpad=0)
ax.set_xlabel('x')
ax.set_ylabel('f(x)', labelpad=-1) # The default is often a little sloppy -- bring it in
ax.set_title("Sine and Cosine")
ax.set_xlim(0, 15)
ax.set_ylim(-1.2, 1.5)

iy, ix = np.mgrid[:200, :100]
fig.add_image((140, 2.5, None, 45), (iy**2 + ix**2), '(c)', label_params={'color':'white'})

fig.savefig('full_page.svg')
fig.savefig('full_page.pdf')
