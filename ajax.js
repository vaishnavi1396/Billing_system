$(document).ready(function(){
        $("#add").click(function(){
        var value=$("#count").text();
        value=parseInt(value)
        value=value+1
        alert(value)
        var markup = "<tr><td>"+(value+1).toString()+"</td><td> </td><td> </td><td> </td><td> </td><td> </td><td> </td></tr>";
        $("#count").text(value.toString())
        $("#rows").append(markup);
        });
        });
