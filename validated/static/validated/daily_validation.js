var dateFormat = "yy-mm-dd";

tr_ini = '<tr>';
tr_fin = '</tr>';
var json_data = {};
var data_date = [];
var data_value = [];
var data_maximum = [];
var data_minimum = [];
var num_datos = 0;

var indicators_subhourly = {
    num_time: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum:0,
    num_stddev: 0,
    // TODO check if renaming num_data is needed
    num_data:0
}

var indicators_daily = {
    num_date: 0,
    num_percentage: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum: 0,
    num_days: 0
}

var num_date = 0;
var detail_table_value_columns;
var daily_table_value_columns;



$(document).ready(function() {
    $("#btn_submit").click(daily_query_submit);

    $("#id_variable").change(function () {
        var variable_id = $(this).val();
        var url = '/variable/variable/' + variable_id.toString() + '/?format=json';
        const url_total = window.location.origin + url;

        fetch(url_total)
          .then(response => response.json())
          .then(data => {
            $("#id_minimum").val(data.minimum);
            $("#id_maximum").val(data.maximum);
          })
          .catch(error => {
            console.error(error);
            alert(error);
          });
    });

    $("#chk_detail_time").change(filter_detail_table);
    $("#chk_detail_value").change(filter_detail_table);
    $("#chk_detail_stddev").change(filter_detail_table);
    $("#chk_detail_selected").change(filter_detail_table);
    $("#chk_detail_value_difference").change(filter_detail_table);

    var $table = $('#table_daily');

    var $btn_daily_send = $('#btn_daily_send');

    var $btn_detail_select = $('#btn_detail_select');
    var $btn_detail_unselect = $('#btn_detail_unselect');
    var $btn_detail_new = $("#btn_detail_new");
    var $btn_detail_save = $('#btn_detail_save');

    var $btn_detail_modify_row = $('#btn_detail_modify_row');
    var $btn_detail_new_save = $('#btn_detail_new_save');


    $btn_daily_send.click(save_daily);

    $btn_detail_select.click(check);
    $btn_detail_unselect.click(uncheck);
    $btn_detail_new.click(open_form_new);
    $btn_detail_save.click(save_detail);

    $btn_detail_modify_row.click(detail_modify_row);
    $btn_detail_new_save.click(detail_new_save);


    var dateFormat = "yy-mm-dd";
    $( "#id_start_date" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2000:'+(new Date).getFullYear()
    });
    $( "#id_start_date" ).on( "change", function() {
        $( "#id_end_date" ).datepicker( "option", "minDate", getDate( this ) );
    });
    $( "#id_end_date" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2000:'+(new Date).getFullYear()
    });
    $( "#id_end_date" ).on( "change", function() {
        $( "#id_start_time" ).datepicker( "option", "maxDate", getDate( this ) );
    });

    function getDate( element ) {
        var date;
        try {
            date = $.datepicker.parseDate( dateFormat, element.value );
        } catch( error ) {
            date = null;
        }
        return date;
    }
});


function generate_traces_dispersion(data, source_type, color){
    var result = [];
    var columns = Object.keys(data);
    columns = columns.filter((e) => e !== "time");
    for (const c of columns) {
      result.push(
        {
          x: data.time,
          y: data[c],
          mode: 'markers',
          name: c,
          showlegend: false,
          marker: {
            color: color,
            size: 2
          },
          type: 'scattergl',
          legendgroup: source_type
        }
      );

    }

    // Legend
    result.push(
        {
          x: [null],
          y: [null],
          mode: 'markers',
          name: source_type,
          showlegend: true,
          marker: {
            color: color,
          },
          type: 'scattergl',
          legendgroup: source_type
        }
    );
    return result;
}

function generate_traces_bars(data, source_type, color){
    var result = [];
    var columns = Object.keys(data);
    columns = columns.filter((e) => e !== "time");

    for (const c of columns) {
      result.push(
        {
          x: data.time,
          y: data[c],
          mode: 'lines',
          name: c + ' - ' + source_type,
          marker: {
            color: color,
            size: 2
          },
          showlegend: true,
          type: 'scattergl',
        }
      );
    }

    return result;
}


function bar_plot(series, append_to, variable){
    var data_array = [];

    let measurement = generate_traces_bars(series.measurement, "Measurement", 'rgb(0, 0, 255)');
    data_array.push(...measurement);
    let validated = generate_traces_bars(series.validated, "Validated", 'rgb(0, 255, 0)');
    data_array.push(...validated);
    let selected = generate_traces_bars(series.selected, "Selected", 'rgb(0, 0, 0)');
    data_array.push(...selected);

    var layout = {
        title: variable.var_nombre,
        showlegend: true,
    };

    const miDiv = document.querySelector("#" + append_to);
    miDiv.style.height = "450px";
    miDiv.style.width = "850px";
    Plotly.newPlot(append_to, data_array, layout, {renderer: 'webgl'});
}

function dispersion_plot(series, append_to, variable){
    var data_array = [];

    let measurement = generate_traces_dispersion(series.measurement, "Measurement", 'rgb(0, 0, 255)');
    data_array.push(...measurement);
    let validated = generate_traces_dispersion(series.validated, "Validated", 'rgb(0, 255, 0)');
    data_array.push(...validated);
    let selected = generate_traces_dispersion(series.selected, "Selected", 'rgb(0, 0, 0)');
    data_array.push(...selected);

    var layout = {
        title: variable.var_nombre,
        showlegend: true,
    };

    const miDiv = document.querySelector("#" + append_to);
    miDiv.style.height = "450px";
    miDiv.style.width = "850px";
    Plotly.newPlot(append_to, data_array, layout, {renderer: 'webgl'});
}




function save_daily(event){
    var $table_daily = $('#table_daily');
    var $table_detail = $('#table_detail');
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    maximum = $("#id_maximum").val();
    minimum = $("#id_minimum").val();
    start_date = $("input[name='start_date']").val();
    end_date = $("input[name='end_date']").val();

    changes = JSON.stringify($table_daily.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));

    $.ajax({
        url: '/validated/daily_save/',
        data: {
            'csrfmiddlewaretoken': token,
            'station_id': station_id,
            'variable_id': variable_id,
            'start_date': start_date,
            'end_date': end_date,
            'maximum': maximum,
            'minimum': minimum,
            'changes': changes
        },
        type:'POST',
        beforeSend: function () {
            $table_daily.bootstrapTable('showLoading');
            $table_detail.bootstrapTable('showLoading');
        },
        success: function (data) {
            if (data.result == true){
                $("#div_body_message").html('Data saved correctly to Validated!')
                $("#div_validation_message").modal("show");
                $("#div_information").hide();
                clean_filters('daily');
                clean_filters('detail');
                $table_detail.bootstrapTable('removeAll');
                $table_daily.bootstrapTable('removeAll');
            }
            else{
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");
            }
            $table_daily.bootstrapTable('hideLoading');
            $table_detail.bootstrapTable('hideLoading');
        },
        error: function () {
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table_daily.bootstrapTable('hideLoading');
        }
    });

}


function save_detail(event){
    var $table = $('#table_detail');
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    data = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));

    $.ajax({
        url: '/validated/detail_save/',
        data: {
            'csrfmiddlewaretoken': token,
            'station_id': station_id,
            'variable_id': variable_id,
            'data': data
        },
        type:'POST',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (response) {
            document.getElementById("tab3-tab").style.display = "none";
            console.log(typeof response.resultado)
            if (response.result == true){
                $("#div_body_message").html('Data saved successfully')
                $("#div_validation_message").modal("show");
                $table.bootstrapTable('destroy');
                document.getElementById("tab3-tab").style.display = "none";
                clean_filters('detail');
                var tab1 = document.getElementById("tab1-tab");
                tab1.click();
                daily_query_submit();
            }
            else{
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");
                $table.bootstrapTable('hideLoading');
            }
        },
        error: function () {
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });


}


function daily_query_submit(){
    var $table_daily = $('#table_daily');
    var var_id = $("#id_variable").val();
    var flag_error = false;
    var message = '';
    $("#orig_variable_id").val(var_id);
    $("#div_information").html('')
    clean_filters('daily');
    clean_filters('detail');
    start_date = document.querySelector('input[name="start_date"]').value;
    end_date = document.querySelector('input[name="end_date"]').value;
    if( start_date == '' || end_date == '')
    {
        $("#div_message_dates").show("slow");
        $("#div_c").html("");
    }
    else {
        $("#div_message_dates").hide();
        $("#div_c").html("");
        $.ajax({
            url: $("#form_validation").attr('action'),
            data: $("#form_validation").serialize(),
            type:'POST',
            beforeSend: function () {
                $table_daily.bootstrapTable('showLoading');
            },
            success: function (data) {
                $("#btn_submit").attr("disabled", false);
                for (var key in data){
                    if (key == 'error'){
                        flag_error = true;
                        message = data.error;
                    }
                }
                if (flag_error == true){
                    $table_daily.bootstrapTable('hideLoading');
                    $("#div_body_message").html(message)
                    $("#div_validation_message").modal("show");
                    return;
                }


                if (data.data.length < 1){
                    $("#div_information").show("slow");
                    $("#div_information").html('<div><h1 style="background-color : red">No hay datos</h1></div>');
                    return;
                }

                $("#div_c").html(data.curva);

                if (data.variable.is_cumulative){
                    bar_plot(data.series, "div_information", data.variable);
                }else{
                    dispersion_plot(data.series, "div_information", data.variable);
                }

//                enable_new();
                var_id = data.variable.id;
                variable = data.variable;
                station = data.station;
                json_data = data.data

                $table_daily.bootstrapTable('destroy');
                indicators_daily = data.indicators;
                var columns = get_columns_daily(var_id, data.value_columns);
                $table_daily.bootstrapTable({
                    columns:columns,
                    data: json_data,
                    height: 400,
                    showFooter: true,
                    uniqueId: 'id',
                    rowStyle: style_row
                });

                $table_daily.bootstrapTable('hideLoading');
                $("#table_detail").bootstrapTable('removeAll');
            },
            error: function () {
                $table_daily.bootstrapTable('hideLoading');
                $("#div_body_message").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_validation_message").modal("show");
                //mostrar_mensaje()
            }
        });
    
    }

    var tab1 = document.getElementById("tab1-tab");
    tab1.click();
}


function getTab(evt, tabName) {
    var i, tabpane;
    tabpane = document.getElementsByClassName("tab-pane");
    for (i = 0; i < tabpane.length; i++) {
        tabpane[i].style.display = "none";
        tabpane[i].classList.remove("show");
    }

    var e = document.getElementById(tabName);
    e.classList.add("show");
    e.style.display = "";
}








function get_existe_en_tabla(fecha, datos){
    debugger;
    var existe = false;
    return datos.filter(
        function(datos){
            //if(datos.fecha == fecha)
                //existe = true
            return datos.fecha == fecha
        }
    )


}



function detail_modify_row(event){
    $('input[name="detail_time"]').attr('disabled',false);
    var variable_id = parseInt($("#id_variable").val());
    var $form = $("#form_modify");
    var inputs =$form.serializeArray();
    var $modal = $("#modal_modify");
    var data = {};
    var table = $table = $("#table_detail");

    $.each(inputs, function(i, field){
        if (field.name.includes('detail_')) {
            var _field = field.name.split("_")[1];
            if(detail_table_value_columns.includes(_field) || ['id', 'time'].includes(_field)){
                data[_field] = field.value;
            }
        }
    });

    id = data['id'];
    delete data['id'];
    data['is_selected'] = true;

    for (const c of detail_table_value_columns) {
        data[ c + '_error'] = get_value_error(data[c])
    }
    data['stddev_error'] = false;
    $table.bootstrapTable('updateByUniqueId',{
        id: id,
        row: data
    });
    $modal.modal('hide');
}


function detail_new_save(event){
    var variable_id = parseInt($("#id_variable").val());
    var $form = $("#form_new");
    var inputs =$form.serializeArray();
    var $modal = $("#modal_new");
    var data = {};
    var table = $table = $("#table_detail");

    $.each(inputs, function(i, field){
        if (field.name.includes('new_')) {
            var _field = field.name.split("_")[1];
            if(detail_table_value_columns.includes(_field) || ['date', 'hour'].includes(_field)){
                data[_field] = field.value;
                $('input[name="'+field.name+'"]').val("");
            }
        }
    });

    data['time'] = data['date'] + ' ' + data['hour'];
    delete data['date'];
    delete data['hour'];
    data['is_selected'] = true;
    var last_row = $table.bootstrapTable('getData').slice(-1);
    var last_id = parseInt(last_row[0]['id']);
    data['id'] = last_id + 1;

    $table.bootstrapTable('append', data);
    $table.bootstrapTable('scrollTo', 'bottom');



    $modal.modal('hide');
}


function check(event){
    var name = event.currentTarget.name;
    var tx_selection = '';
    var $table = '';

    if (name === 'detail'){
        $table = $("#table_detail");
        tx_selection = $("#txt_detail_selection").val().toString();
    }
    else{
    }
    $table.bootstrapTable('showLoading');
    var arr_id = tx_selection.split(',');
    var arr_range = tx_selection.split('-');
    var ids = []

    if (arr_id.length>1){
        ids = arr_id.map(function(id){
            return parseInt(id)
        });
    }
    if (arr_range.length>0){
        var start = parseInt(arr_range[0]);
        var end = parseInt(arr_range[1]);

        for (var id = start; id <= end; id++){
            ids.push(id);
        }
    }

    $table.bootstrapTable('checkBy', {field: 'id', values: ids})
    $table.bootstrapTable('hideLoading');
    $("#txt_detail_selection").val("");
}


function uncheck(event){
    var name = event.currentTarget.name;
    var tx_selection = '';
    var $table = '';

    if (name === 'detail'){
        $table = $("#table_detail");
        tx_selection = $("#txt_detail_selection").val().toString();
    }
    else{
    }
    $table.bootstrapTable('showLoading');
    var arr_id = tx_selection.split(',');
    var arr_range = tx_selection.split('-');
    var ids = []

    if (arr_id.length>1){
        ids = arr_id.map(function(id){
            return parseInt(id)
        });
    }
    if (arr_range.length>0){
        var start = parseInt(arr_range[0]);
        var end = parseInt(arr_range[1]);

        for (var id = start; id <= end; id++){
            ids.push(id);
        }
    }

    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids})
    $table.bootstrapTable('hideLoading');
    $("#txt_detail_selection").val("");
}

function detail_details(e, value, row){
    var $table = $('#table_detail');
    var station_id = $("#id_station").val();
    var variable_id = $("#id_variable").val();

    var id_daily = 0;
    var date = '';

    var state = row || false

    if (state == false ){
        id_daily = $("#orig_id_daily").val();
        date = $("#orig_date_daily").val();
    }
    else{
        id_daily = row.id;
        date = row.date;
        $("#orig_id_daily").val(id_daily);
        $("#orig_date_daily").val(date);
    }
    date = row.date;
    $("#orig_detail_date").val(date);


    var var_maximum = $("#id_maximum").val();
    var var_minimum = $("#id_minimum").val();

    url = '/validated/detail_list/' + station_id + '/' + variable_id + '/' + date + '/' + var_minimum + '/' + var_maximum;

    $.ajax({
        url: url,
        type:'GET',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            document.getElementById("tab3-tab").style.display = "block";
            document.getElementById("tab3-tab").click();
            detail_table_value_columns = data.value_columns;
            json_data = data.series;
            $table.bootstrapTable('destroy');
            for (const index in data.indicators){
                indicators_subhourly[index] = data.indicators[index];
                // TODO Verificar
                $("#span_"+index+"_detail").text(indicators_subhourly[index]);
            }


            for (const element of json_data) {
                element["time"] = (element['time']).replace('T',' ');
            }

            var columns = get_columns_detail(variable_id, data.value_columns);
            $table.bootstrapTable({
                columns:columns,
                data: json_data,
                rowStyle: style_row,
                height: 370,
                });
            $table.bootstrapTable('hideLoading');
        },
        error: function () {
            $("#div_body_message").html('An issue occurred with the validation. Please contact the administrator.')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });

};




function open_form_new(event){
    var date = $("#orig_detail_date").val();
    var variable_id = parseInt($("#id_variable").val());
    var $form_modal = $('#modal_new');
    var $form = "#form_new";
    var inputs = $("#form_new").serializeArray();

    $.each(inputs, function(i, field){
        if (field.name.includes('new_')) {
            var _field = field.name.split("_")[1];
            if(detail_table_value_columns.includes(_field) || ['date', 'hour'].includes(_field)){
                $('input[name="'+field.name+'"]').parent().show();
            }else{
                $('input[name="'+field.name+'"]').parent().hide();
            }
        }
    });

    $($form+',input[name="new_date"]').val(date);
    $form_modal.modal("show");
}



function open_form_update(e, value, row, index){
    var $form_modal = $('#modal_modify');
    var inputs = $("#form_modify").serializeArray();
    $.each(inputs, function(i, field){
        if (field.name.includes('detail_')) {
            var _field = field.name.split("_")[1];
            if(detail_table_value_columns.includes(_field) || ['id', 'time'].includes(_field)){
                $('input[name="'+field.name+'"]').parent().show();
                $('input[name="'+field.name+'"]').val(row[_field]);
            }else{
                $('input[name="'+field.name+'"]').parent().hide();
            }
        }
    });
    $('input[name="detail_time"]').attr('disabled',true);
    $form_modal.modal("show");
}



function get_columns_daily(var_id, value_columns){
    var columns = [];

    var state = {
        field:'state',
        checkbox:true
    };
    columns.push(state);

    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id
    };
    columns.push(id);

    var date = {
        field:'date',
        title: 'Date',
        cellStyle: style_date,
        formatter: format_value,
        footerFormatter: footer_date,
        //filterControl: 'datepicker'
    };
    columns.push(date);


    var percentage = {
        field:'percentage',
        title:'Percnt.',
        cellStyle: style_percentage,
        footerFormatter: footer_average,
        //filterControl: 'input'
    };
    columns.push(percentage);

    if (value_columns.includes("sum")){
        var sum = {
            field:'sum',
            title:'Sum',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_sum
        };
        columns.push(sum);
    }

    if (value_columns.includes("average")){
        var average = {
            field:'average',
            title:'Average',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_average
        };
        columns.push(average);
    }

    if (value_columns.includes("maximum")){
        var maximum = {
            field:'maximum',
            title:'Max. of Maxs. ',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_average
        };
        columns.push(maximum);
    }

    if (value_columns.includes("minimum")){
        var minimum= {
            field:'minimum',
            title:'Min. of Mins. ',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_average
        }
        columns.push(minimum);
    }

    var value_difference = {
        field:'value_difference_error_count',
        title:'Diff. Err',
        cellStyle: style_value_diff,
        formatter: format_value,
        footerFormatter: footer_value_diff
    };
    columns.push(value_difference);

    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_daily,
        events: {
           'click .search': detail_details,
        }
    };
    columns.push(action);

    return columns
}


function get_columns_detail(var_id, value_columns){
    var columns = [];
    var span = '<span id="span_id" class="badge badge-danger">num</span>';

    var is_selected = {
        field:'is_selected',
        checkbox:true,
    };
    columns.push(is_selected);

    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id,
        footerFormatter: footer_id
    };
    columns.push(id);

    var time = {
        field:'time',
        title:'Time',
        cellStyle: style_detail_time,
        footerFormatter: footer_data_count
    };
    columns.push(time);

    var time_lapse_status = {
        field:'time_lapse_status',
        visible: false,
    };
    columns.push(time_lapse_status);

    for (const c of detail_table_value_columns) {
        var value_column = {
            field: c,
            title: c.charAt(0).toUpperCase() + c.slice(1),
            cellStyle: style_detail_value_error,
//            formatter: format_value,
            footerFormatter: footer_average
        };
        if ( c == 'sum'){
            value_column.cellStyle = style_detail_value_error;
            value_column.footerFormatter = footer_sum;
        }
        columns.push(value_column);

        var value_column_error = {
            field: c + '_error',
            visible: false,
        };
        columns.push(value_column_error);
    }


    var outlier_err = {
        field:'stddev_error',
        title:'Outliers',
        cellStyle: style_stddev_err,
        formatter: format_stddev_err,
        footerFormatter: footer_stddev_err
    };
    columns.push(outlier_err);


    var value_difference = {
        field:'value_difference',
        title:'Value diff.',
        cellStyle: style_detail_value_diff,
        footerFormatter: footer_detail_value_diff
    };
    columns.push(value_difference);

    var value_diff_error = {
        field:'value_difference_error',
        visible: false,
    };
    columns.push(value_diff_error);

    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_detail,
        events: {
           'click .update': open_form_update
        }
    };
    columns.push(action);

    return columns
}


function operate_table_daily(value, row, index) {
    return [
      '<a class="search" href="javascript:void(0)" title="Detail">',
      '<i class="fa fa-search"></i>',
      '</a>  ',
    ].join('')
}



function operate_table_detail(value, row, index) {
    return [
      '<a class="update" href="javascript:void(0)" title="Modify">',
      '<i class="fa fa-edit"></i>',
      '</a>  ',
    ].join('')
}





function style_row(row, index){
    var _class = '';
    if (row.state == false) {
      _class = 'error';
    }

    else
        _class = '';
    return {classes: _class}

//    var _class = '';
//    if (row.is_selected) {
//      _class = 'normal';
//    }
//    return {classes: _class}

}


function style_id(value, row, index){
    var _class = '';

    if (row.all_validated == true){
        _class = 'validated';
    }
   // TODO check row.seleccionado translation
    else if (row.seleccionado == false){
        _class = 'error';
    }
    else{
        _class = '';
    }
    return { classes: _class}
}


function style_date(value, row, index){
    var _class = '';
    if (row.date_error > 0)
        _class = 'error';
    else
        _class = '';
    return { classes: _class}
}

function style_percentage(value, row, index) {
    if (row.percentage_error == true) {
        return {
            classes: 'error'
        }
    }
    else{
        return {
            classes: 'normal'
        }
    }
}


function style_value(value, row, index, field){
    var _class = '';
    field_value = "suspicious_" + field +"s_count";

    if (row[field_value]>0 )
        _class = 'error';
    else
        _class = 'normal';
    return { classes: _class}
}


function style_value_diff(value, row, index){
    var _class = ''
    if (row.value_difference_error_count >= 1)
        _class = 'error';
    else
        _class = '';
    return { classes: _class}
}





function style_detail_time(value, row, index){
    var _class = '';
    if (row.time_lapse_status == 0){
        _class = 'error';
    }else if (row.time_lapse_status == 2){
        _class = 'warning';
    }else if (row.time_lapse_status == 1){
        if (row.is_selected){
            _class = 'normal';
        }
    }else {
        _class = 'error';
    }
    return { classes: _class}
}

function style_detail_value_error(value, row, index, field){
    var _class = '';
    field_error = field + '_error';
    if (row[field_error] === true){
        _class = 'error';
    }
    else if (row.is_selected){
        _class = 'normal';
    }
    return { classes: _class};
}


function style_stddev_err(value, row, index){
    var _class = '';
    if (value === true)
    {
        _class = 'error';
    }
    else if (row.is_selected){
        _class = 'normal';
    }
    return { classes: _class}
}


function style_detail_value_diff(value, row, index){
    var _class = '';
    if (row.value_difference_error)
    {
        _class = 'error';
    }
    else if (row.is_selected){
        _class = 'normal';
    }
    return { classes: _class}
}







function format_value(value, row, index, field){
    var span = '<span class="badge badge-light">num</span>';
    var content = value;
    var errors_field;
    if (["sum", "average", "value", "maximum", "minimum"].includes(field)){
        errors_field = "suspicious_" + field +"s_count";
    }else if (field == "value_difference_error_count"){
        errors_field = "value_difference_error_count";
        content = "";
    }else{
        errors_field = field +"_error";
    }

    if (row[errors_field]>0 ){
        span = span.replace('num',row[errors_field].toString());
        content = content + ' ' + span;
    }
    return content
}

function format_stddev_err(value, row, index, field){
    if (value){
        return "X";
    }
    return "-";
}



function footer_id(data){
    var span = '<span class="badge badge-danger">num</span>';
    var num_date = data.reduce(function(num, i){
        // TODO check translation: seleccionado
        if (i['state'] && i['is_selected']==false)
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_date.toString());

    return span;

}


function footer_date(data){
    var span = '<span class="badge badge-danger">num</span>';
    var var_id = $("#id_variable").val();
    var dates = [];

    $.map(data, function(row){
        dates.push(row.date);
    });

    var sum = dates.unique().length;
    var num_date = data.reduce(function(num, i){
        if (i['date_error']>0)
            return num +1;
        else
            return num;
    }, 0);

    // TODO ask the team for prefferred behaviour
    span = span.replace('num', num_date.toString());

    return sum + ' of ' + indicators_daily['num_days'] + ' days ' + span;
}


function footer_average(data){
    var field = this.field;
    var field_error = '';

    field_error = field + '_error';

    var span = '<span class="badge badge-danger">num</span>';
    var mean = 0;
    var sum = data.reduce(function (sum, i) {
          if (i['state'] && i[field] != null && i[field] != "")
            return sum + parseFloat(i[field])
        else
            return sum;
    }, 0);
    var data_count = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "")
            return sum + 1;
        else
            return sum;
    }, 0);

    var num_value = data.reduce (function (num, i){
        if (i[field_error] && i['state'])
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num', num_value);

    if (isNaN(sum))
        mean = '-';
    else
        mean = (sum / data_count).toFixed(2);
    return mean + ' ' + span;
}




function footer_sum(data){
    var field = this.field;
    var field_error = this.field + '_error';
    var span = '<span class="badge badge-danger">num</span>';
    var sum = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "" ){
            return sum + parseFloat(i[field])
        }
        else{
            return sum
        }

    }, 0);
    var num_value = data.reduce (function (sum, i){
        if (i[field_error] && i['state'])
            return sum +1 ;
        else
            return sum;
    }, 0);

    span = span.replace('num', num_value);

    return sum.toFixed(2) + ' ' + span;
}


function footer_value_diff(data){

    var span = '<span class="badge badge-danger">num</span>';
    var num_vd= data.reduce(function(num, i){
        if (i['value_difference_error_count'] >= 1 )
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_vd);
    return span;
}



function footer_data_count(data){
    var span = '<span class="badge badge-danger">num</span>';

    var sum = data.reduce(function (sum, i) {
        if (i['state']){
            return sum + 1
        }
        else{
            return sum
        }

    }, 0);

    var num_date = data.reduce(function(num, i){
        // TODO check logic
        if ( (i['time_lapse_status']==0) || (i['time_lapse_status']==2) || (i['time_lapse_status']==3))
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_date.toString());

    return sum + ' of ' + indicators_subhourly['num_data'] + '. ' + span;
}



function footer_stddev_err(data){
    var span = '<span class="badge badge-danger">num</span>';
    var num_stddev = data.reduce(function(num, i){
        if (i['stddev_error'] && i['state'])
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_stddev.toString());

    return span;
}

function footer_detail_value_diff(data){
    var span = '<span class="badge badge-danger">num</span>';
    var num_vde = data.reduce(function(num, i){
        if (i['value_difference_error'])
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num', num_vde.toString());

    return span;
}






function get_filter_time(option){
    var filter = [];

    if (option == 'shorter_than_tx_period')
        filter = [0];
    else if (option == 'greater_than_tx_period')
        filter = [2];
    else
        filter = [0, 1, 2];
    return filter
}

function get_filter_percentage(option){
    var filter = [];

    if (option == 'error')
        filter = [true];
    else if (option == 'normal')
        filter = [false];
    else
        filter = [true, false];

    return filter;
}

function get_filter_value(option){
    var filter = [];

    if (option == 'error')
        filter = [true];
    else if (option == 'normal')
        filter = [false];
    else
        filter = [true, false, null];

    return filter
}


function get_filter_stddev(option){
    var filter = [];

    if (option == 'error')
        filter = [true];
    else if (option == 'normal')
        filter = [false];
    else
        filter = [true, false, null];

    return filter
}


function get_filter_state(option){
    var filter = [];

    if (option == 'error')
        filter = [false];
    else if (option == 'normal')
        filter = [true];
    else
        filter = [true, false];

    return filter
}


function get_filter_selected(option){
    var filter = [];

    if (option == 'selected')
        filter = [true];
    else if (option == 'non-selected')
        filter = [false];
    else
        filter = [true, false];

    return filter
}


function get_filter_value_difference(option){
    var filter = [];

    if (option == 'error')
        filter = [true];
    else if (option == 'normal')
        filter = [false];
    else
        filter = [true, false, null];

    return filter;
}

function filter_detail_table(){
    var time = $("#chk_detail_time").val();
    var value = $("#chk_detail_value").val();
    var stddev = $("#chk_detail_stddev").val();
    var selected = $("#chk_detail_selected").val();
    var value_difference = $("#chk_detail_value_difference").val();

    var filter_time = get_filter_time(time);
    var filter_value = get_filter_value(value);
    var filter_stddev = get_filter_stddev(stddev);
    var filter_selected = get_filter_selected(selected);
    var filter_value_difference = get_filter_value_difference(value_difference);

    var filter = {
        is_selected: filter_selected,
        stddev_error: filter_stddev,
        time_lapse_status: filter_time,
        value_difference_error: filter_value_difference,
    };

    var main_column = detail_table_value_columns.filter(c => ["sum", "average", "value"].includes(c));
    main_column.forEach(c => filter[c + '_error'] = filter_value);
    $("#table_detail").bootstrapTable('filterBy', filter);
}


function clean_filters(type){
    if (type == 'detail'){
        $("#chk_detail_time").prop('selectedIndex',0);
        $("#chk_detail_value").prop('selectedIndex',0);
        $("#chk_detail_stddev").prop('selectedIndex',0);
        $("#chk_detail_selected").prop('selectedIndex',0);
        $("#chk_detail_value_difference").prop('selectedIndex',0);
        $("#txt_detail_selection").val('');
    }
    else{
        // for daily filters
    }
}

function get_value_error(value){
    var minimum = Number($("#id_minimum").val());
    var maximum = Number($("#id_maximum").val());
    var value_error = false;

    if (Number(value) > maximum || Number(value) < minimum )
    {
        value_error = true;
    }
    return value_error;
}


function enable_new(){
    var variable_id = $("#id_variable").val();

    if ( variable_id != "11" || variable_id == "4" || variable_id == "5" )
        $("#btn_detail_new").attr("disabled", false);
    else
        $("#btn_detail_new").attr("disabled", true);
}




Array.prototype.unique=function(a){
  return function(){return this.filter(a)}}(function(a,b,c){return c.indexOf(a,b+1)<0
});

