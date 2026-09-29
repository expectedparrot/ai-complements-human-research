import math,functools,numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
def solver(pi0,p):
    ell=math.log(p/(1-p)); lam=math.log(pi0/(1-pi0))
    post=lambda n:1/(1+math.exp(-(lam+n*ell)))
    pup=lambda n:post(n)*p+(1-post(n))*(1-p)
    @functools.lru_cache(None)
    def V(sc,b):
        if b==0: return post(sc[0]) if sc else pi0
        q0=pup(0); best=q0*V(tuple(sorted(sc+(1,),reverse=True)),b-1)+(1-q0)*V(sc,b-1)
        for n in set(sc):
            l=list(sc); l.remove(n); up=tuple(sorted(l+[n+1],reverse=True)); dn=tuple(sorted(l+([n-1] if n>1 else []),reverse=True))
            q=pup(n); best=max(best,q*V(up,b-1)+(1-q)*V(dn,b-1))
        return best
    return lambda B:V((),B)
pis=np.linspace(0.02,0.98,49)
B=8
plt.rcParams.update({'font.size':8,'font.family':'serif','axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(3.3,2.4))
curves={}
for p,ls in [(0.6,':'),(0.7,'-'),(0.9,'--')]:
    S=np.array([solver(pi,p)(B)-pi for pi in pis]); curves[p]=S
    ax.plot(pis,S,ls,color='black',lw=1.2)
pk=lambda p:(pis[int(np.argmax(curves[p]))],curves[p].max())
x,y=pk(0.9); ax.annotate('$p=0.9$ (one check nearly\nreveals the type)',xy=(x,y),xytext=(x+0.03,y+0.02),fontsize=6.8,ha='left',va='bottom')
x,y=pk(0.7); ax.annotate('$p=0.7$',xy=(x,y),xytext=(x+0.02,y+0.03),fontsize=6.8,ha='left',va='bottom')
x,y=pk(0.6); ax.annotate('$p=0.6$ (one check is\nbarely informative)',xy=(x,y),xytext=(x-0.02,y-0.05),fontsize=6.8,ha='left',va='top')
ax.set_xlabel(r'share of good projects after screening, $\pi$')
ax.set_ylabel('value added by $B=8$ human checks\n$S(\\pi)=V_B(\\pi)-\\pi$')
ax.set_xlim(0,1); ax.set_ylim(0,0.86)
ax.annotate('a screen that moves $\\pi$ up the slope\nraises the value of human checks',xy=(0.02,0.855),fontsize=6.5,color='0.35',ha='left',va='top')
ax.annotate('',xy=(0.26,0.74),xytext=(0.03,0.74),arrowprops=dict(arrowstyle='->',color='0.35',lw=0.8))
ax.annotate('past the peak, a better\nscreen lowers it',xy=(0.99,0.47),fontsize=6.5,color='0.35',ha='right',va='bottom')
ax.annotate('',xy=(0.99,0.45),xytext=(0.76,0.45),arrowprops=dict(arrowstyle='->',color='0.35',lw=0.8))
fig.tight_layout(pad=0.3)
fig.savefig('hump.pdf')
fig.savefig('hump.png', dpi=200)
