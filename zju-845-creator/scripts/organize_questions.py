#!/usr/bin/env python3
"""Local 845 question organizer. Keyword fallback is not semantic classification."""
from __future__ import annotations
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import secrets
import shutil

CATEGORIES = ("01-数学模型","02-时域分析","03-根轨迹","04-频域分析","05-离散系统",
              "06-非线性控制","07-现代控制","08-综合题","99-待分类")
ALIASES = {
    "数学模型":0,"建模":0,"时域":1,"时域分析":1,"根轨迹":2,"根轨迹分析":2,
    "频域":3,"频域分析":3,"离散":4,"离散系统":4,"离散控制":4,
    "非线性":5,"非线性控制":5,"现代控制":6,"现代控制理论":6,"状态空间":6,
    "综合":7,"综合题":7,"跨模块":7,"待分类":8,"未确定":8,
}
RULES = {
  0: [(r"梅森|信号流图|框图化简|建立微分方程|电路建模|机械系统建模",5),(r"数学模型|系统建模|求传递函数",3)],
  1: [(r"超调量|峰值时间|调节时间|稳态误差|动态性能|终值定理",5),(r"单位阶跃响应|斜坡响应|阻尼比|劳斯判据|Routh",4)],
  2: [(r"根轨迹|分离点|汇合点|出射角|入射角",5),(r"渐近线|实轴根轨迹",4)],
  3: [(r"Nyquist|奈奎斯特|Bode|伯德|波德",5),(r"增益裕度|相位裕度|幅值裕度|频率特性",4)],
  4: [(r"Z变换|z变换|Jury|朱利判据|脉冲传递函数",5),(r"采样周期|离散系统|单位圆稳定|差分方程",4)],
  5: [(r"描述函数|相平面|极限环|非线性环节",5),(r"非线性控制|相轨迹",4)],
  6: [(r"能控|能观|可控性|可观性|状态反馈|状态观测器",5),(r"状态空间|状态方程|矩阵指数|Lyapunov|李雅普诺夫|Riccati|最优控制|PBH",4)],
}
ALLOWED_ATTACHMENTS = {".pdf",".png",".jpg",".jpeg",".webp",".txt",".md"}


def normalize_category(value):
    value = str(value).strip()
    if value in CATEGORIES:
        return value
    if value in ALIASES:
        return CATEGORIES[ALIASES[value]]
    raise ValueError("未知分类：" + value)


def classify_question(item):
    if item.get("category"):
        cat = normalize_category(item["category"])
        return {"category":cat,"method":"explicit","review_required":cat==CATEGORIES[8],"scores":{}}
    text = "\n".join(str(item.get(k) or "") for k in ("title","original","variant","topic_hint"))
    scores = {CATEGORIES[i]:sum(w for regex,w in rules if re.search(regex,text,re.I))
              for i,rules in RULES.items()}
    ranked = sorted(scores.items(),key=lambda t:(-t[1],CATEGORIES.index(t[0])))
    a,b = ranked[:2]
    if a[1]<3:
        category=CATEGORIES[8]
    elif b[1]>=4 and b[1]>=a[1]*0.75:
        category=CATEGORIES[7]
    else:
        category=a[0]
    return {"category":category,"method":"keyword_fallback",
            "review_required":category in (CATEGORIES[7],CATEGORIES[8]),
            "scores":{k:v for k,v in ranked if v}}


def init_bank(root):
    for cat in CATEGORIES:
        target=root/cat
        target.mkdir(parents=True,exist_ok=True)
        (target/".gitkeep").touch(exist_ok=True)


def load_items(path):
    obj=json.loads(path.read_text(encoding="utf-8"))
    items=obj if isinstance(obj,list) else [obj]
    if not items or any(not isinstance(x,dict) for x in items):
        raise ValueError("需要题目 JSON 对象或非空对象数组")
    return items


def save_item(item,root,include_solution=False,dry_run=False):
    original=item.get("original") or ""
    variant=item.get("variant") or ""
    if not isinstance(original,str) or not isinstance(variant,str) or not (original.strip() or variant.strip()):
        raise ValueError("每题至少含非空 original 或 variant")
    classification=classify_question(item)
    raw=str(item.get("id") or ("Q"+datetime.now().strftime("%Y%m%d-%H%M%S")+"-"+secrets.token_hex(3)))
    ident=re.sub(r"[^A-Za-z0-9_-]","-",raw).strip("-_")[:60] or "Q-"+secrets.token_hex(4)
    cat=classification["category"]
    folder=root/cat/ident
    ix=2
    while folder.exists():
        folder=root/cat/(ident+"-"+str(ix).zfill(2))
        ix+=1
    title=str(item.get("title") or "845 同构题")[:120]
    files=[name for name,body in (("original.md",original),("variant.md",variant)) if body.strip()]
    if include_solution and isinstance(item.get("solution"),str) and item["solution"].strip():
        files.append("solution.md")
    attachments=item.get("attachment_paths") or []
    tags=item.get("tags") or []
    if not isinstance(attachments,list) or not all(isinstance(p,str) for p in attachments):
        raise ValueError("attachment_paths 需要本地路径字符串数组")
    if not isinstance(tags,list) or not all(isinstance(p,str) for p in tags):
        raise ValueError("tags 需要字符串数组")
    # Validate all attachment paths before creating a directory.
    sources=[Path(path).expanduser() for path in attachments]
    for source in sources:
        if source.is_symlink() or not source.is_file() or source.suffix.lower() not in ALLOWED_ATTACHMENTS:
            raise ValueError("无效或不支持的附件："+str(source))
    if not dry_run:
        folder.mkdir(parents=True,exist_ok=False)
        for filename,body in (("original.md",original),("variant.md",variant)):
            if body.strip():
                (folder/filename).write_text("# "+title+"\n\n"+body.strip()+"\n",encoding="utf-8")
        if "solution.md" in files:
            (folder/"solution.md").write_text("# "+title+" — 解析\n\n"+item["solution"].strip()+"\n",encoding="utf-8")
        for source in sources:
            target=folder/"attachments"
            target.mkdir(exist_ok=True)
            clean=re.sub(r"[^A-Za-z0-9_.-]","_",source.name)
            dst=target/clean
            suffix=2
            while dst.exists():
                dst=target/(Path(clean).stem+"-"+str(suffix)+source.suffix.lower())
                suffix+=1
            shutil.copy2(source,dst)
            files.append("attachments/"+dst.name)
        meta={"id":folder.name,"title":title,"category":cat,"tags":tags,
              "mode":item.get("mode") or "同构训练","source_id":item.get("source_id"),
              "classification":classification,"files":files}
        (folder/"metadata.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"folder":str(folder),"category":cat,"files":files,
            "classification":classification,"dry_run":dry_run}


def main():
    parser=argparse.ArgumentParser(description="分类归档845题目，仅本地文件写入")
    parser.add_argument("command",choices=("init","classify","save"))
    parser.add_argument("--root",type=Path,default=Path("question-bank"))
    parser.add_argument("--input",type=Path)
    parser.add_argument("--include-solution",action="store_true")
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args()
    if args.command=="init":
        if not args.dry_run:
            init_bank(args.root)
        result={"root":str(args.root),"categories":CATEGORIES,"dry_run":args.dry_run}
    else:
        if not args.input:
            parser.error("classify/save 必须带 --input")
        questions=load_items(args.input)
        result=[classify_question(q) if args.command=="classify" else
                save_item(q,args.root,include_solution=args.include_solution,dry_run=args.dry_run)
                for q in questions]
        if len(result)==1:
            result=result[0]
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
