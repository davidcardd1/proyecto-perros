//$("#loginLink").click(function(){
    //$("#includedLogin").load("/login"); 
    //alert("Hola");
    //$("#viewLogin").dialog(); 
//});

$('#loginLink').click(function(){   //bind handlers
    var url = $(this).attr('href');
    showDialog("/login");
    return false;
});
 
$("#loginModal").dialog({  //create dialog, but keep it closed
    autoOpen: false,
    height: 300,
    width: 350,
    modal: true
});
 
function showDialog(url){  //load content and open dialog
     $("#loginModal").load(url);
     $("#loginModal").dialog("open");         
}

$(function(){
    //$("#includedRegister").load("register"); 
});