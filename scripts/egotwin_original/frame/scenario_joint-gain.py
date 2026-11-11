"""scenario_joint-gain：按场景统计三个框架成功题数与 SAGE Joint 提升。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/scenario_joint-gain.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/scenario_joint-gain.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/scenario_joint-gain.py"
"""
from _statistics import *

def main():
    scenes=["kitchen4","order2","restaurant5","retail6","retail10"];counts=[sum(s==sc for s,i in TASKS) for sc in scenes]+[len(TASKS)]
    values=np.zeros((3,3,6))
    for m in range(3):
        for j in range(3):
            success=joints(m,j)
            values[m,j]=[sum(success.get(k,False) for k in TASKS if k[0]==sc) for sc in scenes]+[sum(success.get(k,False) for k in TASKS)]
            print(SHORT[m],METHODS[j],list(zip(scenes+["All"],values[m,j].astype(int),counts)))
    fig,axs=plt.subplots(2,1,figsize=(4.95,4.3),sharex=True)
    for j,ax in enumerate(axs):
        for m,c in enumerate(["#1f4e9c","#c46a17","#2a9d8f"]):
            gain=(values[m,2]-values[m,j])/counts*100
            bars=ax.bar(np.arange(6)+(m-1)*.26,gain,.24,color=c,label=SHORT[m],zorder=3)
            ax.bar_label(bars,labels=[f"{x:+.0f}" for x in gain],padding=2,fontsize=6.5)
        ax.set_title(f"({chr(97+j)}) SAGE vs. {METHODS[j]}",fontsize=8.5)
        ax.set_ylim(-18,70);ax.set_ylabel("Joint gain (pp)");ax.axhline(0,color="#4c4d4c",lw=.7);ax.axvline(4.5,color="#cccccc",ls="--",lw=.7);style(ax)
    axs[1].set_xticks(range(6),[f"{s}\n(n={n})" for s,n in zip(scenes+["All"],counts)])
    legend(fig,axs[0]);fig.tight_layout(rect=(0,0,1,.94),h_pad=.8);save(fig,"scenario_joint-gain")
if __name__=="__main__": main()
