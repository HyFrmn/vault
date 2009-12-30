from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1262195977.7527339
_template_filename='/data/home/mpetersen/workspace/vault/src/vault/vault/templates/project/index.html'
_template_uri='/project/index.html'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['title']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n<p>')
        # SOURCE LINE 3
        __M_writer(escape(c.projects.count()))
        __M_writer(u' new projects!</p>\n\n')
        # SOURCE LINE 5
        for project in c.projects:
            # SOURCE LINE 6
            __M_writer(u'<p class="content" style="border-style:solid;border-width:1px">\n        <span class="h3"> ')
            # SOURCE LINE 7
            __M_writer(escape(project.title))
            __M_writer(u' </span>\n        <span class="h4">Created at ')
            # SOURCE LINE 8
            __M_writer(escape(project.created))
            __M_writer(u'</span>\n        <br>\n          ')
            # SOURCE LINE 10
            __M_writer(escape(project.description))
            __M_writer(u'\n</p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'MyBlog Home')
        return ''
    finally:
        context.caller_stack._pop_frame()


