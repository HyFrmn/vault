<%inherit file="/base.mako" />

<%def name="title()">MyBlog Home</%def>


% for resource in c.resources:
<div class="content">
        <h2> ${resource.title} </h2>
        <strong style="display: none">${resource.name}</strong>
        <p>Created at ${resource.created}</p>
        <p>Modified at ${resource.modified}</p>
        <p>
          ${resource.description}
        </p>
</div>
% endfor
