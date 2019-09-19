// A $( document ).ready() block.
$(document).ready(function () {

    var views = {
        'loading': '.loading',
        'ninja-list': '#ninja-list',
        'ninja-form': '#add-ninja-form',
        'ninja-detail': '#ninja-detail',
        'mooc-form': '#mooc-form'
    }

    function setView(view) {
        Object.keys(views).forEach(function(v) {
            if (v === view) {
                $(views[v]).show();
            } else {
                $(views[v]).hide();
            }
        });
    }

    function image(image) {
        if (image) {
            return '<img class="img-small" src="' + image + '">';
        } else {
            return '<img class="img-small" src="resources/ninja.svg">';
        }
    }

    function loadNinjas(department) {
        if (department === undefined) {
            setView('loading')
        }
        listNinjas(department, function(response) {
            showNinjaList(response);
        });
    }

    function showNinjaList(list) {
        setView('ninja-list')
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
            showNinjaDetail(JSON.parse(decodeURI($(e.target).parents('tr').find('input[type="hidden"]').val())))
        });
    }

    function showNinjaDetail(data) {
        setView('ninja-detail')
        if (data) {
            $('#ninja-detail-id').text(data._id);
            $('#ninja-detail-name').text(data.name);
            $('#ninja-detail-email').text(data.email);
            $('#ninja-detail-department').text(data.department);
            $('#ninja-detail-building').text(data.building);
            if (data.image) {
                $('#ninja-detail-image').prop('src', data.image);
            }
            $('#ninja-detail-list-content').empty();
            listMoocs(data._id, function(response) {
                response.forEach(function (i) {
                    $('#ninja-detail-list-content').append(row(
                        hidden(JSON.stringify(i)) +
                        column(i.name) +
                        column(i.desc) +
                        column(i.points) +
                        column(i.date) +
                        column(link('Delete', 'mooc-delete')), "mooc"));
                    $('.mooc-delete').click(function (e) {
                        if (confirm('Delete?')) {
                            var mooc = JSON.parse(decodeURI($(e.target).parents('tr').find('input[type="hidden"]').val()));
                            deleteMooc(mooc._id, function() {
                                showNinjaDetail(data);
                            });
                        }
                    });
                });
            });
        }
    }

    function showNinjaForm(id) {
        setView('ninja-form')
        $('form').trigger("reset");
        $('#add-ninja-form-image').val(undefined);
        $('#add-ninja-form-id').val(undefined);
        if (id) {
            getNinja(id, function() {
                $('#add-ninja-form-id').val(data._id);
                $('#add-ninja-form-name').val(data.name);
                $('#add-ninja-form-email').val(data.email);
                $('#add-ninja-form-department').val(data.department);
                $('#add-ninja-form-building').val(data.building);
                if (data.image) {
                    $('#ninja-image').prop('src', data.image);
                }
            });
        }
    }

    $('#add-ninja-btn').click(function () {
        showNinjaForm();
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
            editNinja(id, loadNinjas);
        } else {
            saveNinja(id, loadNinjas);
        }
        return false;
    });

    $('#add-ninja-cancel').click(function () {
        $('#add-ninja-form').hide();
        loadNinjas();
    });

    $('#ninja-detail-back-btn').click(function () {
        $('#add-ninja-form').hide();
        loadNinjas();
    });

    $('#ninja-detail-edit-btn').click(function() {
        var id = $('#ninja-detail-id').text();
        showNinjaForm(id);
    });

    $('#ninja-detail-delete-btn').click(function() {
        var id = $('#ninja-detail-id').text();
        if (confirm("Delete?")) {
            deleteNinjas(id, loadNinjas);
        }
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

    $('#ninja-detail-add-mooc-btn').click(function() {
        setView('mooc-form');
        $('#mooc-form-ninja-id').text($('#ninja-detail-id').text());
    });

    $('#mooc-form-cancel').click(function() {
        var id = $('#mooc-form-ninja-id').text();
        showNinjaDetail(id);
    });

    $('#mooc-form-submit').click(function() {
        var id = $('#mooc-form-ninja-id').text();
        var data = {
            name: $('#mooc-form-name').val(),
            desc: $('#mooc-form-desc').val(),
            points: parseInt($('#mooc-form-points').val()),
            ninja_id: parseInt(id)
        }
        saveMooc(data, function() {
            showNinjaDetail(id);
        });
        return false;
    });

    loadNinjas();
});