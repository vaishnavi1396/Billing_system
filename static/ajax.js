$(document).ready(function(){
        $("#add").click(function(){

        var count=$("#count").text();
        count=parseInt(count)
        count=count+1
        var med_name=$("#txtSearch").val()
        alert("adding medicine is" +med_name);
        //alert(value)

        if(med_name=="")
        {
            alert("Enter the medicine name");

        }
        else{
            $.get("http://127.0.0.1:5000/add?medicine="+med_name, function(data, status){
                    alert("Data: " + data + "\nStatus: " + status);
                    if(status.trim() === "success".trim())
                    {

                    var markup = "<tr><td>"+(count).toString()+"</td><td>"+med_name+"</td><td> </td><td> </td><td> </td><td> </td><td> </td><td> </td></tr>";
                    $("#count").text(count.toString())
                    $("#rows").append(markup);

                    }
                });
        }
        });

        $("#txtSubmit").click(function(){
        var value=$("#txtSearch").val()
        alert("Getting the medicine name "+value);
        if(value=="")
        {
            alert("Enter the medicine name");
        }
        else{
            $.get("http://127.0.0.1:5000/search?medicine="+value, function(data, status){
                    alert("Data: " + data + "\nStatus: " + status);
                });
            }
        });
});
