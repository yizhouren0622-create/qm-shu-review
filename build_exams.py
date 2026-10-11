"""Generate both exam pages and the answer collection from one bilingual source."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def lang(z,e,tag='div',cls=''):
    return f'<{tag} class="{cls}"><div data-lang="zh" lang="zh-CN">{z}</div><div data-lang="en" lang="en">{e}</div></{tag}>'
def inline(z,e):return f'<span data-lang="zh" lang="zh-CN">{z}</span><span data-lang="en" lang="en">{e}</span>'
def disclosure(z,e,content,kind):
    return '<details class="reveal '+kind+'"><summary>'+inline(z,e)+'</summary><div class="reveal-body">'+lang(content['zh'],content['en'],cls='parallel')+'</div></details>'
def format_options(s):
    def format_match(m):
        options=re.sub(r'<br\s*/?>',' ',m.group(1))
        options=re.sub(r'\s+([B-D]\.)',r'<br>\1',options)
        return '<div class="opts">'+options+'</div>'
    return re.sub(r'<div class="opts">(.*?)</div>',format_match,s,flags=re.S)
def card(q,collection=False):
    n=q['n']; points=q['points']
    out=f'<section class="question" id="q{n}" data-points="{points}" aria-labelledby="q{n}-title"><h3 id="q{n}-title">'+inline(f'第 {n} 题',f'Question {n}')+f'<small>{points} '+inline('分','points')+'</small></h3>'
    if not collection:out+=lang(format_options(q['question']['zh']),q['question']['en'],cls='question-body parallel')
    else:out+='<p class="topic-links"><a href="exam.html#q'+str(n)+'">'+inline('查看题目','View question')+'</a></p>'
    out+=disclosure('提示','Hint',q['hint'],'hint')+disclosure('参考答案与步骤','Answer & working',q['answer'],'solution')
    out+=f'<p class="topic-links"><a href="formulas.html#qmf-{q["formula"]}">'+inline('查看相关公式','Related formula')+'</a></p></section>'
    return out

def page(title,meta,groups,collection=False):
    body='<main class="exam-page"><article class="exam-paper"><h1>'+inline(*title)+'</h1>'+lang(*meta,cls='exam-meta')
    body+=lang('本卷与参考答案由 AI 生成，仅供对照课件复习自测，不是课程官方试卷或解答。','This AI-generated paper and its reference solutions are revision material, not an official course examination or answer key.',cls='ai-note')
    body+=lang('先独立作答；需要时点击每题的“提示”或“参考答案与步骤”。两者默认收起，可分别展开。分值以题号旁标注为准。','Attempt each question first. Open its Hint or Answer & working when needed; both start closed and open independently. Points are shown beside each question.',cls='exam-instructions')
    body+='<div class="exam-actions"><button type="button" data-print="questions">'+inline('打印题目','Print questions')+'</button><button type="button" data-print="solutions">'+inline('打印含答案版','Print with solutions')+'</button><button type="button" data-close-reveals>'+inline('收起所有提示和答案','Close all hints & answers')+'</button></div>'
    body+='<nav class="exam-toc" aria-label="试卷目录 / Exam sections">'+''.join(f'<a href="#sec{i}">'+inline(*t)+'</a>' for i,(t,_) in enumerate(groups,1))+'</nav>'
    for i,(heading,qs) in enumerate(groups,1):
        body+=f'<h2 id="sec{i}">'+inline(*heading)+'</h2>'+''.join(card(q,collection) for q in qs)
    body+=lang('常数若题中未给，可保留符号。数值结果允许合理的末位舍入差异。','Keep constants symbolic when not specified. Reasonable rounding differences in the last digit are acceptable.',cls='exam-meta')+'</article></main>'
    if collection:
        body=re.sub(r'<button type="button" data-print="questions">.*?</button>','',body)
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title[0]+'</title></head><body>'+body+'</body></html>'

def build():
    data=json.loads((ROOT/'data/exams.json').read_text()); q=data['comprehensive']; c=data['chapter3']
    assert sum(x['points'] for x in q)==sum(x['points'] for x in c)==100
    groups=[(('一、选择题 · 20 分','I. Multiple choice · 20 points'),q[:10]),(('二、填空题 · 16 分','II. Fill in the blanks · 16 points'),q[10:16]),(('三、计算题 · 44 分','III. Calculations · 44 points'),q[16:20]),(('四、简答题 · 20 分','IV. Short answers · 20 points'),q[20:])]
    meta=('Chapter 01–03 · 满分 100 分 · 建议用时 100 分钟 · 闭卷自测<br>范围依据三份课件，不含固体物理；本站的拓展阅读不作为本卷出题依据。','Chapters 01–03 · 100 points · Suggested time: 100 minutes · Closed-book self-test<br>Based on the supplied slides, excluding solid-state physics and the site’s supplementary reading.')
    (ROOT/'exam.source.html').write_text(page(('前三章 · 综合模拟卷','Chapters 01–03 · Comprehensive mock exam'),meta,groups))
    (ROOT/'answers.source.html').write_text(page(('综合卷 · 参考答案','Comprehensive exam · Reference solutions'),('与综合卷共用同一份答案来源。每题答案默认收起，点击后查看。','Uses the same solution source as the comprehensive paper. Each answer starts closed; click to reveal it.'),groups,True))
    cg=[(('一、概念与简答 · 30 分','I. Concepts & short answers · 30 points'),c[:3]),(('二、证明题 · 20 分','II. Proofs · 20 points'),c[3:5]),(('三、计算题 · 35 分','III. Calculations · 35 points'),c[5:7]),(('四、测不准关系 · 15 分','IV. Uncertainty · 15 points'),c[7:])]
    (ROOT/'exam-ch3.source.html').write_text(page(('第3章 · 力学算符模拟卷','Chapter 03 · Operators mock exam'),('Chapter 03 · 满分 100 分 · 建议用时 90 分钟<br>δ 分布、算符与厄米性、对易关系、测量与平均值、动量和角动量、测不准关系。','Chapter 03 · 100 points · Suggested time: 90 minutes<br>Delta distributions, operators and Hermiticity, commutators, measurements, momentum, angular momentum and uncertainty.'),cg))
if __name__=='__main__':build()
