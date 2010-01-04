from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1262617303.39873
_template_filename='/data/home/mpetersen/workspace/vault/src/vault/vault/templates/resources/details.xtpl'
_template_uri='/resources/details.xtpl'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<div class="content">\n        <h2> {title} </h2>\n        <strong style="display: none">{name}</strong>\n        <p>Created at {created}</p>\n        <p>Modified at {modified}</p>\n        <p>\n          {description}\n        </p>\n</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


