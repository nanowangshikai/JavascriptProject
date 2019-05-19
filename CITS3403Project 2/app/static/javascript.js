//adapt phone size and toggle shows menu bar
$(document).ready(function(){
    $(".menu-icon").click(function(){
        $('nav').toggleClass('activeNav')
        $('.loginBox').toggleClass('hidBox')
        $('#my-slider').toggleClass('hid')
        $('footer').toggleClass('hid')
    })
})

//last modified time
$(document).ready(function(){
var x = document.lastModified.split(" ")[0];
var y ="Last Modified Time<br/> "+x+"<br/>";
$('footer').append(y)
})

//show when user voted 
function time(){
    var x = new Date(document.lastModified);
    document.getElementById("time").innerHTML = x;
}

function createVote(){
    var x = document.getElementById("vote");
    
    if (x.style.display == "none"){
        x.style.display = "block";
    }else{
        x.style.display = "none";
    }
}