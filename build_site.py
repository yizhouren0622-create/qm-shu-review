# -*- coding: utf-8 -*-
"""Build static bilingual pages with pre-rendered, offline MathML.
Install build dependencies with: python -m pip install -r requirements-build.txt
"""
from __future__ import annotations
import re
from pathlib import Path
from lxml import html as H,etree
from latex2mathml.converter import convert
from build_exams import build,inline,lang
ROOT=Path(__file__).resolve().parent
NAV_LINKS=[('index.html','首页','Home'),('review.html','复习课','Review'),('examples.html','课件例题','Examples'),('formulas.html','公式与应用','Formulas'),('exam.html','综合卷','Exam'),('answers.html','答案','Solutions'),('exam-ch3.html','第3章卷','Chapter 3')]
NAV='<header class="site-top" id="siteTop"><div class="site-top-inner"><a class="site-brand" href="index.html">'+inline('量子力学复习','Quantum review')+'</a><button type="button" class="site-menu-btn" aria-expanded="false" aria-controls="siteLinks">'+inline('菜单','Menu')+'</button><nav class="site-links" id="siteLinks" aria-label="站点导航 / Site navigation">'+''.join(f'<a href="{p}" data-page="{p}">'+inline(z,e)+'</a>' for p,z,e in NAV_LINKS)+'</nav></div></header>'
TOOLBAR='<div class="site-tools"><label for="site-language">'+inline('语言','Language')+'</label><select id="site-language" aria-label="语言 / Language"><option value="both">中英对照 / Bilingual</option><option value="zh">中文</option><option value="en">English</option></select><a href="study.html">'+inline('学习路线与符号表','Study map & notation')+'</a></div>'
FOOTER='<footer class="site-footer">'+inline('上海大学微电子 · Chapter 01–03 复习材料。公式已预渲染，无需外部公式服务；页面及资源保存到本地后可离线阅读。','SHU Microelectronics · Chapters 01–03 revision. Equations are pre-rendered; saved pages and assets can be read offline.')+'</footer>'
HEAD_EXTRA='<meta name="color-scheme" content="light"><meta name="theme-color" content="#efeae2"><link rel="stylesheet" href="assets/site.css">'
MATH_PATTERN=re.compile(r'\$\$(.+?)\$\$|\\\[(.+?)\\\]|(?<!\\)\$([^$\n]+?)\$|\\\((.+?)\\\)',re.S)

def strip_old_katex_and_scripts(s):
    s=re.sub(r'<link[^>]+katex[^>]*>\s*','',s,flags=re.I)
    s=re.sub(r'<script[^>]*(?:katex|auto-render)[^>]*>.*?</script>\s*','',s,flags=re.I|re.S)
    return re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded".*?</script>\s*','',s,flags=re.S)

def mathml_page(s):
    doc=H.document_fromstring(s)
    slots=[]
    for el in doc.iter():
        if not isinstance(el.tag,str):continue
        skip=el.tag in ('script','style','math','annotation','pre','code') or any(a.tag in ('math','script','style','pre','code') for a in el.iterancestors())
        if not skip and el.text and MATH_PATTERN.search(el.text):slots.append((el,'text',el.text))
        if el.tail and MATH_PATTERN.search(el.tail) and not any(a.tag in ('math','script','style','pre','code') for a in el.iterancestors()):slots.append((el,'tail',el.tail))
    for el,slot,text in slots:
        parts=[];pos=0
        for m in MATH_PATTERN.finditer(text):
            parts.append(text[pos:m.start()]);display=m.group(1) is not None or m.group(2) is not None
            tex=next(g for g in m.groups() if g is not None).strip()
            try: converted=convert(tex,display='block' if display else 'inline')
            except Exception as e:raise RuntimeError(f'Math conversion failed: {tex}') from e
            if '<merror' in converted:raise RuntimeError('Math error: '+tex)
            # Keep the original TeX in an annotation for copy/export and inspection.
            math=H.fromstring(converted)
            sem=H.Element('semantics')
            for c in list(math):sem.append(c)
            ann=H.Element('annotation',encoding='application/x-tex');ann.text=tex;sem.append(ann);math.append(sem)
            wrap=H.Element('div' if display else 'span',attrib={'class':'math-display' if display else 'math-inline'});wrap.append(math)
            parts.append(wrap);pos=m.end()
        parts.append(text[pos:])
        if slot=='text':
            el.text=parts[0];parent=el;idx=0
        else:
            el.tail=parts[0];parent=el.getparent();idx=parent.index(el)+1
        for j in range(1,len(parts),2):
            node=parts[j];node.tail=parts[j+1];parent.insert(idx,node);idx+=1
    return '<!DOCTYPE html>\n'+etree.tostring(doc,encoding='unicode',method='html')

def inject_chrome(s,title=None):
    s=strip_old_katex_and_scripts(s)
    if title:s=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',s,count=1,flags=re.S)
    if not re.search(r'<meta[^>]+viewport',s,re.I):s=s.replace('<head>','<head><meta name="viewport" content="width=device-width,initial-scale=1">',1)
    # Last in the head so shared spacing and language rules override legacy inline CSS.
    s=s.replace('</head>',HEAD_EXTRA+'</head>',1)
    s=re.sub(r'<body([^>]*)>',r'<body\1>'+NAV+TOOLBAR,s,count=1,flags=re.I)
    s=s.replace('</body>',FOOTER+'<script defer src="assets/site.js"></script></body>',1)
    s=s.replace('../前三章知识梳理.html','formulas.html').replace('模拟卷_答案.html','answers.html').replace('模拟卷.html','exam.html')
    return mathml_page(s)

def build_hub():
    cards=[('review.html','复习课（带图精讲）','Illustrated review','逐节梳理概念，拓展内容单独标明。','Concepts explained in sequence; supplementary content is labeled.'),('examples.html','课件例题全解','Slide examples','保留中文完整推导，附英文要点与公式链接。','Full Chinese derivations with English essentials and formula links.'),('formulas.html','公式与应用','Formulas in practice','35 组公式，含条件、符号和可展开的简单例题。','35 formula groups, assumptions, symbols and expandable examples.'),('exam.html','综合模拟卷','Comprehensive mock exam','24 题 · 100 分 · 逐题展开提示和答案。','24 questions · 100 points · reveal hints and solutions per question.'),('answers.html','综合卷答案','Reference solutions','与试卷共用答案来源，可按题查阅。','A question-by-question collection using the same source as the paper.'),('exam-ch3.html','第3章力学算符卷','Chapter 3 operators exam','8 题 · 100 分 · 提示和答案默认收起。','8 questions · 100 points · hints and answers start closed.'),('study.html','学习路线与符号表','Study map & notation','课件页码、概念、公式、例题和练习相互连接。','Connect slide pages, concepts, formulas, examples and practice.')]
    body='<main class="hub"><div class="hub-card"><h1>'+inline('量子力学前三章 · 复习站','Quantum mechanics · Chapters 01–03')+'</h1>'+lang('上海大学微电子学院课程课件复习资料。保留图文讲解，支持中文、English 和中英对照。','Revision based on the SHU Microelectronics course slides. Choose Chinese, English or bilingual reading.',cls='lead')+'<div class="hub-grid">'
    for p,z,e,d,f in cards:body+=f'<a class="hub-link" href="{p}"><strong>'+inline(z,e)+'</strong>'+inline(d,f)+'</a>'
    body+='</div>'+lang('建议先看概念与课件例题，再做模拟卷。试卷与参考答案为 AI 编写的自测材料；课件范围与拓展阅读已区分。复习建议不代表教师公布的考试要求。','Read concepts and slide examples, then attempt the mock exams. Papers and solutions are AI-authored practice. Slide coverage and supplementary reading are distinguished; study suggestions are not official examination requirements.',cls='hub-note')+'</div></main>'
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>量子力学复习站 · SHU</title></head><body>'+body+'</body></html>'

def main():
    build()
    for src in sorted(ROOT.glob('*.source.html')):
        out=src.name.replace('.source','');s=inject_chrome(src.read_text())
        (ROOT/out).write_text(s);print('wrote',out,len(s.encode()))
    (ROOT/'index.html').write_text(inject_chrome(build_hub()))
    (ROOT/'.nojekyll').write_text('')
if __name__=='__main__':main()
