<html>
  <head>
    <title>Index of /{{relative_path}}</title>
  </head>
  <body bgcolor="white">
    <h1>Index of /{{relative_path}}</h1><br/>
    <hr/>
    <pre>
%if relative_path:
<a href="../">../</a>
%end
%for (filename, mdate, size) in entries:
<a href="{{filename}}">{{filename}}</a>{{" " * (60 - len(filename))}}{{mdate}}    {{size}}
%end
    </pre>
    <hr/>
  </body>
</html>
