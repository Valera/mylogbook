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
</body>
</html>
