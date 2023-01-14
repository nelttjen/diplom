let used_groups = [];
let last_selected = null;
let last_selected_name = null;
let commit_values = [];

function get_response(response) {
    let raw = response;
    try {
        if (response.responseText) {
            response = $.parseJSON(response.responseText);
        } else response = raw;
        
    } catch {
        response = raw;
    }
    return response;
  }

function select_group() {
    let selected = $('#group-select');
    used_groups.push(selected.val());
    last_selected = selected.val();
    $.ajax({
        type: "GET",
        url: `http://localhost:8000/api/group/lessons/?group=${last_selected}`,
    }).done((response => {
        response = get_response(response);
        // console.log(response);
        last_selected_name = response.extra.group_name;
        html = 
        `
        Группа ${response.extra.group_name}:
        <div id="group-lesson-inputs">
        `;
        $.each(response.content, function (indexInArray, valueOfElement) { 
            add_html = `<div class="lesson-input">
            <label for="lesson${valueOfElement.id}-input">Кол-во пар - ${valueOfElement.name}</label>
            <input id="lesson${valueOfElement.id}-input" value="4" class="form-control" less-index="${valueOfElement.id}" less-name="${valueOfElement.name}">
            </div>
            `;
            html += add_html;
        });
        html += '</div>';
        html += '<button class="btn btn-primary mt-3" id="lessons-commit">Сохранить</button>';
        $(".group-input").html(html);
        buttons();
    })).fail((response) => {
        response = get_response(response);
        alert(response.msg); 
    });
}

function commit_group() { 
    let items = $('.lesson-input');
    let values = [];
    $.each(items, function (indexInArray, elem) { 
        let value = $(elem).find('input').val();
        let obj_id = $(elem).find('input').attr('less-index');
        let obj_name = $(elem).find('input').attr('less-name');
        let new_obj = {
            'count': value,
            'lesson_id': obj_id,
            'lesson_name': obj_name
        };
        values.push(new_obj);
    });
    let obj_ = {};
    obj_[last_selected] = values;
    commit_values.push(obj_);
    
    let exclude_groups = used_groups.join(',');
    $.ajax({
        type: "GET",
        url: `http://localhost:8000/api/group/?exclude=${exclude_groups}`,
    })
    .done((response) => {
        response = get_response(response);
        let outer = `</div></div>`;
        let html = `
        <div class="commited-data mb-3" style="border: 1px solid red; padding: 5px;">
        Группа ${last_selected_name}:
        <div class="commited-data-rows">
        `;
        $.each(values, function (indexInArray, elem) { 
            let inner_html = `
            <div class="commited-inner mt-1">
            Пара ${elem.lesson_name} - ${elem.count} шт.
            </div>
            `;
            html += inner_html;
        });
        html += outer;
        $(".all_groups").html($(".all_groups").html() + html);
        outer = `</select>
        <button id="btn-add-group" class="btn btn-primary">Добавить</button>`;
        html = `
        <label for="group-select">Выберите группу</label>
        <select name="group-select" id="group-select">
        `;
        $.each(response.content, function (index, elem) { 
            inner_html = `
            <option value="${elem.id}">${elem.name}</option>
            `;
            html += inner_html;
        });
        html += outer;
        $(".group-input").html(html);
        buttons();
    })
    .fail((response) => {
        response = get_response(response);
        alert(response.msg);
    });
}

function buttons() { 
    $("#btn-add-group").click(function (e) { 
        e.preventDefault();
        select_group();
    });
    $('#lessons-commit').click((e) => {
        e.preventDefault();
        commit_group();
    });
}

$(document).ready(function () {
    buttons();
});