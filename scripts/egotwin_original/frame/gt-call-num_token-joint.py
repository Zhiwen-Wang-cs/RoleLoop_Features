"""gt-call-num_token-joint：按 GT 工具调用数分档统计 Joint 与每题 token 并画图。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/gt-call-num_token-joint.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/gt-call-num_token-joint.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/gt-call-num_token-joint.py"
"""
from _statistics import *

def main():
    values,_ = aggregates()
    fig,axs=plt.subplots(2,3,figsize=(6.875,3.9))
    counts=[sum(bucket(k)==b for k in TASKS) for b in range(3)]
    for row in range(2):
        for m in range(3):
            ax=axs[row,m]
            for j in range(3): line(ax,range(3),values[m,j,:,row],j)
            ax.set_title(f"({chr(97+row*3+m)}) {MODELS[m]}",fontsize=8.5)
            ax.set_xticks(range(3),[f"{s}\n(n={n})" for s,n in zip(["1–4","5–7","8+"],counts)])
            ax.set_xlim(-.25,2.25); ax.set_ylim((0,.85) if row==0 else (150,600));style(ax)
            ax.set_yticks(np.arange(0,.81,.2) if row==0 else np.arange(200,601,100))
    axs[0,0].set_ylabel("Joint success rate");axs[1,0].set_ylabel("Tokens per task (k)")
    legend(fig,axs[0,0]);fig.tight_layout(rect=(0,.04,1,.93),h_pad=.8,w_pad=1)
    fig.supxlabel("# ground-truth tool calls",fontsize=9,y=.005)
    save(fig,"gt-call-num_token-joint")
if __name__=="__main__": main()
