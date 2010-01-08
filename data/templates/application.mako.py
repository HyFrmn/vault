from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1262979381.4058311
_template_filename='/data/home/mpetersen/workspace/vault/src/vault/vault/templates/application.mako'
_template_uri='/application.mako'
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
        __M_writer(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n    <head>\n        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n        <title>Vault</title>\n        <!-- ** CSS ** -->\n        <!-- base library -->\n        <link rel="stylesheet" type="text/css" href="/ext/ext-all.css" />\n \n        <!-- overrides to base library -->\n \n        <!-- ** Javascript ** -->\n        <!-- ExtJS library: base/adapter -->\n        <script type="text/javascript" src="/ext/ext-base.js"></script>\n        <!-- ExtJS library: all widgets -->\n        <script type="text/javascript" src="/ext/ext-all-debug.js"></script>\n        \n        <script type="text/javascript" src="/js/file-upload.js"></script>\n        \n        <link rel="stylesheet" type="text/css" href="/css/file-upload.css" />\n        <link rel="stylesheet" type="text/css" href="/css/vault.css" />\n        <!-- page specific -->\n        <script type="text/javascript" src="/js/application.js"></script>\n        <script type="text/javascript" src="/js/dialogs.js"></script>\n        <script type="text/javascript" src="/js/grids.js"></script>\n        <script type="text/javascript" src="/js/details.js"></script>\n        <script type="text/javascript" src="/js/panels.js"></script>\n        <script type="text/javascript" src="/js/components.js"></script>\n        <script type="text/javascript" src="/js/layout.js"></script>\n    </head>\n    <body>\n    </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


