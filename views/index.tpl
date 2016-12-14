<html>
<head>
    <meta charset='UTF-8'/>
</head>
<body>
    <table border="1">
%for i in range(10):
        <tr>
%   for j in range(10):
            <td>x</td>
%   end
        </tr>
%end
    </table>
    <a href="/static/register.html">Register</a> <br>
    <a href="/static/signin.html">Sign in</a> <br>
    <a href="/info">info</a> <br>
{{text}} <br>
Username:<br>
{{user_name}}
</body>
</html>
