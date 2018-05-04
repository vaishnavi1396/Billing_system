var bill_info=[];


$(document).ready(function(){
        $("#search").click(function(){
                var value=$("#txtSearch").val()
                //alert("Getting the medicine name "+value);
                if(value=="")
                {
                    alert("Enter the medicine name");
                }
                else{
                    $.get("http://127.0.0.1:5000/search?medicine=" +value, function(data, status){
                                console.log(data)
                                alert("Data: " + data + "\nStatus: " + status);
                                if(data.status==true){
                                    alert("medicine exist");
                                }
                                else{
                                    alert("medicine does not exist");
                                }
                        });
                    }
                });

        $('#bill_table').DataTable();

        $("#add").click(function(){
        var count=$("#count").text();
        count=parseInt(count)
        count=count+1
        var med_name=$("#txtSearch").val()
        //alert("adding medicine is" +med_name);
        //alert(value)

        if(med_name=="")
        {
            alert("Enter the medicine name");

        }
        else{
            $.get("http://127.0.0.1:5000/add?medicine=" +med_name, function(data, status){
                     //alert("Data: " + data + "\nStatus: " + status);
                     function convert(str) {
                        var date = new Date(str),
                            month = ("0" + (date.getMonth()+1)).slice(-2),
                            day  = ("0" + date.getDate()).slice(-2);
                        return [ day, month, date.getFullYear() ].join("-");
                        }

                    if(status.trim() == "success".trim())
                    {
                    console.log(data)
                    var markup = '<tr id=medicin_item'+(count).toString()+'"><td style="display:None">'+data.batch_id+'</td><td style="display:None">'+data.med_id+'</td><td>'+(count).toString()+'</td><td>'+med_name+'</td><td>'+convert(data.mfg_Date)+' </td><td>'+convert(data.exp_Date)+' </td><td>'+data.cost+' </td><td><input type="number" min="0" max="100" value="0" size="2" style="width:50px" name="qty" id="qty'+count+'"/> </td><td class="txtCal" id=amount'+count+'>0</td></tr>';
                    $("#count").text(count.toString())
                    $("#bill_table").DataTable().row.add($(markup)[0]).draw();

                    $("#qty"+count).change(function(){
                    var value = $(this).val();
//                    alert(value);
                    if(data.qty<value){
                        alert("quantity exceeded")
                        return
                    }
                    amount= data.cost*value;
//                    alert(amount);

                    curr_amt=$("#amount"+count).html()
                    console.log(curr_amt)
                    if (curr_amt == ""){
                        curr_amt=0.0
                        }
                    else{
                        curr_amt=parseFloat(curr_amt)
                    }
                    var total=parseFloat($("#total").html())-curr_amt
                    console.log(total)
                    $("#amount"+count).text(amount);
                    total=total+amount
                    $("#total").text(" "+total)
                    });
                    }
                });
            }
//       $("#bill_table").on('amount', function () {
//       var calculated_total_sum = 0;
//
//       $("#amount .txtCal").each(function () {
//           var get_textbox_value = $(this).val();
//           alert(get_textbox_value);
//           if ($.isNumeric(get_textbox_value)) {
//              calculated_total_sum += parseFloat(get_textbox_value);
//              }
//            });
//              $("#total").html(calculated_total_sum);
//       });



    });

    $("#bill").click(function(){
        var username = $("#uname").val();
        if(username == ""){
        alert("Enter the Username");
        return

        }

        var phoneNo = $("#phoneNo").val();
        if(phoneNo == ""){
        alert("Enter the Phone Number");
        return
        }

        var email = $("#email").val();
        if(email == ""){
        alert("Enter the User's email");
        return
        }

        tabel=$("#bill_table").DataTable()
        if(tabel.rows().count()==0){
            alert("BILL INFO IS EMPTY" +tabel.count());
            return
        }
        else{

        var items=[]
                data=tabel.rows().data()


                for(i=0;i<tabel.rows().count();i++)
                {
                     batch_id=data[i][0]
                     med_id=data[i][1]
                     id=data[i][2]
                     qty=$("#qty"+id).val()
                     var item={"batch_id":batch_id,"qty":qty,"med_id":med_id}
                     items.push(item)
                }

                data={
                "username":username,
                "phone":phoneNo,
                "email":email,
                "data":items
                }

                data = JSON.stringify(data);

                console.log(data)
                $.ajax({
                    type:'POST',
                    url:"http://127.0.0.1:5000/generate",
                    data:data,
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
        });

});
