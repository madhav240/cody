import json
from parso import parse
from nbconvert import HTMLExporter
import nbformat
import os

def getdata(source):
    data = {
        'cimports': None,
        "imports": set(),
        "funcdefs": []
    }

    p = parse(source, version="3.8")

    cimp = []
    for imp in p.iter_imports():
        cimp.append(imp.get_code().replace("\n", ""))
        c0 = imp.children[0].value
        if c0 == "from":
            c1 = imp.children[1].get_code()
            c3 = imp.children[3].get_code().strip()
            if "(" not in c3:
                s = c3
            else:
                s = imp.children[4].get_code()
            for i in s.split(","):
                data['imports'].add(f"{c1}.{i}".replace(" ", ""))
        else:
            c1 = imp.children[1].get_first_leaf().get_code().split(",")
            for i in c1:
                data['imports'].add(i.strip())
    cimp.sort()
    data['cimports'] = "\n".join(cimp)

    for defs in p.iter_funcdefs():
        doc = defs.get_doc_node()
        if doc != None:
            doc = doc.value
        else:
            doc = ""
        data['funcdefs'].append({
            'name' : defs.children[1].get_code()[1:],
            'code' : doc
        })

    return data


def open_ipynb(source):
    j = json.loads(source)

    source = ""

    for cell in j['cells']:
        if cell['cell_type'] == "code":
            for s in cell['source']:
                source += s
    return getdata(source)


def getext(fname):
    return fname[fname.rfind("."):]

def gethtml(source, fname):
    ext = getext(fname)
    data = None
    if ext == ".ipynb":
        data = open_ipynb(source)
        html_exporter = HTMLExporter()
        html_exporter.theme = 'dark'
        nb = nbformat.reads(source, as_version=4)
        (body, resources) = html_exporter.from_notebook_node(nb)

        viewHTML = body[body.find("<body "):body.find("</body>")]
    elif ext == ".py":
        data = getdata(source)
        viewHTML = f"""<pre style="border:none"><code class="python">{source}</code></pre>"""

    analyzeHTML = f"""<pre style="border:none"><code class="python">{data['cimports']}</code></pre>"""
    return {
    "analyzeHTML" : analyzeHTML,
    "viewHTML" : viewHTML
    }
 
import pdoc

def getdoc(mod):

    html = None
    dot = mod.find(".")
    hx = ".html"
    package = mod
    mod = mod.replace(".", "/")
    path = "docs/" + mod

    if dot != -1:
        package = mod[:dot]

    if os.path.exists(path) == os.path.exists(path + hx):
        os.system("python -m pdoc --html --output-dir docs " + package)
    if os.path.exists(path + hx):
        html = open_html(path + hx)
    else:
        try:
            html = open_html(path + "/index.html")
        except:
            if package == mod:
                html = "$##$" + open_html(path[:path.rfind("/")] + "/index.html")
            else:
                html = "$##$" + open_html(path[:path.rfind("/")] + hx)
    return html

def open_html(path):
    with open(path, 'r', encoding="utf-8") as f:
        html = f.read()
        f.close()

    return html