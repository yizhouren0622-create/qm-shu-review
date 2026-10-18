"""Render a transcribed source paper and two school-style mocks from shared data."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def lang(z,e,tag='div',cls=''):
    return f'<{tag} class="{cls}"><div data-lang="zh" lang="zh-CN">{z}</div><div data-lang="en" lang="en">{e}</div></{tag}>'
def inline(z,e):return f'<span data-lang="zh" lang="zh-CN">{z}</span><span data-lang="en" lang="en">{e}</span>'
def disclosure(z,e,content,kind):
    return '<details class="reveal '+kind+'"><summary>'+inline(z,e)+'</summary><div class="reveal-body">'+lang(content['zh'],content['en'],cls='parallel')+'</div></details>'
def format_options(s):
    def replace(m):
        t=re.sub(r'<br\s*/?>',' ',m.group(1))
        t=re.sub(r'\s+([B-D]\.)',r'<br>\1',t)
        return '<div class="opts">'+t+'</div>'
    return re.sub(r'<div class="opts">(.*?)</div>',replace,s,flags=re.S)

def references(q,sources):
    items=''.join('<li>'+lang(sources[k]['zh'],sources[k]['en'])+'</li>' for k in q['sources'])
    return '<details class="source-details"><summary>'+inline('课件与教材依据','Slide & textbook references')+'</summary><ul>'+items+'</ul></details>'

def card(q,sources,collection=False):
    n=q['n'];local=q['local'];points=q['points'];s=q['section']
    z=['填空','选择','简答','计算'][s-1];e=['Fill-in','Choice','Short answer','Calculation'][s-1]
    out=f'<section class="question" id="q{n}" data-points="{points}" data-section="{s}" aria-labelledby="q{n}-title"><h3 id="q{n}-title">'+inline(f'{z} {local}',f'{e} {local}')+f'<small>{points} '+inline('分','points')+'</small></h3>'
    if q.get('origin'):out+='<p class="question-origin">'+inline('原卷 '+q['origin'],'Source paper '+q['origin'].replace('一、','I.').replace('二、','II.').replace('三、','III.').replace('四、','IV.'))+'</p>'
    if not collection:out+=lang(format_options(q['question']['zh']),q['question']['en'],cls='question-body parallel')
    else:out+='<p>'+lang(q['title']['zh'],q['title']['en'])+'</p><p><a href="exam.html#q'+str(n)+'">'+inline('查看对应题目','View the question')+'</a></p>'
    out+=disclosure('提示','Hint',q['hint'],'hint')
    out+='<details class="reveal solution"><summary>'+inline('参考答案与完整解析','Answer & full working')+'</summary><div class="reveal-body">'+lang(q['answer']['zh'],q['answer']['en'],cls='parallel')+references(q,sources)+'</div></details>'
    out+=f'<p class="topic-links"><a href="formulas.html#qmf-{q["formula"]}">'+inline('相关公式与简单例题','Related formula & example')+'</a></p></section>'
    return out

def paper_links():
    return '<nav class="paper-tabs" aria-label="试卷入口 / Papers"><a href="past-paper.html">'+inline('原卷逐题解析','Source paper')+'</a><a href="exam.html">'+inline('仿真模拟 A','Mock A')+'</a><a href="exam-ch3.html">'+inline('仿真模拟 B','Mock B')+'</a></nav>'

def blueprint():
    return '<details class="paper-guide"><summary>'+inline('本轮模拟卷怎样参考这份试卷','How the mocks follow this paper')+'</summary>'+lang('两套新卷都保持8道填空、4道选择、4道简答、1道20分计算的结构。A卷贴近原卷的基础概念、辨错、对易短证明和无限深阱；B卷用相同考法扩展到课件中的概率流、箱归一化、δ分布、完全集与角动量叠加态。没有把原卷未出现的繁长推导当作主体。','Both new papers retain eight fill-ins, four choices, four short answers and one 20-point calculation. A mirrors core concepts, error identification, a short commutator proof and an infinite well. B uses the same question forms to cover current, box normalization, delta distributions, complete sets and angular superpositions from the slides.')+lang('题目与考点可重合，表达和计算任务重新编写；这是一份拼卷提供的风格样本，不足以据此断言今后考试范围或命题概率。','Topics may overlap, but wording and calculation tasks are newly authored. One assembled source paper supports a style model, not predictions about a future examination.')+'</details>'

def page(title,questions,sources,kind,collection=False):
    past=kind=='past'
    if past:
        meta=('用户提供的往年题拼卷《课堂检测(1)》 · 2页 · 17题','User-supplied assembled past questions, Classroom Check (1) · 2 pages · 17 questions')
        notice=('题目按原卷顺序完整转录，统一排字与公式记号；新增英译、提示、解析和参考分配不是学校官方答案。前三类标题的“5′”按每小题5分解释：40＋20＋20＋20＝100；原PDF未另列总分说明。','Questions are fully transcribed in source order with normalized typography. Translations, hints, explanations and suggested marking are newly written, not an official key. Reading “5′” as five points per question gives 40+20+20+20=100; the PDF does not separately state a total.')
    else:
        meta=('依原卷考法重新编写 · 17题 · 满分100分 · 建议自测90分钟（非原卷规定）','Newly authored in the source paper’s style · 17 questions · 100 points · Suggested practice time: 90 minutes, not specified by the source')
        notice=('新编练习，参考原卷题型与课件考点，不是往年真题或预测卷。题目、提示与解答共用一份来源；保留原卷解析作为对照。','New practice based on the source paper’s question forms and the slides. These are neither past questions nor predictions. Questions, hints and solutions share one source; compare with the transcribed paper.')
    body='<main class="exam-page"><article class="exam-paper">'+paper_links()+'<h1>'+inline(*title)+'</h1>'+lang(*meta,cls='exam-meta')+lang(*notice,cls='ai-note')
    body+=lang('先独立作答；提示和完整解析分别点击展开，初次打开均隐藏。出处放在解析末尾，可继续展开核对。所有课件页码均按PDF物理页序，教材同时列书内页与PDF页。','Attempt the question first. Hints and full solutions start closed and open independently. Expand references at the end of a solution to check its basis. Slide references use physical PDF order; textbook references also give printed pages.',cls='exam-instructions')
    body+='<div class="exam-actions">'
    if not collection:body+='<button type="button" data-print="questions">'+inline('打印题目','Print questions')+'</button>'
    body+='<button type="button" data-print="solutions">'+inline('打印含解析版','Print with solutions')+'</button><button type="button" data-close-reveals>'+inline('收起提示和解析','Close hints & solutions')+'</button>'
    if past:body+='<a class="paper-download" href="assets/classroom-check.pdf" target="_blank" rel="noopener">'+inline('查看原卷PDF','Open source PDF')+'</a>'
    body+='</div>'+blueprint()
    if kind=='mock_a':body+='<p class="topic-links"><a href="answers.html">'+inline('按题查阅A卷答案','A solution collection')+'</a></p>'
    headings=[('一、填空题 · 每题5分，共40分','I. Fill in the blanks · 5 each, 40 points'),('二、选择题 · 每题5分，共20分','II. Multiple choice · 5 each, 20 points'),('三、简答题 · 每题5分，共20分','III. Short answers · 5 each, 20 points'),('四、计算题 · 20分','IV. Calculation · 20 points')]
    body+='<nav class="exam-toc" aria-label="试卷目录 / Exam sections">'+''.join(f'<a href="#sec{i}">'+inline(*h)+'</a>' for i,h in enumerate(headings,1))+'</nav>'
    for i,h in enumerate(headings,1):body+=f'<h2 id="sec{i}">'+inline(*h)+'</h2>'+''.join(card(q,sources,collection) for q in questions if q['section']==i)
    body+=lang('本页解析以课件为主，教材补充推导与限制条件。额外边界说明用于避免错误推广，不要求把全部说明原样写进简答题。','Solutions prioritize the slides; the textbook supplies supporting derivations and assumptions. Extra boundary notes prevent overgeneralization and need not all be copied into an exam response.',cls='exam-meta')+'</article></main>'
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title[0]+'</title></head><body>'+body+'</body></html>'

def build():
    data=json.loads((ROOT/'data/papers.json').read_text());sources=json.loads((ROOT/'data/paper-sources.json').read_text())
    configs=[('past','past-paper',('往年题拼卷 · 完整解析','Assembled past paper · Full solutions')),('mock_a','exam',('仿真模拟 A · 基础与无限深阱','Mock A · Fundamentals & infinite well')),('mock_b','exam-ch3',('仿真模拟 B · 课件扩展覆盖','Mock B · Broader slide coverage'))]
    for kind,name,title in configs:
        qs=data[kind]
        assert len(qs)==17 and sum(q['points'] for q in qs)==100
        assert [sum(q['section']==s for q in qs) for s in [1,2,3,4]]==[8,4,4,1]
        (ROOT/f'{name}.source.html').write_text(page(title,qs,sources,kind))
    (ROOT/'answers.source.html').write_text(page(('模拟 A · 按题查阅参考解答','Mock A · Solution collection'),data['mock_a'],sources,'mock_a',True))
if __name__=='__main__':build()
