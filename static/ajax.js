var bill_info=[];


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
                    var markup = '<tr><td>'+(count).toString()+'</td><td>'+med_name+'</td><td>'+data.mfg_Date+' </td><td>'+data.exp_Date+' </td><td>'+data.cost+' </td><td><input type="number" min="0" max="100" value="0" size="2" style="width:50px" name="qty" id="qty'+count+'"/> </td><td id=amount'+count+'> </td></tr>';
                    $("#count").text(count.toString())
                    $("#rows").append(markup);

                    $("#qty"+count).change(function(){
                    var value = $(this).val();
//                    alert(value);
                    amount= data.cost*value;
//                    alert(amount);
                    $("#amount"+count).text(amount);
                    var entry=new Object();
                    entry.qty=value
                    entry.batch_id=data.batch_id
                    bill_info.push(entry);


                    });
                    }
                });
            }

    });
    $("#bill").click(function(){
        if($("#uname").val() == ""){
        alert("Enter the Username");
        }
        if($("#phoneNo").val() == ""){
        alert("Enter the Phone Number");
        }
        if($("#email").val() == ""){
        alert("Enter the User's email");
        }
        else{
            if(bill_info.length==" ")
                {
                alert("BILL INFO IS EMPTY");
                }

            else{
                var jsonArray = JSON.stringify(bill_info);
                console.log(jsonArray)
                $.ajax({
                    type:'POST',
                    url:"http://127.0.0.1:5000/generate",
                    data:jsonArray,
                    dataType:"json",
                    contentType: "application/json; charset=UTF-8",
                    success:function(data,status){
                        alert("bill generated");
                        bill_info=[];
                        location.reload(true);
                    },
                    error: function(jqXHR, exception){
                            alert(exception.toString());
                            }
                        });
                    }
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
            $.get("http://127.0.0.1:5000/search?medicine=" +value, function(data, status){
                        console.log(data)

                        if(data.status==true){
                            alert("medicine exist");
                        }
                        else{
                            alert("medicine does not exist");

                        }
                });
            }
        });

});
