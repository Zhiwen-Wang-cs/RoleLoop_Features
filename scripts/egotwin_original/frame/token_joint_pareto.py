"""token_joint_pareto：统计 fixed96 成功率和平均 token 并画帕累托图。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/token_joint_pareto.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/token_joint_pareto.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/token_joint_pareto.py"
"""
from _statistics import *
from matplotlib.lines import Line2D

def main():
    _,v=aggregates()
    fig,ax=plt.subplots(figsize=(3.25,2.8))
    markers=["o","s","^"]
    for m in range(3):
        for j in range(3): ax.scatter(v[m,j,1],v[m,j,0],marker=markers[m],s=44 if j==2 else 30,color=COLORS[j],edgecolors="white",linewidths=.7,zorder=3)
        ax.annotate("",xy=(v[m,2,1],v[m,2,0]),xytext=(v[m,0,1],v[m,0,0]),arrowprops=dict(arrowstyle="-|>",color="#c6d4ec",lw=1.1,shrinkA=8,shrinkB=8))
        ax.annotate(SHORT[m],(v[m,2,1],v[m,2,0]),xytext=((7,-4) if m==0 else (-8,0)),textcoords="offset points",ha="left" if m==0 else "right",fontsize=7.5)
    handles=[Line2D([],[],color=c,marker="o",ms=4.5,ls="",label=k) for c,k in zip(COLORS,METHODS)]
    handles += [Line2D([],[],color="#999999",marker=mk,ms=4.5,ls="",label=k) for mk,k in zip(markers,SHORT)]
    fig.legend(handles=handles,ncol=3,loc="upper center",frameon=False,columnspacing=1,handletextpad=.3)
    ax.set(xlim=(150,560),ylim=(0,80),xlabel="Tokens per task (k)",ylabel="Joint success rate (%)")
    ax.text(548,74,"better ↖",ha="right",color="#777777",fontsize=7.5);style(ax,"both");ax.set_yticks(range(0,81,10))
    fig.tight_layout(rect=(0,0,1,.85));save(fig,"token_joint_pareto")
if __name__=="__main__": main()
