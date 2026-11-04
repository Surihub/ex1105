from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E

BASE = Path(__file__).parent
NS = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main', 'a':'http://schemas.openxmlformats.org/drawingml/2006/main', 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
def q(prefix, tag): return '{'+NS[prefix]+'}'+tag

def serialize(root): return E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

with ZipFile(BASE/'original.pptx') as archive:
    files = {name: archive.read(name) for name in archive.namelist()}
source = E.fromstring(files['ppt/slides/slide25.xml'])
body_source = source.xpath('//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]', namespaces=NS)[0]

def textbox(tree, identifier, x, y, w, h, lines, size=1600, code=False):
    shape = deepcopy(body_source)
    nv = shape.find('p:nvSpPr', NS)
    nv.find('p:cNvPr', NS).set('id', str(identifier))
    nv.find('p:cNvPr', NS).set('name', f'Content {identifier}')
    nv.find('p:nvPr', NS).clear()
    transform = shape.find('p:spPr/a:xfrm', NS)
    transform.find('a:off',NS).attrib.update({'x':str(int(x*914400)), 'y':str(int(y*914400))})
    transform.find('a:ext',NS).attrib.update({'cx':str(int(w*914400)), 'cy':str(int(h*914400))})
    tx=shape.find('p:txBody',NS)
    for old in list(tx): tx.remove(old)
    E.SubElement(tx,q('a','bodyPr'),wrap='square',lIns='0',rIns='0',tIns='0',bIns='0')
    E.SubElement(tx,q('a','lstStyle'))
    for text in lines:
        para=E.SubElement(tx,q('a','p'))
        props=E.SubElement(para,q('a','pPr'),marL='0',indent='0')
        spacing=E.SubElement(props,q('a','lnSpc'))
        E.SubElement(spacing,q('a','spcPct'),val='115000' if code else '135000')
        E.SubElement(props,q('a','buNone'))
        run=E.SubElement(para,q('a','r'))
        rpr=E.SubElement(run,q('a','rPr'),sz=str(size),lang='ko-KR')
        fill=E.SubElement(rpr,q('a','solidFill'))
        E.SubElement(fill,q('a','srgbClr'),val='262626')
        E.SubElement(rpr,q('a','latin'),typeface='Menlo' if code else 'Arial')
        E.SubElement(rpr,q('a','ea'),typeface='Arial')
        E.SubElement(run,q('a','t')).text=text or ' '
    tree.append(shape)

def new_slide(number, title, sections):
    root=deepcopy(source)
    title_sp=root.xpath('//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="title"]]',namespaces=NS)[0]
    title_sp.find('.//a:t',NS).text=title
    tree=root.find('p:cSld/p:spTree',NS)
    tree.remove(root.xpath('//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]',namespaces=NS)[0])
    for index, section in enumerate(sections): textbox(tree,500+index,**section)
    files[f'ppt/slides/slide{number}.xml']=serialize(root)
    rels=E.fromstring(files['ppt/slides/_rels/slide25.xml.rels'])
    for rel in rels:
        if rel.get('Type').endswith('/notesSlide'): rel.set('Target',f'../notesSlides/notesSlide{number}.xml')
    files[f'ppt/slides/_rels/slide{number}.xml.rels']=serialize(rels)
    notes=E.fromstring(files['ppt/notesSlides/notesSlide25.xml'])
    body=notes.xpath('//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]',namespaces=NS)
    if body:
        tx=body[0].find('p:txBody',NS)
        for para in tx.findall('a:p',NS): tx.remove(para)
        para=E.SubElement(tx,q('a','p'));run=E.SubElement(para,q('a','r'))
        E.SubElement(run,q('a','t')).text='출처: Streamlit 공식 문서, Session State. https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state'
    files[f'ppt/notesSlides/notesSlide{number}.xml']=serialize(notes)
    notesrels=E.fromstring(files['ppt/notesSlides/_rels/notesSlide25.xml.rels'])
    for rel in notesrels:
        if rel.get('Type').endswith('/slide'): rel.set('Target',f'../slides/slide{number}.xml')
    files[f'ppt/notesSlides/_rels/notesSlide{number}.xml.rels']=serialize(notesrels)

new_slide(26,'버튼을 누르면 코드가 다시 실행됩니다',[
    dict(x=.5,y=.95,w=9,h=.95,lines=['버튼 클릭이나 입력 변경 → 위에서 아래로 다시 실행', '일반 변수에 0을 대입하는 코드도 매번 실행됨'],size=1700),
    dict(x=.8,y=2.12,w=8.5,h=1.65,lines=['count = 0','if st.button("1 증가"):', '    count += 1', 'st.write("현재 값:", count)'],size=1600,code=True),
    dict(x=.5,y=3.85,w=9,h=1,lines=['여러 번 눌러도 1 → 1 → 1', '이전 값을 누적하려면 실행 사이에 값을 기억해야 함'],size=1700),
])
new_slide(27,'session_state로 이전 값 유지하기',[
    dict(x=.5,y=.95,w=9,h=.45,lines=['처음에만 만들기 → 버튼에서 변경하기 → 현재 값 표시하기'],size=1600),
    dict(x=.8,y=1.55,w=8.9,h=3.45,lines=['import streamlit as st','','if "count" not in st.session_state:', '    st.session_state.count = 0','','if st.button("1 증가"):', '    st.session_state.count += 1','','if st.button("초기화"):', '    st.session_state.count = 0','','st.write("현재 값:", st.session_state.count)'],size=1450,code=True),
])
new_slide(28,'session_state 확인 실습',[
    dict(x=.5,y=1.0,w=9,h=3.8,lines=[
        '1. 「1 증가」를 세 번 눌러 1 → 2 → 3 확인',
        '2. 「초기화」를 눌러 0으로 돌아가는지 확인',
        '3. 첫 if문을 없애고 매번 0을 대입하면 어떻게 될까요?',
        '',
        '응용: 랜덤 추출 기록은 숫자 대신 리스트에 누적',
        '현재 사용자 세션 안에서 값을 유지함',
        '새로고침하거나 연결이 끊어지면 초기화될 수 있음',
        '영구 보관할 기록은 CSV 파일이나 DB에 별도 저장',
    ],size=1600),
])
pres=E.fromstring(files['ppt/presentation.xml'])
rels=E.fromstring(files['ppt/_rels/presentation.xml.rels'])
slides=pres.find('p:sldIdLst',NS)
maxid=max(int(s.get('id')) for s in slides)
used={r.get('Id') for r in rels}
for offset,number in enumerate([26,27,28],1):
    rid=f'rIdSessionState{offset}'
    assert rid not in used
    E.SubElement(rels,'{'+REL+'}Relationship',Id=rid,Type=NS['r']+'/slide',Target=f'slides/slide{number}.xml')
    item=E.Element(q('p','sldId'),id=str(maxid+offset))
    item.set(q('r','id'),rid)
    slides.insert(24+offset-1,item)
files['ppt/presentation.xml']=serialize(pres)
files['ppt/_rels/presentation.xml.rels']=serialize(rels)
ct=E.fromstring(files['[Content_Types].xml'])
for number in [26,27,28]:
    for kind,mime in [('slides','slide'),('notesSlides','notesSlide')]:
        E.SubElement(ct,'{'+CT+'}Override',PartName=f'/ppt/{kind}/{mime}{number}.xml',ContentType=f'application/vnd.openxmlformats-officedocument.presentationml.{mime}+xml')
files['[Content_Types].xml']=serialize(ct)
if 'docProps/app.xml' in files:
    app=E.fromstring(files['docProps/app.xml'])
    for item in app:
        if E.QName(item).localname=='Slides': item.text='28'
    files['docProps/app.xml']=serialize(app)
with ZipFile(BASE/'updated.pptx','w',ZIP_DEFLATED) as out:
    for name,data in files.items(): out.writestr(name,data)
print('28 slides: new material inserted before the closing slide')
