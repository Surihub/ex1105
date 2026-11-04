from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import re
from lxml import etree as E

BASE=Path(__file__).parent
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def q(p,t): return '{'+NS[p]+'}'+t
with ZipFile(BASE/'original.pptx') as z:
    files={name:z.read(name) for name in z.namelist()}


def shape(tree, ident, x,y,w,h,lines,size=1700,color='262626',bold=False,code=False,fill=None):
    sp=E.SubElement(tree,q('p','sp'))
    nv=E.SubElement(sp,q('p','nvSpPr'))
    E.SubElement(nv,q('p','cNvPr'),id=str(ident),name=f'Lesson text {ident}')
    E.SubElement(nv,q('p','cNvSpPr'),txBox='1')
    E.SubElement(nv,q('p','nvPr'))
    props=E.SubElement(sp,q('p','spPr'))
    xf=E.SubElement(props,q('a','xfrm'))
    E.SubElement(xf,q('a','off'),x=str(int(x*914400)),y=str(int(y*914400)))
    E.SubElement(xf,q('a','ext'),cx=str(int(w*914400)),cy=str(int(h*914400)))
    geom=E.SubElement(props,q('a','prstGeom'),prst='rect');E.SubElement(geom,q('a','avLst'))
    if fill:
        sf=E.SubElement(props,q('a','solidFill'));E.SubElement(sf,q('a','srgbClr'),val=fill)
    else: E.SubElement(props,q('a','noFill'))
    ln=E.SubElement(props,q('a','ln'));E.SubElement(ln,q('a','noFill'))
    tx=E.SubElement(sp,q('p','txBody'))
    pad='110000' if fill else '0'
    E.SubElement(tx,q('a','bodyPr'),wrap='square',lIns=pad,rIns=pad,tIns=pad,bIns=pad)
    E.SubElement(tx,q('a','lstStyle'))
    for text in lines:
        p=E.SubElement(tx,q('a','p'))
        pp=E.SubElement(p,q('a','pPr'),marL='0',indent='0')
        spacing=E.SubElement(pp,q('a','lnSpc'));E.SubElement(spacing,q('a','spcPct'),val='125000')
        E.SubElement(pp,q('a','buNone'))
        chunks=re.split(r'(st\.session_state(?:\.count)?|"[^"]*"|\b(?:if|not|in|import|as)\b)',text) if code else [text]
        for chunk in chunks:
            if not chunk: continue
            ink=color
            if code:
                if chunk.startswith('st.session_state'): ink='B3261E'
                elif chunk.startswith('"'): ink='176A50'
                elif chunk in ['if','not','in','import','as']: ink='3758A5'
            run=E.SubElement(p,q('a','r'))
            rp=E.SubElement(run,q('a','rPr'),sz=str(size),lang='ko-KR',b='1' if bold else '0')
            sf=E.SubElement(rp,q('a','solidFill'));E.SubElement(sf,q('a','srgbClr'),val=ink)
            E.SubElement(rp,q('a','latin'),typeface='Menlo' if code else 'Arial')
            E.SubElement(rp,q('a','ea'),typeface='Arial')
            t=E.SubElement(run,q('a','t'));t.text=chunk
            t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')


def slide(number,title,sections):
    root=E.fromstring(files[f'ppt/slides/slide{number}.xml'])
    tree=root.find('p:cSld/p:spTree',NS)
    for sp in list(tree.findall('p:sp',NS)):
        ph=sp.find('p:nvSpPr/p:nvPr/p:ph',NS)
        if ph is not None and ph.get('type')=='title':
            sp.find('.//a:t',NS).text=title
        elif ph is None or ph.get('type')!='sldNum': tree.remove(sp)
    for i, section in enumerate(sections,500): shape(tree,i,**section)
    files[f'ppt/slides/slide{number}.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)

slide(26,'기억 기능이 없으면 어떻게 될까요?',[
    dict(x=.5,y=1.0,w=9,h=.5,lines=['버튼을 누를 때마다 코드가 맨 위부터 다시 실행됩니다.'],size=1800),
    dict(x=.5,y=1.75,w=5.55,h=1.85,lines=['count = 0','if st.button("1 증가"):', '    count += 1', 'st.write(count)'],size=1550,code=True,fill='F5F5F5'),
    dict(x=6.5,y=1.85,w=3,h=.4,lines=['세 번 눌렀는데…'],size=1700,bold=True),
    dict(x=6.5,y=2.45,w=3,h=.6,lines=['1 → 1 → 1'],size=2700,color='B3261E',bold=True),
    dict(x=.5,y=3.95,w=9,h=.5,lines=['count = 0도 매번 실행되어 이전 횟수가 지워집니다.'],size=1800),
    dict(x=.5,y=4.6,w=9,h=.45,lines=['이전 값을 기억해 두는 곳이 session_state입니다.'],size=1800,color='B3261E',bold=True),
])
slide(27,'session_state는 값을 기억하는 메모',[
    dict(x=.5,y=.96,w=9,h=.4,lines=['st.session_state.count  →  count라는 이름으로 기억한 값'],size=1800,bold=True),
    dict(x=.5,y=1.7,w=2.5,h=.5,lines=['1. 처음에만 만들기'],size=1700,color='B3261E',bold=True),
    dict(x=3,y=1.55,w=6.45,h=1.05,lines=['if "count" not in st.session_state:', '    st.session_state.count = 0'],size=1400,code=True,fill='F5F5F5'),
    dict(x=3,y=2.67,w=6.4,h=.4,lines=['count가 없을 때만 0을 넣습니다.'],size=1600),
    dict(x=.5,y=3.25,w=2.5,h=.5,lines=['2. 기억한 값 바꾸기'],size=1700,color='B3261E',bold=True),
    dict(x=3,y=3.12,w=6.45,h=.6,lines=['st.session_state.count += 1'],size=1400,code=True,fill='F5F5F5'),
    dict(x=.5,y=4.25,w=2.5,h=.5,lines=['3. 화면에 보여 주기'],size=1700,color='B3261E',bold=True),
    dict(x=3,y=4.12,w=6.45,h=.6,lines=['st.write(st.session_state.count)'],size=1400,code=True,fill='F5F5F5'),
])
slide(28,'실습: 누를 때마다 1씩 쌓기',[
    dict(x=.5,y=1.0,w=6.05,h=2.95,lines=['import streamlit as st','', 'if "count" not in st.session_state:', '    st.session_state.count = 0','', 'if st.button("1 증가"):', '    st.session_state.count += 1','', 'st.write(st.session_state.count)'],size=1400,code=True,fill='F5F5F5'),
    dict(x=6.95,y=1.15,w=2.5,h=.5,lines=['세 번 눌러 보세요'],size=1700,bold=True),
    dict(x=6.95,y=1.8,w=2.6,h=.65,lines=['1 → 2 → 3'],size=2500,color='176A50',bold=True),
    dict(x=6.95,y=2.8,w=2.6,h=.5,lines=['직접 바꿔 보기'],size=1700,bold=True),
    dict(x=6.95,y=3.4,w=2.6,h=.55,lines=['+= 1을 += 10으로'],size=1500),
    dict(x=.5,y=4.3,w=9,h=.45,lines=['응용: 뽑기 기록이나 퀴즈 점수도 같은 방법으로 누적합니다.'],size=1700),
    dict(x=.5,y=4.95,w=9,h=.35,lines=['사용자 세션에서 유지됩니다. 새로고침하면 초기화될 수 있어, 영구 보관은 CSV 등에 따로 저장합니다.'],size=1250,color='666666'),
])
with ZipFile(BASE/'updated.pptx','w',ZIP_DEFLATED) as z:
    for name,data in files.items(): z.writestr(name,data)
print('기존 3장을 쉬운 설명과 짧은 예제로 수정했습니다.')
