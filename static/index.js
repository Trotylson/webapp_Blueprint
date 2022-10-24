// $(document).ready(function () {
$("#registerButton").on('click', function(){
    console.log("button pushed")

    let username = $("#username").val();
    let password = $("#password").val();
    let email = $("#email").val();

    let register_data = {"username": username, "email": email, "password": password}

    console.log(username)

    $.ajax({
        type: "POST",
        url: "/register",
        data: register_data,
        dataType: "application/json",

        success: function(result){
        console.log("SUCCESS!", result)        
        },
        error: function(result){
            console.log("ERROR!", result)
        }
    })
})
// })