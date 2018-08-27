import mistune
import shutil
import os
import glob

class KanbanRenderer(mistune.Renderer):
    closeHeader = False
    openList = True
    colors = ['is-warning', 'is-info', 'is-success', 'is-link', 'is-primary', 'is-danger']
    headerCnt = 0
    singleHeaderCheck = False
    strippedNames = []

    def header(self, text, level, raw=None):
        html = ""
        if level == 3:
            if not self.closeHeader:
                self.closeHeader = True
            else:
                html += "</div></div>"

            html += """<div class="column">
                <div class="message %s">
                    <header class="message-header">
                        <p class="message-header-title">
                            %s
                        </p>
                    </header>
                    <div class="message-content">
            <div>
            """ % (self.colors[self.headerCnt], text)
            self.headerCnt += 1
        elif level == 1:
            if self.singleHeaderCheck:
                raise Exception('Only a single h1 allowed. Specify multiple projects in different files.')
            else:
                self.singleHeaderCheck = True
            boards = self.strippedNames
            html += """
            <div class="hero-head">
                <div class="container">
                    <nav class="navbar is-transparent is-boxed">
                        <div class="navbar-menu">
                            <div class="navbar-end">
                                <a class="navbar-item">
                                    %s
                                </a>""" % text
            if len(boards) > 0:
                html += """<div class="navbar-item has-dropdown is-hoverable">
                                <a class="navbar-link">
                                Other boards
                                </a>"""
                for item in boards:
                    html += """
                                <div class="navbar-dropdown is-boxed">
                                    <a class="navbar-item" href="/%s.html">
                                        %s
                                    </a>
                                </div>
                            </div>""" % (item, item.replace('_', ' '))
            html += """</div></div></nav></div></div>
            <div class="hero-body">
                <div class="container">
                    <div class="columns is-multiline">
            """
            self.headerCnt = 0
        else:
            raise Exception('Only header of level 1 and 3 are supported')
        return html

    def list(self, *args, **kwargs):
        self.openList = True
        return '</div></div>' + super().list(*args, **kwargs)

    def codespan(self, tag, **kwargs):
        color = ''
        if '|' in tag:
            cnt = tag.index('|')
            color = tag[:cnt]
            if 'is-' not in color[:3]:
                color = 'is-' + color
            tag = tag[cnt+1:]
            if color not in self.colors:
                raise Exception('Not a valid Bulma color tag')

        html = '<span class="tag is-small %s">%s</span>' % (color, tag)
        return html

    def list_item(self, body, ordered=True):
        html = ""
        if self.openList:
            html += '<div class="box">'
            self.openList = False
        else:
            html += "<hr>"

        if ': ' in body:
            idx = body.index(': ')
            title = body[:idx]
            content = body[idx+1:]
            html += """<div class="content">
                            <strong>%s</strong>
                            <br>
                            %s
                        </div>
                    """ %(title, content)
        else:
            html += """<div class="content">
                            <strong>%s</strong>
                        </div>
                    """ %(body)

        return html

def process_markdown(fp, current, strippedNames):
    cs = set(); cs.add(current)
    renderer = KanbanRenderer(escape=False)
    renderer.strippedNames = tuple(sorted(set(strippedNames) - cs)) # ugly
    markdown = mistune.Markdown(renderer=renderer)
    with open(fp, 'r') as f:
        content = f.read()
    body = markdown(content)
    result = """<html lang="en">
    <head>
    <meta charset="utf-8">
     <meta name="description" content="Cartello, markdown kanban board">
    <title>Cartello</title>
    <link rel="stylesheet" href="./bulma.min.css">
    </head>
    <body>
    <section class="hero is-fullheight is-light is-bold">
    """ + body + """
    </div></div></div></div></div>
    <div class="hero-foot">
            <div class="section">
                <div class="container">
                    <div class="content has-text-centered has-text-grey">
                        <p> Create kanban boards to projects from flat markdown files.</p>
                        <a href="https://github.com/framecca/cartello" class="is-click">
                            Fork it on Github.
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </body></html>
    """

    return result

if __name__ == '__main__':
    outputDir = 'site'
    files = tuple(sorted(glob.glob('boards/*.md')))
    strippedNames =  [''.join(fp.split('/')[1:])[:-3] for fp in files]

    for f in glob.glob(outputDir + '/*'):
        os.remove(f)
    shutil.copyfile('./css/bulma.min.css', outputDir + '/bulma.min.css')
    for fp, name in zip(files, strippedNames):
        text = process_markdown(fp, name, strippedNames)
        print("Processing '" + name + "'")
        with open(outputDir + '/' + name +'.html', 'w') as out:
            out.write(text)
