// A $( document ).ready() block.
$( document ).ready(function() {

    $('#add-ninja-btn').click(function(){
        $('#add-ninja-form').show();
    });

    $('#add-ninja-submit').click(function() {
        var data = {
            name: $('#add-ninja-form-name').val(),
            email: $('#add-ninja-form-email').val(),
            department: $('#add-ninja-form-department').val(),
            building: $('#add-ninja-form-building').val()
        }
        console.log(data.name);
        console.log(data.email);
        console.log(data.department);
        console.log(data.building);

        $.ajax({
            type: "POST",
            url: '/ninjas',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (response) {
                console.log(response)
            }
        })
        return false;
    });
});