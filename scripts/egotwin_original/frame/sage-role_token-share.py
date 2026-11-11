"""sage-role_token-share：从 telemetry 统计 SAGE 四角色 token、调用数和输入开销。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/sage-role_token-share.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/sage-role_token-share.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/sage-role_token-share.py"
"""
from _statistics import *

def main():
    roles=["Planner","Executor","Reporter","Visual"];colors=["#1f4e9c","#2a9d8f","#c46a17","#8b63b3"]
    totals=[]
    for m in range(3):
        rows=sage_telemetry_records(m);sums=np.zeros((4,3))
        for d in rows:
            for e in events(d):
                role=e.get("role")
                if role not in ("planner","executor","reporter","选帧","识别"):continue
                k={"planner":0,"executor":1,"reporter":2,"选帧":3,"识别":3}[role]
                sums[k]+=[e["input_tokens"]+e["output_tokens"],1,e["input_tokens"]]
        totals.append(sums[:,0]/len(rows)/1000)
        for k in range(4):
            t,n,inp=sums[k]
            print(f"{SHORT[m]} {roles[k]}: share={t:.0f}/{sums[:,0].sum():.0f}={t/sums[:,0].sum()*100:.1f}%; token={t:.0f}/{len(rows)}={t/len(rows)/1000:.0f}k; calls={n:.0f}/{len(rows)}={n/len(rows):.1f}; input={inp:.0f}/{n:.0f}={inp/n/1000:.1f}k")
        print(SHORT[m],f"total/task={sum(totals[-1]):.0f}k")
    totals=np.array(totals);shares=totals/totals.sum(axis=1)[:,None]*100
    fig,ax=plt.subplots(figsize=(3.25,1.75));left=np.zeros(3)
    for k in range(4):
        ax.barh(range(3),shares[:,k],left=left,height=.62,color=colors[k],edgecolor="white",label=roles[k])
        for m in range(3):ax.text(left[m]+shares[m,k]/2,m,f"{shares[m,k]:.0f}%",ha="center",va="center",color="white",fontsize=7)
        left+=shares[:,k]
    for m in range(3):ax.text(101.3,m,f"{totals[m].sum():.0f}k",va="center",fontsize=7)
    ax.set_yticks(range(3),SHORT);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel("Share of SAGE tokens per task (%)")
    for s in ("top","right","left"):ax.spines[s].set_visible(False)
    ax.tick_params(axis="y",length=0);legend(fig,ax,4)
    fig.tight_layout(rect=(0,0,1,.88));save(fig,"sage-role_token-share")
if __name__=="__main__": main()
