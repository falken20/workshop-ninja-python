function listNinjas(department, callback) {
    $.ajax({
        type: "GET",
        url: '/ninjas' + (department ? "?department=" + department : ""),
        dataType: 'json',
        contentType: 'application/json',
        success: function (response) {
            console.log(response);
            callback(response);
        }
    });
}

function getNinja(id, callback) {
    $.ajax({
        type: "GET",
        url: '/ninjas/' + id,
        success: function (data) {
            callback(data);
        }
    });
}

function saveNinja(data, callback) {
    $.ajax({
        type: "POST",
        url: '/ninjas',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response) {
            console.log(response);
            callback();
        }
    });
}

function editNinja(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: '/ninjas/' + id,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response) {
            console.log(response);
            callback();
        }
    });
}

function deleteNinja(id, callback) {
    $.ajax({
        type: "DELETE",
        url: '/ninjas/' + id,
        success: function () {
            callback();
        }
    });
}

function listMoocs(ninja_id, callback) {
    $.ajax({
        type: "GET",
        url: '/moocs?ninja_id=' + ninja_id,
        success: function (response) {
            console.log(response);
            callback(response);
        }
    });
}

function saveMooc(mooc, callback) {
    $.ajax({
        type: "POST",
        url: "/moocs",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(mooc),
        success: function (response) {
            console.log(response);
            callback();
        }
    });
}

function deleteMooc(id, callback) {
    $.ajax({
        type: "DELETE",
        url: '/moocs/' + id,
        success: function () {
            callback();
        }
    });
}

function listRanking(callback) {
    $.ajax({
        type: "GET",
        url: '/ranking',
        dataType: 'json',
        contentType: 'application/json',
        success: function (response) {
            console.log(response);
            callback(response);
        }
    });
}
