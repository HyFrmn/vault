from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1263192723.1155889
_template_filename='/Users/mpeter/Documents/workspace/vault/src/vault/vault/templates/application.mako'
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
        __M_writer(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n    <head>\n        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n        <title>Vault</title>\n        <!-- ** CSS ** -->\n        <!-- base library -->\n        <link rel="stylesheet" type="text/css" href="/ext/ext-all.css" />\n \n        <!-- overrides to base library -->\n \n        <!-- ** Javascript ** -->\n        <!-- ExtJS library: base/adapter -->\n        <script type="text/javascript" src="/ext/ext-base.js"></script>\n        <!-- ExtJS library: all widgets -->\n        <script type="text/javascript" src="/ext/ext-all-debug.js"></script>\n        \n        <script type="text/javascript" src="/js/file-upload.js"></script>\n        \n        <link rel="stylesheet" type="text/css" href="/css/file-upload.css" />\n        <link rel="stylesheet" type="text/css" href="/css/vault.css" />\n        <!-- page specific -->\n\n        <!-- Basics -->\n        <script type="text/javascript" src="/js/Vault.LayoutPanel.js"></script>\n        <script type="text/javascript" src="/js/Vault.Grid.js"></script>\n        <script type="text/javascript" src="/js/Vault.Details.js"></script>\n        <script type="text/javascript" src="/js/Vault.Dialog.js"></script>\n        <script type="text/javascript" src="/js/Vault.Actions.js"></script>\n\n        <!-- Form Fields -->\n        <script type="text/javascript" src="/js/Vault.ResourceLinkField.js"></script>\n        <script type="text/javascript" src="/js/Vault.FileUploadField.js"></script>\n\n        <!-- Panels -->\n        <script type="text/javascript" src="/js/Vault.AssetGrid.js"></script>\n        <script type="text/javascript" src="/js/Vault.TaskGrid.js"></script>\n        <script type="text/javascript" src="/js/Vault.VersionGrid.js"></script>\n        <script type="text/javascript" src="/js/Vault.CommentGrid.js"></script>\n\n        <script type="text/javascript" src="/js/Vault.ResourceDataView.js"></script>\n        <script type="text/javascript" src="/js/Vault.AssetDataView.js"></script>\n        <script type="text/javascript" src="/js/Vault.ProjectDashboard.js"></script>\n\n        <!-- Dialogs -->\n        <script type="text/javascript" src="/js/Vault.FormDialog.js"></script>\n        <script type="text/javascript" src="/js/Vault.RestfulFormDialog.js"></script>\n        <script type="text/javascript" src="/js/Vault.SelectResourceDialog.js"></script>\n\n        <!-- Action -->\n        <script type="text/javascript" src="/js/Vault.OpenFormDialog.js"></script>\n        <script type="text/javascript" src="/js/application.js"></script>\n\n    </head>\n    <body>\n    </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


