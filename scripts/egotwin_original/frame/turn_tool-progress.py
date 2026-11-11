"""turn_tool-progress：按轮次截断工具调用并用官方评估器统计累计完成比例。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/turn_tool-progress.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/turn_tool-progress.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/turn_tool-progress.py"
"""
from _statistics import *

def main():
    values=np.zeros((3,3,8,2))
    for m in range(3):
        for j in range(3):
            rows=records(m,j)
            for k in range(8):
                ratios=[];hits=0
                for sc in sorted({s for s,i in TASKS}):
                    truncated=[]
                    for s,i in TASKS:
                        if s!=sc:continue
                        d=rows.get((s,i),{});calls=[]
                        if j==2:
                            for e in d.get("dialogue",[]):
                                if e.get("role")=="executor" and e.get("call") not in (None,"observe_visual","finish","submit_reasoning") and (k==7 or e.get("turn",0)<=k):
                                    calls.append({"tool_name":e["call"],"parameters":e.get("arguments") or {}})
                        else:
                            for t in d.get("tool_calls",[]):
                                if k==7 or t.get("turn",0)<=k:
                                    calls.extend({"tool_name":c.get("tool_name") or c.get("name", ""),"parameters":c.get("parameters") or c.get("arguments") or {}} for c in t.get("calls",[]))
                        truncated.append({"task_id":i,"tool_calls":[{"calls":calls}]})
                    # 格式异常导致官方工具评分未完成（total_gt_calls=0）时记零，
                    # 不修补嵌套 tool_call，以保留原评估行为和全部 96 题分母。
                    for d in score(sc,truncated):
                        t=d["tool_based"];ratios.append(t["matches"]/t["total_gt_calls"] if t["total_gt_calls"] else 0);hits+=t["success"]
                values[m,j,k]=np.mean(ratios)*100,hits/len(TASKS)*100
                print(f"{SHORT[m]} {METHODS[j]} turn={k+1 if k<7 else 'All'}: ratio_sum={sum(ratios):.8f}/{len(TASKS)}={values[m,j,k,0]:.1f}%; all={hits}/{len(TASKS)}={values[m,j,k,1]:.1f}%",flush=True)
    fig,axs=plt.subplots(2,3,figsize=(6.875,3.9))
    for row in range(2):
        for m in range(3):
            ax=axs[row,m]
            ends=values[m,:,-1,row]
            label_y=ends.copy()
            order=np.argsort(ends)
            for prev,cur in zip(order,order[1:]):
                label_y[cur]=max(label_y[cur],label_y[prev]+7.5)
            for j in range(3):
                y=values[m,j,:,row];line(ax,range(8),y,j)
                ax.text(7.28,label_y[j],f"{y[-1]:.0f}",va="center",fontsize=6.5,color="#444444")
            ax.set_title(f"({chr(97+row*3+m)}) {MODELS[m]}",fontsize=8.5);ax.set_ylim(0,100);ax.set_xlim(-.3,7.75)
            ax.set_xticks(range(8),[str(i) for i in range(1,8)]+["All"] if row else []);style(ax)
    axs[0,0].set_ylabel("GT tool calls\ncompleted (%)");axs[1,0].set_ylabel("Tasks with all GT\ntool calls correct (%)")
    legend(fig,axs[0,0]);fig.tight_layout(rect=(0,.04,1,.93),h_pad=.8,w_pad=1)
    fig.supxlabel("Dialogue turn (cumulative)",fontsize=9,y=.005);save(fig,"turn_tool-progress")
if __name__=="__main__": main()
