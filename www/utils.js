function row(content, type) {
    return '<tr class="' + type + '">' + content + '</tr>';
}

function column(content) {
    return '<td>' + content + '</td>';
}

function hidden(content) {
    return '<input type="hidden" value="' + encodeURI(content) + '"/>';
}

function link(content, type) {
    return '<a class="' + type + '">' + content + '</a>';
}
