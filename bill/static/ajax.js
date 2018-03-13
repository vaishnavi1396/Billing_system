$(document).ready(function(){
    $("button").click(function(){
        var value=$("#search_id").val()
        alert("Getting the medicine name "+value);
        if(value=="")
        {
            alert("Enter the medicine name");
            exit;
        }
        else if(value==NotExists)
        {
        alert("Medicine not found")
        }
        else{
         $.get("http://127.0.0.1:5000/search?medicine="+value, function(data, status){
            alert("Data: " + data + "\nStatus: " + status);
        });
        }
    });
});
