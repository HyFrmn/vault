from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1262973889.7815299
_template_filename='/data/home/mpetersen/workspace/vault/src/vault/vault/templates/login.mako'
_template_uri='login.mako'
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
        __M_writer(u'<form method="POST" action="/login/submit">\n  Username: <input type="text" name="username" size="15" /><br />\n  Password: <input type="password" name="password" size="15" /><br />\n  <p><input type="submit" value="Login" /></p>\n</form>')
        return ''
    finally:
        context.caller_stack._pop_frame()


