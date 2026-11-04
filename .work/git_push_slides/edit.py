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

R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
for number in [29,30,31]:
    files[f'ppt/slides/slide{number}.xml']=files['ppt/slides/slide25.xml']
    rels=E.fromstring(files['ppt/slides/_rels/slide25.xml.rels'])
    for rel in rels:
        if rel.get('Type').endswith('/notesSlide'): rel.set('Target',f'../notesSlides/notesSlide{number}.xml')
    files[f'ppt/slides/_rels/slide{number}.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
    notes=E.fromstring(files['ppt/notesSlides/notesSlide25.xml'])
    body=notes.xpath('//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]',namespaces=NS)[0]
    tx=body.find('p:txBody',NS)
    for p in tx.findall('a:p',NS): tx.remove(p)
    p=E.SubElement(tx,q('a','p'));r=E.SubElement(p,q('a','r'))
    E.SubElement(r,q('a','t')).text='출처: GitHub 공식 문서. https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github ; https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository ; https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository'
    files[f'ppt/notesSlides/notesSlide{number}.xml']=E.tostring(notes,xml_declaration=True,encoding='UTF-8',standalone=True)
    rels=E.fromstring(files['ppt/notesSlides/_rels/notesSlide25.xml.rels'])
    for rel in rels:
        if rel.get('Type').endswith('/slide'): rel.set('Target',f'../slides/slide{number}.xml')
    files[f'ppt/notesSlides/_rels/notesSlide{number}.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)

slide(29,'처음 올리기: 빈 저장소에 연결',[
    dict(x=.5,y=.95,w=9,h=.75,lines=['GitHub에서 README 없이 빈 저장소를 만듭니다.', '올릴 앱 파일이 있는 폴더에서 터미널을 엽니다.'],size=1650),
    dict(x=.5,y=1.95,w=9,h=2.3,lines=['git init','git add .','git commit -m "첫 앱 업로드"','git branch -M main','git remote add origin https://github.com/USERNAME/REPO.git','git push -u origin main'],size=1350,code=True,fill='F5F5F5'),
    dict(x=.5,y=4.45,w=9,h=.45,lines=['USERNAME/REPO는 내 계정과 저장소 이름으로 바꾸세요.'],size=1550,color='B3261E',bold=True),
    dict(x=.85,y=5.0,w=8.6,h=.3,lines=['init: Git 관리 시작   ·   origin: 연결할 GitHub 저장소의 별명   ·   -u: 다음부터 git push만으로 전송'],size=1200,color='666666'),
])
slide(30,'파일이 이미 있는 저장소라면?',[
    dict(x=.5,y=.95,w=9,h=.75,lines=['먼저 clone으로 기존 저장소를 가져옵니다.', '그 폴더 안에서 앱 파일을 넣거나 수정한 뒤 올립니다.'],size=1650),
    dict(x=.5,y=1.95,w=9,h=2.3,lines=['git clone https://github.com/Surihub/hello-streamlit-0.git','cd hello-streamlit-0','# 여기서 앱 파일을 넣거나 수정하고 저장합니다.','git add .','git commit -m "수학 실습 앱 추가"','git push origin main'],size=1350,code=True,fill='F5F5F5'),
    dict(x=.5,y=4.45,w=9,h=.45,lines=['hello-streamlit-0에는 파일이 있으므로 이 방법을 사용합니다.'],size=1550,color='B3261E',bold=True),
    dict(x=.85,y=5.0,w=8.6,h=.3,lines=['이미 Codespaces에서 저장소를 열었다면 clone은 생략하고, 해당 앱 폴더에서 수정하면 됩니다.'],size=1250,color='666666'),
])
slide(31,'수정한 뒤에는 이 세 줄',[
    dict(x=.5,y=.95,w=9,h=.55,lines=['연결된 앱 폴더에서 코드를 고치고 저장한 뒤 실행합니다.'],size=1750),
    dict(x=.5,y=1.85,w=6.0,h=1.6,lines=['git add .','git commit -m "안내 문구 수정"','git push origin main'],size=1650,code=True,fill='F5F5F5'),
    dict(x=6.85,y=1.95,w=2.6,h=1.6,lines=['변경한 파일 담기','내 컴퓨터에 이력 저장','GitHub로 전송'],size=1600),
    dict(x=.5,y=3.95,w=9,h=.55,lines=['수정·저장 → add → commit → push'],size=2200,color='B3261E',bold=True),
    dict(x=.5,y=4.75,w=9,h=.4,lines=['commit 메시지에는 무엇을 바꿨는지 적습니다. git status로 현재 상태를 확인할 수 있습니다.'],size=1450),
])
pres=E.fromstring(files['ppt/presentation.xml'])
rels=E.fromstring(files['ppt/_rels/presentation.xml.rels'])
ids=pres.find('p:sldIdLst',NS)
maxid=max(int(s.get('id')) for s in ids)
ct=E.fromstring(files['[Content_Types].xml'])
for index,number in enumerate([29,30,31],1):
    rid=f'rIdGitPush{index}'
    assert not any(rel.get('Id')==rid for rel in rels)
    E.SubElement(rels,'{'+PKG+'}Relationship',Id=rid,Type=R+'/slide',Target=f'slides/slide{number}.xml')
    item=E.SubElement(ids,q('p','sldId'),id=str(maxid+index));item.set('{'+R+'}id',rid)
    for kind,mime in [('slides','slide'),('notesSlides','notesSlide')]:
        E.SubElement(ct,'{'+CT+'}Override',PartName=f'/ppt/{kind}/{mime}{number}.xml',ContentType=f'application/vnd.openxmlformats-officedocument.presentationml.{mime}+xml')
for name,root in [('ppt/presentation.xml',pres),('ppt/_rels/presentation.xml.rels',rels),('[Content_Types].xml',ct)]:
    files[name]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(BASE/'updated.pptx','w',ZIP_DEFLATED) as z:
    for name,data in files.items(): z.writestr(name,data)
print('마지막에 Git 명령어 3장 추가 완료: 총 31장')
