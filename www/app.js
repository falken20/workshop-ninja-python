// A $( document ).ready() block.
$(document).ready(function () {

    function row(content, type) {
        return '<tr class="' + type + '">' + content + '</tr>';
    }

    function column(content) {
        return '<td>' + content + '</td>';
    }

    function hidden(content) {
        return '<input type="hidden" value="' + encodeURI(content) + '"/>';
    }

    function image(image) {
        if (image) {
            return '<img class="img-small" src="' + image + '">';
        } else {
            return '<img class="img-small" src="resources/ninja.svg">';
        }
    }

    function loadNinjas(department) {
        $('.loading').show();
        $.ajax({
            type: "GET",
            url: '/ninjas' + (department ? "?department=" + department : ""),
            dataType: 'json',
            contentType: 'application/json',
            success: function (response) {
                console.log(response);
                $('.loading').hide();
                showNinjaList(true, response);
            }
        });
    }

    function showNinjaList(show, list) {
        if (show) {
            if (list == undefined || list.length == 0) {
                $('#ninja-list-empty').show();
            } else {
                $('#ninja-list-empty').hide();
            }
            $('#ninja-list-content').empty();
            list.forEach(function (i) {
                $('#ninja-list-content').append(row(
                    hidden(JSON.stringify(i)) +
                    column(image(i.image)) +
                    column(i.name) +
                    column(i.email) +
                    column(i.department) +
                    column(i.building), "ninja"));
            });
            $('.ninja').click(function (e) {
                showNinjaForm(true, JSON.parse(decodeURI($(e.target).parents('tr').find('input[type="hidden"]').val())));
            });
            $('#ninja-list').show();
        } else {
            $('#ninja-list').hide();
        }
    }

    function showNinjaForm(show, data) {
        if (show) {
            showNinjaList(false);
            $('form').trigger("reset");
            $('#add-ninja-form-image').val(undefined);
            $('#add-ninja-form-id').val(undefined);
            console.log(data);
            if (data) {
                $('#add-ninja-form-id').val(data._id);
                $('#add-ninja-form-name').val(data.name);
                $('#add-ninja-form-email').val(data.email);
                $('#add-ninja-form-department').val(data.department);
                $('#add-ninja-form-building').val(data.building);
                if (data.image) {
                    $('#ninja-image').prop('src', data.image);
                }
            }
            $('#add-ninja-form').show();
        } else {
            $('#add-ninja-form').hide();
        }
    }

    $('#add-ninja-btn').click(function () {
        showNinjaForm(true);
    });

    $('#add-ninja-submit').click(function () {
        var data = {
            name: $('#add-ninja-form-name').val(),
            email: $('#add-ninja-form-email').val(),
            department: $('#add-ninja-form-department').val(),
            building: $('#add-ninja-form-building').val(),
            image: $('#ninja-image').prop('src')
        };

        var id = $('#add-ninja-form-id').val();

        if (data.image.indexOf("resources/ninja.svg") !== -1) {
            data.image = ""
        } else if (!data.image.startsWith("data:image")) {
            delete data.image
        }

        if (id) {
            $.ajax({
                type: "PUT",
                url: '/ninjas/' + id,
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function (response) {
                    console.log(response);
                    showNinjaForm(false);
                    loadNinjas();
                }
            });
        } else {
            $.ajax({
                type: "POST",
                url: '/ninjas',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function (response) {
                    console.log(response);
                    showNinjaForm(false);
                    loadNinjas();
                }
            });
        }
        return false;
    });

    $('#add-ninja-cancel').click(function () {
        $('#add-ninja-form').hide();
        loadNinjas();
    });

    $('#select-image').click(function () {
        $('#add-ninja-form-image').click();
        return false;
    });

    $('#clear-image').click(function () {
        $('#ninja-image').prop('src', 'resources/ninja.svg');
        return false;
    });

    $('#add-ninja-form-image').on("change", function (e) {
        var fr = new FileReader();
        fr.onload = function (e) {
            var image = e.target.result;
            $('#ninja-image').prop('src', image);
        };
        fr.readAsDataURL($(e.target).prop('files')[0]);
    });

    $('#search-btn').click(function () {
        var department = $('#department').val();
        loadNinjas(department);
    });

    loadNinjas();
});