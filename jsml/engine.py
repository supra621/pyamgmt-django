class Element:
    pass


class Div(Element):
    pass


class Nav(Element):
    pass


class Table(Element):
    pass


class Tr(Element):
    pass


class JSONTemplate:
    """"""
    ALLOWED_TAGS = {
        'div',
        'footer',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'header',
        'li',
        'nav',
        'ol',
        'p',
        'section',
        'span',
        'table',
        'tbody',
        'td',
        'th',
        'thead',
        'tr',
        'ul'
    }
