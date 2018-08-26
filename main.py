import mistune
import sys

class KanbanRenderer(mistune.Renderer):
    closeHeader = False
    openList = True
    colors = ['is-warning', 'is-info', 'is-success', 'is-link', 'is-primary', 'is-danger']
    headerCnt = 0

    def header(self, text, level, raw=None):
        html = ""
        if level == 3:
            if not self.closeHeader:
                self.closeHeader = True
            else:
                html += "</div></div>"

            html += """<div class="column is-narrow is-one-third">
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
            html += """
            <nav class="navbar is-transparent">
                <div class="navbar-brand">
                    <a class="navbar-item" href="https://bulma.io">
                    <img src="https://bulma.io/images/bulma-logo.png" alt="Bulma: a modern CSS framework based on Flexbox" width="112" height="28">
                    </a>
                <div class="navbar-menu">
                    <div class="navbar-start">
                    <a class="navbar-item" href="https://bulma.io/">
                        %s
                    </a>
                    <div class="navbar-item has-dropdown is-hoverable">
                        <a class="navbar-link" href="/documentation/overview/start/">
                        Other boards
                        </a>
                        <div class="navbar-dropdown is-boxed">
                        <a class="navbar-item" href="/documentation/overview/start/">
                            Overview
                        </a>
                        <a class="navbar-item" href="https://bulma.io/documentation/modifiers/syntax/">
                            Modifiers
                        </a>
                        <a class="navbar-item" href="https://bulma.io/documentation/columns/basics/">
                            Columns
                        </a>
                        <a class="navbar-item" href="https://bulma.io/documentation/layout/container/">
                            Layout
                        </a>
                        <a class="navbar-item" href="https://bulma.io/documentation/form/general/">
                            Form
                        </a>
                        </div>
                    </div>
                    </div>
                </div>
                </nav>
                <div class="container">
                    <div class="columns is-multiline">
            """ % text
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
        if ': ' not in body:
            raise Exception('Missing title delimiter \': \'')
        idx = body.index(': ')
        title = body[:idx]
        content = body[idx+1:]
        html = ""
        if self.openList:
            html += '<div class="box">'
            self.openList = False
        html += """<div class="content">
                    <strong>%s</strong>
                    <br>
                        %s
                    <hr>
                </div>""" %(title, content)
        return html


if __name__ == '__main__':
    renderer = KanbanRenderer(escape=False)
    markdown = mistune.Markdown(renderer=renderer)
    with open('./board.md', 'r') as f:
        content = f.read()
    body = markdown(content)
    result = """
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>PUT TITLE OR DESC</title>
    <link rel="stylesheet" href="https://bulma.io/css/bulma-docs.min.css?v=201808261416">
    </head>
    <body>
    """ + body + """
    </body></html>
    """

    print(result)
