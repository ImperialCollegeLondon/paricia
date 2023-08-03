var colors = {
    'black': 'rgb(0, 0, 0)',
    'blue': 'rgb(0, 0, 255)',
    'red': 'rgb(255, 0, 0)',
    'green': 'rgb(0, 255, 0)',
};

function plot(data){
    var data_array = [];
    var cols = Object.keys(data.series);
    cols = cols.filter(item => item !== 'time');

    var color;
    for (let i = 0; i < cols.length; i++) {
        if (cols[i] == 'value' || cols[i] == 'average' || cols[i] == 'sum'){
            color = colors['black'];
        }else if (cols[i] == 'maximum'){
            color = colors['red'];
        }else if (cols[i] == 'minimum'){
            color = colors['blue'];
        }else{
            color = colors['green'];
        }

        if (data.variable.is_cumulative){
            data_array.push(bar_plot(data.series['time'], data.series[cols[i]], cols[i], color));
        }else{
            data_array.push(dispersion_plot(data.series['time'], data.series[cols[i]], cols[i], color));
        }
    }

    var layout = {
        title: data.station.code + " - " + data.variable.name,
        showlegend: true,
    };

    const miDiv = document.querySelector("#div_information");
    miDiv.style.height = "450px";
    miDiv.style.width = "820px";
    Plotly.newPlot('div_information', data_array, layout, {renderer: 'webgl'});
}


function bar_plot(x, y, name, color){
    var result = {
        x: x,
        y: y,
        mode: 'markers',
        type: 'bar',
        name: name,
        showlegend: true,
        marker: {
            color: color,
        },
    };
    return result;
}

function dispersion_plot(x, y, name, color){
    var result = {
        x: x,
        y: y,
        mode: 'markers',
        type: 'scattergl',
        name: name,
        showlegend: true,
        marker: {
            color: color,
            size: 2
        },
    };
    return result;
}



$(document).ready(function() {
    $("#btn_submit").click(plot_query);
    $("#btn_export").click(export_query);
});


function plot_query(){
    document.getElementById("id_request_type").value = "json";
    $("#div_information").html('')
    start_date = document.querySelector('input[name="start_date"]').value;
    end_date = document.querySelector('input[name="end_date"]').value;
    if( start_date == '' || end_date == '')
    {
        $("#div_message").show("slow");
        return null;
    }


    $.ajax({
        url: $("#form_data").attr('action'),
        data: $("#form_data").serialize(),
        type:'POST',
        beforeSend: function () {

        },
        success: function (data) {
            $("#btn_submit").attr("disabled", false);
            if (data.series.time.length < 1){
                return null;
            }
            plot(data);
        },
        error: function () {
            $("#div_body_message").html('Ocurrio un problema con la validación por favor contacte con el administrador')
            $("#div_validation_message").modal("show");
        }
    });
}


function export_query(){
    document.getElementById("id_request_type").value = "csv";
    $("#div_information").html('')
    start_date = document.querySelector('input[name="start_date"]').value;
    end_date = document.querySelector('input[name="end_date"]').value;
    if( start_date == '' || end_date == '')
    {
        $("#div_message").show("slow");
        return null;
    }
    $.ajax({
        url: $("#form_data").attr('action'),
        data: $("#form_data").serialize(),
        dataType: 'text',
        type:'POST',
        beforeSend: function () {
        },
        success: function (response) {
            var link = document.createElement('a');
            link.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(response);
            var stations = document.getElementById("id_station");
            var station = stations.options[stations.selectedIndex].text.replace(/ /g, "_");
            var variables = document.getElementById("id_variable");
            var variable = variables.options[variables.selectedIndex].text.replace(/ /g, "_");
            link.download = station + '__' + variable + '.csv';
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },
        error: function () {
            $("#div_body_message").html('Ocurrio un problema con la validación por favor contacte con el administrador')
            $("#div_validation_message").modal("show");
        }
    });


}
