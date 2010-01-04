from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1262567333.0565641
_template_filename='/Users/mpeter/Documents/workspace/vault/src/vault/vault/templates/resource/index.mako'
_template_uri='/resource/index.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n\n')
        # SOURCE LINE 6
        for resource in c.resources:
            # SOURCE LINE 7
            __M_writer(u'<div class="content">\n        <h2> ')
            # SOURCE LINE 8
            __M_writer(escape(resource.title))
            __M_writer(u' </h2>\n        <strong style="display: none">')
            # SOURCE LINE 9
            __M_writer(escape(resource.name))
            __M_writer(u'</strong>\n        <p>Created at ')
            # SOURCE LINE 10
            __M_writer(escape(resource.created))
            __M_writer(u'</p>\n        <p>Modified at ')
            # SOURCE LINE 11
            __M_writer(escape(resource.modified))
            __M_writer(u'</p>\n        <p>\n          ')
            # SOURCE LINE 13
            __M_writer(escape(resource.description))
            __M_writer(u'\n        </p>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'MyBlog Home')
        return ''
    finally:
        context.caller_stack._pop_frame()


