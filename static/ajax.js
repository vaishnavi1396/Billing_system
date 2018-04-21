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
            $.get("http://127.0.0.1:5000/add?medicine=" +med_name, function(data, status){
                    alert("Data: " + data + "\nStatus: " + status);
                    if(status.trim() == "success".trim())
                    {
                    var markup = '<tr><td>'+(count).toString()+'</td><td>'+med_name+'</td><td>'+data.mfg_Date+' </td><td>'+data.exp_Date+' </td><td>'+data.cost+' </td><td><input type="number" min="0" max="100" value="0" size="2" style="width:50px" name="qty" id="qty"/> </td><td> </td></tr>';
                    $("#count").text(count.toString())
                    $("#rows").append(markup);

                    $("#qty").keyup(function(){
                    var value = $(this).val();
                    alert(value);
                    amount= data.cost*value
                    alert(amount)
                    });
                    }
                });
            }

        });
        $("#search").click(function(){
        var value=$("#txtSearch").val()
        alert("Getting the medicine name "+value);
        if(value=="")
        {
            alert("Enter the medicine name");
        }
        else{
            $.get("http://127.0.0.1:5000/search?medicine="+value, function(data, status){
                        console.log(data)

                        if(data.status==true){
                            alert("medicine exist")
                        }else{
                            alert("medicine does not exist")

                        }
                });
            }
        });

        $("#bill").click(function(){
        alert("Bill is ready")
        });
});
