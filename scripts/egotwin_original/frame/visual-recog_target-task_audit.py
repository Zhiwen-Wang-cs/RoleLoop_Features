"""visual-recog_target-task 审计：逐条列出 Base/Summary_v2 中“泄露前查过、但因枚举被剔除”的目标。
每条打印：题号、目标描述、标准名、命中查询的轮次与工具、同轮同工具查过的其他候选名。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/visual-recog_target-task_audit.py"
    # 只看某个模型/模式：
    python ".../visual-recog_target-task_audit.py" Muse-Glimmer-30B Base
"""
import sys,importlib.util,collections
spec=importlib.util.spec_from_file_location("vr",__file__.replace("_audit.py",".py")); vr=importlib.util.module_from_spec(spec); spec.loader.exec_module(vr)
models=[sys.argv[1]] if len(sys.argv)>1 else vr.MODELS; modes=[sys.argv[2]] if len(sys.argv)>2 else ["Base","Summary"]
for model in models:
    for mode in modes:
        dist=collections.Counter(); print(f"===== {model} {mode}")
        for row in vr.gt:
            sc,i=row["task"].rsplit("_",1); ev=vr.events(model,mode,sc,int(i)) or []
            allgt={vr.n(a) for tg in row["targets"] for a in tg["answer"]}
            for tg in row["targets"]:
                for a in map(vr.n,tg["answer"]):
                    k=vr.first_probe(ev,a)
                    if k is None: continue
                    sib=vr.siblings(ev,k,allgt)
                    if not sib: continue
                    dist[min(len(sib),10)]+=1; _,_,T,tool=ev[k]
                    print(f"{row['task']} | {tg['ref'][:60]} | GT: {a} | 第{T}轮 {tool} | 其他候选{len(sib)}个: {sorted(sib)[:8]}{' …' if len(sib)>8 else ''}")
        print("其他候选个数分布（10=≥10）:",sorted(dist.items()))
