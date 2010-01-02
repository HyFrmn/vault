<%inherit file="/base.mako" />

<%def name="title()">MyBlog Home</%def>

<p>${c.projects.count()} new projects!</p>

% for project in c.projects:
<p class="content" style="border-style:solid;border-width:1px">
        <span class="h3"> ${project.title} </span>
        <span class="h4">Created at ${project.created}</span>
        <br>
          ${project.description}
</p>
% endfor
