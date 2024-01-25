// Define the date format
var dateFormat = "yy-mm-dd";

// Define the initial and final HTML for table rows
tr_ini = '<tr>';
tr_fin = '</tr>';

// Initialize an empty object to hold the JSON data
var json_data = {};

// Initialize arrays to hold the date, value, maximum, and minimum data
var data_date = [];
var data_value = [];
var data_maximum = [];
var data_minimum = [];

// Initialize a counter for the number of data points
var num_datos = 0;

// Define an object to hold the subhourly indicators
var indicators_subhourly = {
    num_time: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum:0,
    num_stddev: 0,
    // TODO check if renaming num_data is needed
    num_data:0 
}

// Define an object to hold the daily indicators
var indicators_daily = {
    num_date: 0, 
    num_percentage: 0, 
    num_value: 0, 
    num_maximum: 0, 
    num_minimum: 0, 
    num_days: 0 
}

// Initialize a counter for the number of date data points
var num_date = 0;

// Initialize variables to hold the detail and daily table value columns
var detail_table_value_columns;
var daily_table_value_columns;



// When the document is ready
$(document).ready(function() {
    // When the "Submit" button is clicked, call the daily_query_submit function
    $("#btn_submit").click(daily_query_submit);

    // When the variable ID changes
    $("#id_variable").change(function () {
        // Get the new variable ID
        var variable_id = $(this).val();
        // Construct the URL to fetch the variable data
        var url = '/variable/variable/' + variable_id.toString() + '/?format=json';
        const url_total = window.location.origin + url;

        // Fetch the variable data
        fetch(url_total)
          .then(response => response.json())
          .then(data => {
            // Update the minimum and maximum values in the user interface
            $("#id_minimum").val(data.minimum);
            $("#id_maximum").val(data.maximum);
          })
          .catch(error => {
            // Log and alert any errors
            console.error(error);
            alert(error);
          });
    });

    // When any of the detail filters change, call the filter_detail_table function
    $("#chk_detail_time").change(filter_detail_table);
    $("#chk_detail_value").change(filter_detail_table);
    $("#chk_detail_stddev").change(filter_detail_table);
    $("#chk_detail_selected").change(filter_detail_table);
    $("#chk_detail_value_difference").change(filter_detail_table);

    // Get references to various elements in the user interface
    var $table = $('#table_daily');
    var $btn_daily_send = $('#btn_daily_send');
    var $btn_detail_select = $('#btn_detail_select');
    var $btn_detail_unselect = $('#btn_detail_unselect');
    var $btn_detail_new = $("#btn_detail_new");
    var $btn_detail_save = $('#btn_detail_save');
    var $btn_detail_modify_row = $('#btn_detail_modify_row');
    var $btn_detail_new_save = $('#btn_detail_new_save');

    // When the "Send" button is clicked, call the save_daily function
    $btn_daily_send.click(save_daily);

    // When the "Select" button is clicked, call the check function
    $btn_detail_select.click(check);
    // When the "Unselect" button is clicked, call the uncheck function
    $btn_detail_unselect.click(uncheck);
    // When the "New" button is clicked, call the open_form_new function
    $btn_detail_new.click(open_form_new);
    // When the "Save" button is clicked, call the save_detail function
    $btn_detail_save.click(save_detail);

    // When the "Modify Row" button is clicked, call the detail_modify_row function
    $btn_detail_modify_row.click(detail_modify_row);
    // When the "New Save" button is clicked, call the detail_new_save function
    $btn_detail_new_save.click(detail_new_save);

    // Set up the datepickers
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

    // Function to parse a date from a string
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


/**
 * This function generates traces for a dispersion chart from the provided data.
 * @param {Object} data - The data to generate the traces from.
 * @param {string} source_type - The source type of the data.
 * @param {string} color - The color to use for the traces.
 * @returns {Array} An array of trace objects to be used in a dispersion chart.
 */
function generate_traces_dispersion(data, source_type, color){
        // Initialize an empty array to hold the result
        var result = [];

        // Get the column names from the data
        var columns = Object.keys(data);

        // Filter out the "time" column
        columns = columns.filter((e) => e !== "time");

        // For each column in the data
        for (const c of columns) {
            // Push a new trace object to the result array
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

        // Add a legend trace to the result array
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

        // Return the result array
        return result;
}

/**
 * This function generates traces for a bar chart from the provided data.
 * @param {Object} data - The data to generate the traces from.
 * @param {string} source_type - The source type of the data.
 * @param {string} color - The color to use for the traces.
 * @returns {Array} An array of trace objects to be used in a bar chart.
 */
function generate_traces_bars(data, source_type, color){
        // Initialize an empty array to hold the result
        var result = [];

        // Get the column names from the data
        var columns = Object.keys(data);

        // Filter out the "time" column
        columns = columns.filter((e) => e !== "time");

        // For each column in the data
        for (const c of columns) {
            // Push a new trace object to the result array
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

        // Return the result array
        return result;
}


/**
 * This function generates a bar plot using the Plotly library.
 * @param {Object} series - The data for the traces. Each property should be an object with properties "measurement", "validated", and "selected".
 * @param {string} append_to - The id of the HTML element where the plot should be appended.
 * @param {Object} variable - An object with property "var_nombre" which is the title of the plot.
 */
function bar_plot(series, append_to, variable){
    var data_array = [];

    // Generate traces for "measurement", "validated", and "selected" data and push them to data_array
    let measurement = generate_traces_bars(series.measurement, "Measurement", 'rgb(0, 0, 255)');
    data_array.push(...measurement);
    let validated = generate_traces_bars(series.validated, "Validated", 'rgb(0, 255, 0)');
    data_array.push(...validated);
    let selected = generate_traces_bars(series.selected, "Selected", 'rgb(0, 0, 0)');
    data_array.push(...selected);

    // Define the layout for the plot
    var layout = {
        title: variable.var_nombre, // The title of the plot
        showlegend: true, // Show the legend
    };

    // Set the height and width of the div where the plot will be appended
    const miDiv = document.querySelector("#" + append_to);
    miDiv.style.height = "450px";
    miDiv.style.width = "850px";

    // Generate the plot and append it to the div
    Plotly.newPlot(append_to, data_array, layout, {renderer: 'webgl'});
}

/**
 * This function generates a dispersion plot using the Plotly library.
 * @param {Object} series - The data for the traces. Each property should be an object with properties "measurement", "validated", and "selected".
 * @param {string} append_to - The id of the HTML element where the plot should be appended.
 * @param {Object} variable - An object with property "var_nombre" which is the title of the plot.
 */
function dispersion_plot(series, append_to, variable){
    var data_array = [];

    // Generate traces for "measurement", "validated", and "selected" data and push them to data_array
    let measurement = generate_traces_dispersion(series.measurement, "Measurement", 'rgb(0, 0, 255)');
    data_array.push(...measurement);
    let validated = generate_traces_dispersion(series.validated, "Validated", 'rgb(0, 255, 0)');
    data_array.push(...validated);
    let selected = generate_traces_dispersion(series.selected, "Selected", 'rgb(0, 0, 0)');
    data_array.push(...selected);

    // Define the layout for the plot
    var layout = {
        title: variable.var_nombre, // The title of the plot
        showlegend: true, // Show the legend
    };

    // Set the height and width of the div where the plot will be appended
    const miDiv = document.querySelector("#" + append_to);
    miDiv.style.height = "450px";
    miDiv.style.width = "850px";

    // Generate the plot and append it to the div
    Plotly.newPlot(append_to, data_array, layout, {renderer: 'webgl'});
}




/**
 * This function saves daily data by sending an AJAX POST request to the '/validated/daily_save/' endpoint.
 * @param {Object} event - The event object that triggered the function.
 */
function save_daily(event){
    // Select the daily and detail tables
    var $table_daily = $('#table_daily');
    var $table_detail = $('#table_detail');

    // Gather various pieces of data from the page
    var token = $("input[name='csrfmiddlewaretoken']").val();
    var station_id = $("#id_station").val();
    var variable_id = $("#id_variable").val();
    var maximum = $("#id_maximum").val();
    var minimum = $("#id_minimum").val();
    var start_date = $("input[name='start_date']").val();
    var end_date = $("input[name='end_date']").val();

    // Get the current data in the daily table
    var changes = JSON.stringify($table_daily.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));

    // Send an AJAX POST request to the '/validated/daily_save/' endpoint with the gathered data
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
            // Show a loading state in the daily and detail tables
            $table_daily.bootstrapTable('showLoading');
            $table_detail.bootstrapTable('showLoading');
        },
        success: function (data) {
            // If the request is successful and the server responds with `result: true`
            if (data.result == true){
                // Show a success message, hide the information div, clean the filters, remove all rows from the daily and detail tables
                $("#div_body_message").html('Data saved correctly to Validated!')
                $("#div_validation_message").modal("show");
                $("#div_information").hide();
                clean_filters('daily');
                clean_filters('detail');
                $table_detail.bootstrapTable('removeAll');
                $table_daily.bootstrapTable('removeAll');
            }
            else{
                // If the server responds with `result: false`, show an error message
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");
            }
            // Hide the loading state in the daily and detail tables
            $table_daily.bootstrapTable('hideLoading');
            $table_detail.bootstrapTable('hideLoading');
        },
        error: function () {
            // If the request fails, show an error message and hide the loading state in the daily table
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table_daily.bootstrapTable('hideLoading');
        }
    });
}


/**
 * This function saves detail data by sending an AJAX POST request to the '/validated/detail_save/' endpoint.
 * @param {Object} event - The event object that triggered the function.
 */
function save_detail(event){
    // Select the detail table
    var $table = $('#table_detail');

    // Gather various pieces of data from the page
    var token = $("input[name='csrfmiddlewaretoken']").val();
    var station_id = $("#id_station").val();
    var variable_id = $("#id_variable").val();

    // Get the current data in the detail table
    var data = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));

    // Send an AJAX POST request to the '/validated/detail_save/' endpoint with the gathered data
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
            // Show a loading state in the detail table
            $table.bootstrapTable('showLoading');
        },
        success: function (response) {
            // If the request is successful and the server responds with `result: true`
            if (response.result == true){
                // Show a success message, hide the detail tab, clean the filters, destroy the detail table, and refresh the daily data
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
                // If the server responds with `result: false`, show an error message and hide the loading state in the detail table
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");
                $table.bootstrapTable('hideLoading');
            }
        },
        error: function () {
            // If the request fails, show an error message and hide the loading state in the detail table
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });
}


/**
 * This function submits a daily query by sending an AJAX POST request to the endpoint specified in the form's action attribute.
 * It then processes the response and updates the page accordingly.
 */
function daily_query_submit(){
    // Select the daily table and get the variable id
    var $table_daily = $('#table_daily');
    var var_id = $("#id_variable").val();

    // Initialize error flag and message
    var flag_error = false;
    var message = '';

    // Clean filters and get start and end dates
    $("#orig_variable_id").val(var_id);
    $("#div_information").html('');
    clean_filters('daily');
    clean_filters('detail');
    start_date = document.querySelector('input[name="start_date"]').value;
    end_date = document.querySelector('input[name="end_date"]').value;

    // Check if dates are provided
    if( start_date == '' || end_date == '')
    {
        // If not, show a message and return
        $("#div_message_dates").show("slow");
        $("#div_c").html("");
    }
    else {
        // If dates are provided, hide the message and send the AJAX request
        $("#div_message_dates").hide();
        $("#div_c").html("");
        $.ajax({
            url: $("#form_validation").attr('action'),
            data: $("#form_validation").serialize(),
            type:'POST',
            beforeSend: function () {
                // Show a loading state in the daily table
                $table_daily.bootstrapTable('showLoading');
            },
            success: function (data) {
                // Process the response
                $("#btn_submit").attr("disabled", false);
                for (var key in data){
                    // If there's an error, set the error flag and message
                    if (key == 'error'){
                        flag_error = true;
                        message = data.error;
                    }
                }
                // If there's an error, show the error message and return
                if (flag_error == true){
                    $table_daily.bootstrapTable('hideLoading');
                    $("#div_body_message").html(message)
                    $("#div_validation_message").modal("show");
                    return;
                }

                // If there's no data, show a message and return
                if (data.data.length < 1){
                    $("#div_information").show("slow");
                    $("#div_information").html('<div><h1 style="background-color : red">No hay datos</h1></div>');
                    return;
                }

                // Update the page with the response data
                $("#div_c").html(data.curva);
                if (data.variable.is_cumulative){
                    bar_plot(data.series, "div_information", data.variable);
                }else{
                    dispersion_plot(data.series, "div_information", data.variable);
                }

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
                // If the request fails, show an error message and hide the loading state in the daily table
                $table_daily.bootstrapTable('hideLoading');
                $("#div_body_message").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_validation_message").modal("show");
            }
        });
    }

    // Click the first tab
    var tab1 = document.getElementById("tab1-tab");
    tab1.click();
}


/**
 * This function is used to switch between different tabs in a tabbed interface.
 * @param {Object} evt - The event object that triggered the function.
 * @param {string} tabName - The id of the tab to be displayed.
 */
function getTab(evt, tabName) {
    var i, tabpane;

    // Get all the tab panes
    tabpane = document.getElementsByClassName("tab-pane");

    // Loop through all the tab panes and hide them
    for (i = 0; i < tabpane.length; i++) {
        tabpane[i].style.display = "none";
        tabpane[i].classList.remove("show");
    }

    // Get the tab pane to be displayed and show it
    var e = document.getElementById(tabName);
    e.classList.add("show");
    e.style.display = "";
}



/**
 * This function checks if a given date exists in a data array.
 * @param {string} fecha - The date to be checked.
 * @param {Array} datos - The data array where the date will be checked.
 * @returns {Array} - An array of data that matches the given date.
 */
function get_existe_en_tabla(fecha, datos){
    // The 'debugger' statement has been commented out as it's used for debugging purposes and should not be in production code
    //debugger;

    // Initialize a flag to check if the date exists in the data
    var existe = false;

    // Filter the data array to get data that matches the given date
    return datos.filter(
        function(datos){
            // If the date of the current data matches the given date, set the 'existe' flag to true
            // This line has been commented out as it's not being used
            //if(datos.fecha == fecha)
                //existe = true

            // Return true if the date of the current data matches the given date, false otherwise
            return datos.fecha == fecha
        }
    )
}



/**
 * This function modifies a row in the detail table.
 * @param {Object} event - The event object that triggered the function.
 */
function detail_modify_row(event){
    // Enable the detail time input
    $('input[name="detail_time"]').attr('disabled',false);

    // Get the variable id from the form
    var variable_id = parseInt($("#id_variable").val());

    // Select the modify form and the modal
    var $form = $("#form_modify");
    var inputs =$form.serializeArray();
    var $modal = $("#modal_modify");

    // Initialize an empty data object and select the detail table
    var data = {};
    var table = $table = $("#table_detail");

    // Loop through the form inputs
    $.each(inputs, function(i, field){
        // If the input name includes 'detail_', process it
        if (field.name.includes('detail_')) {
            var _field = field.name.split("_")[1];

            // If the field is included in the detail table value columns or is 'id' or 'time', add it to the data object
            if(detail_table_value_columns.includes(_field) || ['id', 'time'].includes(_field)){
                data[_field] = field.value;
            }
        }
    });

    // Get the id from the data object and remove it from the object
    id = data['id'];
    delete data['id'];

    // Set 'is_selected' to true in the data object
    data['is_selected'] = true;

    // Loop through the detail table value columns and add error values to the data object
    for (const c of detail_table_value_columns) {
        data[ c + '_error'] = get_value_error(data[c])
    }

    // Set 'stddev_error' to false in the data object
    data['stddev_error'] = false;

    // Update the row in the detail table with the data object
    $table.bootstrapTable('updateByUniqueId',{
        id: id,
        row: data
    });

    // Hide the modal
    $modal.modal('hide');
}


/**
 * This function saves a new row in the detail table.
 * @param {Object} event - The event object that triggered the function.
 */
function detail_new_save(event){
    // Get the variable id from the form
    var variable_id = parseInt($("#id_variable").val());

    // Select the new form and the modal
    var $form = $("#form_new");
    var inputs =$form.serializeArray();
    var $modal = $("#modal_new");

    // Initialize an empty data object and select the detail table
    var data = {};
    var table = $table = $("#table_detail");

    // Loop through the form inputs
    $.each(inputs, function(i, field){
        // If the input name includes 'new_', process it
        if (field.name.includes('new_')) {
            var _field = field.name.split("_")[1];

            // If the field is included in the detail table value columns or is 'date' or 'hour', add it to the data object
            // and clear the input field
            if(detail_table_value_columns.includes(_field) || ['date', 'hour'].includes(_field)){
                data[_field] = field.value;
                $('input[name="'+field.name+'"]').val("");
            }
        }
    });

    // Combine 'date' and 'hour' to create 'time' and add it to the data object
    // Then remove 'date' and 'hour' from the data object
    data['time'] = data['date'] + ' ' + data['hour'];
    delete data['date'];
    delete data['hour'];

    // Set 'is_selected' to true in the data object
    data['is_selected'] = true;

    // Get the last row in the detail table and get its id
    // Then increment the id and add it to the data object
    var last_row = $table.bootstrapTable('getData').slice(-1);
    var last_id = parseInt(last_row[0]['id']);
    data['id'] = last_id + 1;

    // Append the data object as a new row in the detail table and scroll to the bottom of the table
    $table.bootstrapTable('append', data);
    $table.bootstrapTable('scrollTo', 'bottom');

    // Hide the modal
    $modal.modal('hide');
}


/**
 * This function checks rows in the detail table based on the ids provided in the detail selection input.
 * @param {Object} event - The event object that triggered the function.
 */
function check(event){
    // Get the name of the current target of the event
    var name = event.currentTarget.name;

    // Initialize the detail selection text and the table
    var tx_selection = '';
    var $table = '';

    // If the name is 'detail', select the detail table and get the detail selection text
    if (name === 'detail'){
        $table = $("#table_detail");
        tx_selection = $("#txt_detail_selection").val().toString();
    }
    else{
        // If the name is not 'detail', do nothing
    }

    // Show a loading state in the table
    $table.bootstrapTable('showLoading');

    // Split the detail selection text on ',' and '-'
    var arr_id = tx_selection.split(',');
    var arr_range = tx_selection.split('-');

    // Initialize an empty ids array
    var ids = []

    // If there are multiple ids, map them to integers and add them to the ids array
    if (arr_id.length>1){
        ids = arr_id.map(function(id){
            return parseInt(id)
        });
    }

    // If there is a range of ids, generate all the ids in the range and add them to the ids array
    if (arr_range.length>0){
        var start = parseInt(arr_range[0]);
        var end = parseInt(arr_range[1]);

        for (var id = start; id <= end; id++){
            ids.push(id);
        }
    }

    // Check the rows in the table that match the ids in the ids array
    $table.bootstrapTable('checkBy', {field: 'id', values: ids})

    // Hide the loading state in the table and clear the detail selection input
    $table.bootstrapTable('hideLoading');
    $("#txt_detail_selection").val("");
}


/**
 * This function unchecks rows in the detail table based on the ids provided in the detail selection input.
 * @param {Object} event - The event object that triggered the function.
 */
function uncheck(event){
    // Get the name of the current target of the event
    var name = event.currentTarget.name;

    // Initialize the detail selection text and the table
    var tx_selection = '';
    var $table = '';

    // If the name is 'detail', select the detail table and get the detail selection text
    if (name === 'detail'){
        $table = $("#table_detail");
        tx_selection = $("#txt_detail_selection").val().toString();
    }
    else{
        // If the name is not 'detail', do nothing
    }

    // Show a loading state in the table
    $table.bootstrapTable('showLoading');

    // Split the detail selection text on ',' and '-'
    var arr_id = tx_selection.split(',');
    var arr_range = tx_selection.split('-');

    // Initialize an empty ids array
    var ids = []

    // If there are multiple ids, map them to integers and add them to the ids array
    if (arr_id.length>1){
        ids = arr_id.map(function(id){
            return parseInt(id)
        });
    }

    // If there is a range of ids, generate all the ids in the range and add them to the ids array
    if (arr_range.length>0){
        var start = parseInt(arr_range[0]);
        var end = parseInt(arr_range[1]);

        for (var id = start; id <= end; id++){
            ids.push(id);
        }
    }

    // Uncheck the rows in the table that match the ids in the ids array
    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids})

    // Hide the loading state in the table and clear the detail selection input
    $table.bootstrapTable('hideLoading');
    $("#txt_detail_selection").val("");
}

/**
 * This function fetches and displays detail data for a specific row in the detail table.
 * @param {Object} e - The event object that triggered the function.
 * @param {Object} value - The value of the clicked cell.
 * @param {Object} row - The data of the clicked row.
 */
function detail_details(e, value, row){
    // Select the detail table and get the station and variable ids
    var $table = $('#table_detail');
    var station_id = $("#id_station").val();
    var variable_id = $("#id_variable").val();

    // Initialize the daily id and date
    var id_daily = 0;
    var date = '';

    // If a row was clicked, get the id and date from the row
    // Otherwise, get the original daily id and date
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

    // Update the original detail date
    date = row.date;
    $("#orig_detail_date").val(date);

    // Get the maximum and minimum variables
    var var_maximum = $("#id_maximum").val();
    var var_minimum = $("#id_minimum").val();

    // Construct the url for the detail list
    url = '/validated/detail_list/' + station_id + '/' + variable_id + '/' + date + '/' + var_minimum + '/' + var_maximum;

    // Send a GET request to the detail list url
    $.ajax({
        url: url,
        type:'GET',
        beforeSend: function () {
            // Show a loading state in the table
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            // On success, display the third tab and click it
            document.getElementById("tab3-tab").style.display = "block";
            document.getElementById("tab3-tab").click();

            // Update the detail table value columns and the json data
            detail_table_value_columns = data.value_columns;
            json_data = data.series;

            // Destroy the current table
            $table.bootstrapTable('destroy');

            // Update the indicators and their spans
            for (const index in data.indicators){
                indicators_subhourly[index] = data.indicators[index];
                $("#span_"+index+"_detail").text(indicators_subhourly[index]);
            }

            // Replace 'T' with ' ' in the time of each element in the json data
            for (const element of json_data) {
                element["time"] = (element['time']).replace('T',' ');
            }

            // Get the columns for the detail table
            var columns = get_columns_detail(variable_id, data.value_columns);

            // Initialize the table with the columns and data
            $table.bootstrapTable({
                columns:columns,
                data: json_data,
                rowStyle: style_row,
                height: 370,
            });

            // Hide the loading state in the table
            $table.bootstrapTable('hideLoading');
        },
        error: function () {
            // On error, display a validation message
            $("#div_body_message").html('An issue occurred with the validation. Please contact the administrator.')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });
};




/**
 * This function opens a form for adding a new row to the detail table.
 * @param {Object} event - The event object that triggered the function.
 */
function open_form_new(event){
    // Get the original detail date and variable id
    var date = $("#orig_detail_date").val();
    var variable_id = parseInt($("#id_variable").val());

    // Select the form modal and the form
    var $form_modal = $('#modal_new');
    var $form = "#form_new";

    // Get the form inputs
    var inputs = $("#form_new").serializeArray();

    // Loop through the form inputs
    $.each(inputs, function(i, field){
        // If the input name includes 'new_', process it
        if (field.name.includes('new_')) {
            var _field = field.name.split("_")[1];

            // If the field is included in the detail table value columns or is 'date' or 'hour', show the input field
            // Otherwise, hide the input field
            if(detail_table_value_columns.includes(_field) || ['date', 'hour'].includes(_field)){
                $('input[name="'+field.name+'"]').parent().show();
            }else{
                $('input[name="'+field.name+'"]').parent().hide();
            }
        }
    });

    // Set the value of the 'new_date' input field to the original detail date and show the form modal
    $($form+',input[name="new_date"]').val(date);
    $form_modal.modal("show");
}



/**
 * This function opens a form for updating a specific row in the detail table.
 * @param {Object} e - The event object that triggered the function.
 * @param {Object} value - The value of the clicked cell.
 * @param {Object} row - The data of the clicked row.
 * @param {number} index - The index of the clicked row.
 */
function open_form_update(e, value, row, index){
    // Select the form modal and get the form inputs
    var $form_modal = $('#modal_modify');
    var inputs = $("#form_modify").serializeArray();

    // Loop through the form inputs
    $.each(inputs, function(i, field){
        // If the input name includes 'detail_', process it
        if (field.name.includes('detail_')) {
            var _field = field.name.split("_")[1];

            // If the field is included in the detail table value columns or is 'id' or 'time', show the input field and set its value to the corresponding row value
            // Otherwise, hide the input field
            if(detail_table_value_columns.includes(_field) || ['id', 'time'].includes(_field)){
                $('input[name="'+field.name+'"]').parent().show();
                $('input[name="'+field.name+'"]').val(row[_field]);
            }else{
                $('input[name="'+field.name+'"]').parent().hide();
            }
        }
    });

    // Disable the 'detail_time' input field and show the form modal
    $('input[name="detail_time"]').attr('disabled',true);
    $form_modal.modal("show");
}


/**
 * This function generates the column configuration for the daily table.
 * @param {number} var_id - The variable id.
 * @param {Array} value_columns - The value columns to include in the table.
 * @returns {Array} The column configuration for the table.
 */
function get_columns_daily(var_id, value_columns){
    // Initialize an empty array for the columns
    var columns = [];

    // Define the state column and add it to the columns array
    var state = {
        field:'state',
        checkbox:true
    };
    columns.push(state);

    // Define the id column and add it to the columns array
    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id
    };
    columns.push(id);

    // Define the date column and add it to the columns array
    var date = {
        field:'date',
        title: 'Date',
        cellStyle: style_date,
        formatter: format_value,
        footerFormatter: footer_date,
    };
    columns.push(date);

    // Define the percentage column and add it to the columns array
    var percentage = {
        field:'percentage',
        title:'Percnt.',
        cellStyle: style_percentage,
        footerFormatter: footer_average,
    };
    columns.push(percentage);

    // If the value columns include 'sum', define the sum column and add it to the columns array
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

    // If the value columns include 'average', define the average column and add it to the columns array
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

    // If the value columns include 'maximum', define the maximum column and add it to the columns array
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

    // If the value columns include 'minimum', define the minimum column and add it to the columns array
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

    // Define the value difference column and add it to the columns array
    var value_difference = {
        field:'value_difference_error_count',
        title:'Diff. Err',
        cellStyle: style_value_diff,
        formatter: format_value,
        footerFormatter: footer_value_diff
    };
    columns.push(value_difference);

    // Define the action column and add it to the columns array
    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_daily,
        events: {
           'click .search': detail_details,
        }
    };
    columns.push(action);

    // Return the columns array
    return columns
}


/**
 * This function generates the column configuration for the detail table.
 * @param {number} var_id - The variable id.
 * @param {Array} value_columns - The value columns to include in the table.
 * @returns {Array} The column configuration for the table.
 */
function get_columns_detail(var_id, value_columns){
    // Initialize an empty array for the columns
    var columns = [];

    // Define the is_selected column and add it to the columns array
    var is_selected = {
        field:'is_selected',
        checkbox:true,
    };
    columns.push(is_selected);

    // Define the id column and add it to the columns array
    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id,
        footerFormatter: footer_id
    };
    columns.push(id);

    // Define the time column and add it to the columns array
    var time = {
        field:'time',
        title:'Time',
        cellStyle: style_detail_time,
        footerFormatter: footer_data_count
    };
    columns.push(time);

    // Define the time_lapse_status column and add it to the columns array
    var time_lapse_status = {
        field:'time_lapse_status',
        visible: false,
    };
    columns.push(time_lapse_status);

    // Loop through the detail table value columns
    for (const c of detail_table_value_columns) {
        // Define the value column and add it to the columns array
        var value_column = {
            field: c,
            title: c.charAt(0).toUpperCase() + c.slice(1),
            cellStyle: style_detail_value_error,
            footerFormatter: footer_average
        };
        // If the column is 'sum', update the cellStyle and footerFormatter of the value column
        if ( c == 'sum'){
            value_column.cellStyle = style_detail_value_error;
            value_column.footerFormatter = footer_sum;
        }
        columns.push(value_column);

        // Define the value_column_error column and add it to the columns array
        var value_column_error = {
            field: c + '_error',
            visible: false,
        };
        columns.push(value_column_error);
    }

    // Define the outlier_err column and add it to the columns array
    var outlier_err = {
        field:'stddev_error',
        title:'Outliers',
        cellStyle: style_stddev_err,
        formatter: format_stddev_err,
        footerFormatter: footer_stddev_err
    };
    columns.push(outlier_err);

    // Define the value_difference column and add it to the columns array
    var value_difference = {
        field:'value_difference',
        title:'Value diff.',
        cellStyle: style_detail_value_diff,
        footerFormatter: footer_detail_value_diff
    };
    columns.push(value_difference);

    // Define the value_diff_error column and add it to the columns array
    var value_diff_error = {
        field:'value_difference_error',
        visible: false,
    };
    columns.push(value_diff_error);

    // Define the action column and add it to the columns array
    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_detail,
        events: {
           'click .update': open_form_update
        }
    };
    columns.push(action);

    // Return the columns array
    return columns
}


/**
 * This function generates the action buttons for each row in the daily table.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {string} The HTML string for the action buttons.
 */
function operate_table_daily(value, row, index) {
        // Return the HTML string for the action buttons
        // The 'search' button is used to view the details of the row
        return [
            '<a class="search" href="javascript:void(0)" title="Detail">',
            '<i class="fa fa-search"></i>',
            '</a>  ',
        ].join('')
}



/**
 * This function generates the action buttons for each row in the detail table.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {string} The HTML string for the action buttons.
 */
function operate_table_detail(value, row, index) {
        // Return the HTML string for the action buttons
        // The 'update' button is used to modify the details of the row
        return [
            '<a class="update" href="javascript:void(0)" title="Modify">',
            '<i class="fa fa-edit"></i>',
            '</a>  ',
        ].join('')
}


/**
 * This function styles a row in the table based on its state.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the row.
 */
function style_row(row, index){
        // Initialize an empty string for the class
        var _class = '';

        // If the state of the row is false, set the class to 'error'
        if (row.state == false) {
            _class = 'error';
        }
        // Otherwise, keep the class as an empty string
        else {
                _class = '';
        }

        // Return the class to apply to the row
        return {classes: _class}

        // The following commented out code would set the class to 'normal' if the row is selected
        // var _class = '';
        // if (row.is_selected) {
        //   _class = 'normal';
        // }
        // return {classes: _class}
}


/**
 * This function styles the id column in the table based on the row's validation status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_id(value, row, index){
    // Initialize an empty string for the class
    var _class = '';

    // If all the data in the row is validated, set the class to 'validated'
    if (row.all_validated == true){
        _class = 'validated';
    }
    // If the row is not selected (assuming 'seleccionado' means 'selected' in Spanish), set the class to 'error'
    else if (row.seleccionado == false){
        _class = 'error';
    }
    // If neither of the above conditions are met, keep the class as an empty string
    else{
        _class = '';
    }

    // Return the class to apply to the cell
    return { classes: _class}
}


/**
 * This function styles the date column in the table based on the row's date error status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_date(value, row, index){
    // Initialize an empty string for the class
    var _class = '';

    // If the date error status of the row is greater than 0, set the class to 'error'
    if (row.date_error > 0){
        _class = 'error';
    }
    // Otherwise, keep the class as an empty string
    else{
        _class = '';
    }

    // Return the class to apply to the cell
    return { classes: _class}
}

/**
 * This function styles the percentage column in the table based on the row's percentage error status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_percentage(value, row, index) {
    // If the percentage error status of the row is true, set the class to 'error'
    if (row.percentage_error == true) {
        return {
            classes: 'error'
        }
    }
    // Otherwise, set the class to 'normal'
    else{
        return {
            classes: 'normal'
        }
    }
}


/**
 * This function styles the value column in the table based on the row's suspicious count for the field.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @param {string} field - The field to check for suspicious count.
 * @returns {Object} The class to apply to the cell.
 */
function style_value(value, row, index, field){
    // Initialize an empty string for the class
    var _class = '';

    // Create the field value by appending "suspicious_" and "s_count" to the field
    var field_value = "suspicious_" + field +"s_count";

    // If the suspicious count for the field in the row is greater than 0, set the class to 'error'
    if (row[field_value]>0 )
        _class = 'error';
    // Otherwise, set the class to 'normal'
    else
        _class = 'normal';

    // Return the class to apply to the cell
    return { classes: _class}
}


/**
 * This function styles the value difference column in the table based on the row's value difference error count.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_value_diff(value, row, index){
    // Initialize an empty string for the class
    var _class = '';

    // If the value difference error count of the row is greater than or equal to 1, set the class to 'error'
    if (row.value_difference_error_count >= 1)
        _class = 'error';
    // Otherwise, keep the class as an empty string
    else
        _class = '';

    // Return the class to apply to the cell
    return { classes: _class}
}




/**
 * This function styles the detail time column in the table based on the row's time lapse status and selection status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_detail_time(value, row, index){
    // Initialize an empty string for the class
    var _class = '';

    // If the time lapse status of the row is 0 or any other value not covered by the conditions, set the class to 'error'
    if (row.time_lapse_status == 0 || row.time_lapse_status != 1 && row.time_lapse_status != 2){
        _class = 'error';
    }
    // If the time lapse status of the row is 2, set the class to 'warning'
    else if (row.time_lapse_status == 2){
        _class = 'warning';
    }
    // If the time lapse status of the row is 1 and the row is selected, set the class to 'normal'
    else if (row.time_lapse_status == 1){
        if (row.is_selected){
            _class = 'normal';
        }
    }

    // Return the class to apply to the cell
    return { classes: _class}
}

/**
 * This function styles the detail value error column in the table based on the row's field error status and selection status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @param {string} field - The field to check for error status.
 * @returns {Object} The class to apply to the cell.
 */
function style_detail_value_error(value, row, index, field){
    // Initialize an empty string for the class
    var _class = '';

    // Create the field error by appending "_error" to the field
    var field_error = field + '_error';

    // If the field error status of the row is true, set the class to 'error'
    if (row[field_error] === true){
        _class = 'error';
    }
    // If the row is selected, set the class to 'normal'
    else if (row.is_selected){
        _class = 'normal';
    }

    // Return the class to apply to the cell
    return { classes: _class};
}


/**
 * This function styles the standard deviation error column in the table based on the cell's value and the row's selection status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_stddev_err(value, row, index){
    // Initialize an empty string for the class
    var _class = '';

    // If the value of the cell is true, set the class to 'error'
    if (value === true)
    {
        _class = 'error';
    }
    // If the row is selected, set the class to 'normal'
    else if (row.is_selected){
        _class = 'normal';
    }

    // Return the class to apply to the cell
    return { classes: _class}
}


/**
 * This function styles the detail value difference column in the table based on the row's value difference error status and selection status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @returns {Object} The class to apply to the cell.
 */
function style_detail_value_diff(value, row, index){
    // Initialize an empty string for the class
    var _class = '';

    // If the value difference error status of the row is true, set the class to 'error'
    if (row.value_difference_error)
    {
        _class = 'error';
    }
    // If the row is selected, set the class to 'normal'
    else if (row.is_selected){
        _class = 'normal';
    }

    // Return the class to apply to the cell
    return { classes: _class}
}







/**
 * This function formats the value of a cell in the table based on the field and the row's error status.
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @param {string} field - The field to check for error status.
 * @returns {string} The formatted content to display in the cell.
 */
function format_value(value, row, index, field){
    // Initialize a span for the badge with a placeholder for the number of errors
    var span = '<span class="badge badge-light">num</span>';
    // Initialize the content with the value of the cell
    var content = value;
    var errors_field;

    // If the field is one of the specified fields, set the errors_field to the suspicious count for the field
    if (["sum", "average", "value", "maximum", "minimum"].includes(field)){
        errors_field = "suspicious_" + field +"s_count";
    }
    // If the field is "value_difference_error_count", set the errors_field to "value_difference_error_count" and clear the content
    else if (field == "value_difference_error_count"){
        errors_field = "value_difference_error_count";
        content = "";
    }
    // Otherwise, set the errors_field to the error status for the field
    else{
        errors_field = field +"_error";
    }

    // If the error count for the errors_field in the row is greater than 0, add the badge to the content
    if (row[errors_field]>0 ){
        span = span.replace('num',row[errors_field].toString());
        content = content + ' ' + span;
    }

    // Return the formatted content
    return content
}

/**
 * This function formats the standard deviation error cell in the table.
 * If the value is truthy, it returns "X", otherwise it returns "-".
 * @param {Object} value - The value of the cell.
 * @param {Object} row - The data of the row.
 * @param {number} index - The index of the row.
 * @param {string} field - The field to check for error status.
 * @returns {string} The formatted content to display in the cell.
 */
function format_stddev_err(value, row, index, field){
    // If the value is truthy, return "X"
    if (value){
        return "X";
    }
    // Otherwise, return "-"
    return "-";
}



/**
 * This function generates a footer id for a table.
 * It counts the number of rows where 'state' is truthy and 'is_selected' is false, and displays this count in a badge.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer id to display in the table.
 */
function footer_id(data){
    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Use the reduce function to count the number of rows where 'state' is truthy and 'is_selected' is false
    var num_date = data.reduce(function(num, i){
        // If 'state' is truthy and 'is_selected' is false, increment the count
        if (i['state'] && i['is_selected']==false)
            return num + 1;
        // Otherwise, keep the count the same
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num',num_date.toString());

    // Return the span to display in the table
    return span;
}


/**
 * This function generates a footer for a table that displays the number of unique dates and the total number of days.
 * It also displays a badge with the number of rows where 'date_error' is greater than 0.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_date(data){
    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Get the selected variable id
    var var_id = $("#id_variable").val();

    // Initialize an empty array for the dates
    var dates = [];

    // Use the map function to add each row's date to the dates array
    $.map(data, function(row){
        dates.push(row.date);
    });

    // Count the number of unique dates
    var sum = dates.unique().length;

    // Use the reduce function to count the number of rows where 'date_error' is greater than 0
    var num_date = data.reduce(function(num, i){
        if (i['date_error']>0)
            return num +1;
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num', num_date.toString());

    // Return the sum of unique dates, the total number of days, and the span to display in the table
    return sum + ' of ' + indicators_daily['num_days'] + ' days ' + span;
}


/**
 * This function generates a footer for a table that displays the average of a field and a badge with the number of errors.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_average(data){
    // Get the field from the context of the function
    var field = this.field;
    // Create the field error by appending "_error" to the field
    var field_error = field + '_error';

    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Initialize the mean and the sum
    var mean = 0;

    // Use the reduce function to calculate the sum of the field for rows where 'state' is truthy and the field is not null or empty
    var sum = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "")
            return sum + parseFloat(i[field])
        else
            return sum;
    }, 0);

    // Use the reduce function to count the number of rows where 'state' is truthy and the field is not null or empty
    var data_count = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "")
            return sum + 1;
        else
            return sum;
    }, 0);

    // Use the reduce function to count the number of rows where the field error is truthy and 'state' is truthy
    var num_value = data.reduce (function (num, i){
        if (i[field_error] && i['state'])
            return num + 1;
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num', num_value);

    // If the sum is not a number, set the mean to "-"
    if (isNaN(sum))
        mean = '-';
    // Otherwise, calculate the mean by dividing the sum by the count and rounding to 2 decimal places
    else
        mean = (sum / data_count).toFixed(2);

    // Return the mean and the span to display in the table
    return mean + ' ' + span;
}




/**
 * This function generates a footer for a table that displays the sum of a field and a badge with the number of errors.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_sum(data){
    // Get the field from the context of the function
    var field = this.field;
    // Create the field error by appending "_error" to the field
    var field_error = this.field + '_error';

    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Use the reduce function to calculate the sum of the field for rows where 'state' is truthy and the field is not null or empty
    var sum = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "" ){
            return sum + parseFloat(i[field])
        }
        else{
            return sum
        }
    }, 0);

    // Use the reduce function to count the number of rows where the field error is truthy and 'state' is truthy
    var num_value = data.reduce (function (sum, i){
        if (i[field_error] && i['state'])
            return sum +1 ;
        else
            return sum;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num', num_value);

    // Return the sum (rounded to 2 decimal places) and the span to display in the table
    return sum.toFixed(2) + ' ' + span;
}


/**
 * This function generates a footer for a table that displays a badge with the count of rows where 'value_difference_error_count' is greater than or equal to 1.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_value_diff(data){
    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Use the reduce function to count the number of rows where 'value_difference_error_count' is greater than or equal to 1
    var num_vd = data.reduce(function(num, i){
        if (i['value_difference_error_count'] >= 1 )
            return num + 1;
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num', num_vd);

    // Return the span to display in the table
    return span;
}



/**
 * This function generates a footer for a table that displays the count of rows where 'state' is truthy and a badge with the count of rows where 'time_lapse_status' is 0, 2, or 3.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_data_count(data){
    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Use the reduce function to count the number of rows where 'state' is truthy
    var sum = data.reduce(function (sum, i) {
        if (i['state']){
            return sum + 1
        }
        else{
            return sum
        }
    }, 0);

    // Use the reduce function to count the number of rows where 'time_lapse_status' is 0, 2, or 3
    var num_date = data.reduce(function(num, i){
        // TODO check logic
        if ( (i['time_lapse_status']==0) || (i['time_lapse_status']==2) || (i['time_lapse_status']==3))
            return num +1;
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num',num_date.toString());

    // Return the count of rows where 'state' is truthy, the total number of data, and the span to display in the table
    return sum + ' of ' + indicators_subhourly['num_data'] + '. ' + span;
}



/**
 * This function generates a footer for a table that displays a badge with the count of rows where 'stddev_error' is truthy and 'state' is also truthy.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_stddev_err(data){
    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Use the reduce function to count the number of rows where 'stddev_error' is truthy and 'state' is also truthy
    var num_stddev = data.reduce(function(num, i){
        if (i['stddev_error'] && i['state'])
            return num +1;
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num',num_stddev.toString());

    // Return the span to display in the table
    return span;
}

/**
 * This function generates a footer for a table that displays a badge with the count of rows where 'value_difference_error' is truthy.
 * @param {Array} data - The data of the table.
 * @returns {string} The footer to display in the table.
 */
function footer_detail_value_diff(data){
    // Initialize a span for the badge with a placeholder for the number
    var span = '<span class="badge badge-danger">num</span>';

    // Use the reduce function to count the number of rows where 'value_difference_error' is truthy
    var num_vde = data.reduce(function(num, i){
        if (i['value_difference_error'])
            return num + 1;
        else
            return num;
    }, 0);

    // Replace the placeholder in the span with the count
    span = span.replace('num', num_vde.toString());

    // Return the span to display in the table
    return span;
}






/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_time(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'shorter_than_tx_period', set the filter to [0]
    if (option == 'shorter_than_tx_period')
        filter = [0];
    // If the option is 'greater_than_tx_period', set the filter to [2]
    else if (option == 'greater_than_tx_period')
        filter = [2];
    // For any other option, set the filter to [0, 1, 2]
    else
        filter = [0, 1, 2];

    // Return the filter
    return filter;
}

/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_percentage(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'error', set the filter to [true]
    if (option == 'error')
        filter = [true];
    // If the option is 'normal', set the filter to [false]
    else if (option == 'normal')
        filter = [false];
    // For any other option, set the filter to [true, false]
    else
        filter = [true, false];

    // Return the filter
    return filter;
}

/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_value(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'error', set the filter to [true]
    if (option == 'error')
        filter = [true];
    // If the option is 'normal', set the filter to [false]
    else if (option == 'normal')
        filter = [false];
    // For any other option, set the filter to [true, false, null]
    else
        filter = [true, false, null];

    // Return the filter
    return filter;
}


/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_stddev(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'error', set the filter to [true]
    if (option == 'error')
        filter = [true];
    // If the option is 'normal', set the filter to [false]
    else if (option == 'normal')
        filter = [false];
    // For any other option, set the filter to [true, false, null]
    else
        filter = [true, false, null];

    // Return the filter
    return filter;
}


/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_stddev(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'error', set the filter to [true]
    if (option == 'error')
        filter = [true];
    // If the option is 'normal', set the filter to [false]
    else if (option == 'normal')
        filter = [false];
    // For any other option, set the filter to [true, false, null]
    else
        filter = [true, false, null];

    // Return the filter
    return filter;
}


/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_selected(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'selected', set the filter to [true]
    if (option == 'selected')
        filter = [true];
    // If the option is 'non-selected', set the filter to [false]
    else if (option == 'non-selected')
        filter = [false];
    // For any other option, set the filter to [true, false]
    else
        filter = [true, false];

    // Return the filter
    return filter;
}


/**
 * This function returns a filter based on the provided option.
 * @param {string} option - The option to determine the filter.
 * @returns {Array} The filter to be used.
 */
function get_filter_value_difference(option){
    // Initialize an empty filter array
    var filter = [];

    // If the option is 'error', set the filter to [true]
    if (option == 'error')
        filter = [true];
    // If the option is 'normal', set the filter to [false]
    else if (option == 'normal')
        filter = [false];
    // For any other option, set the filter to [true, false, null]
    else
        filter = [true, false, null];

    // Return the filter
    return filter;
}

/**
 * This function filters the detail table based on the selected options from the user interface.
 */
function filter_detail_table(){
    // Get the selected options from the user interface
    var time = $("#chk_detail_time").val();
    var value = $("#chk_detail_value").val();
    var stddev = $("#chk_detail_stddev").val();
    var selected = $("#chk_detail_selected").val();
    var value_difference = $("#chk_detail_value_difference").val();

    // Get the filters based on the selected options
    var filter_time = get_filter_time(time);
    var filter_value = get_filter_value(value);
    var filter_stddev = get_filter_stddev(stddev);
    var filter_selected = get_filter_selected(selected);
    var filter_value_difference = get_filter_value_difference(value_difference);

    // Create the filter object
    var filter = {
        is_selected: filter_selected,
        stddev_error: filter_stddev,
        time_lapse_status: filter_time,
        value_difference_error: filter_value_difference,
    };

    // Add the value filter to the main columns
    var main_column = detail_table_value_columns.filter(c => ["sum", "average", "value"].includes(c));
    main_column.forEach(c => filter[c + '_error'] = filter_value);

    // Apply the filter to the table
    $("#table_detail").bootstrapTable('filterBy', filter);
}


/**
 * This function resets the filters based on the provided type.
 * @param {string} type - The type of filters to reset.
 */
function clean_filters(type){
    // If the type is 'detail', reset the detail filters
    if (type == 'detail'){
        // Reset the time filter
        $("#chk_detail_time").prop('selectedIndex',0);
        // Reset the value filter
        $("#chk_detail_value").prop('selectedIndex',0);
        // Reset the stddev filter
        $("#chk_detail_stddev").prop('selectedIndex',0);
        // Reset the selected filter
        $("#chk_detail_selected").prop('selectedIndex',0);
        // Reset the value difference filter
        $("#chk_detail_value_difference").prop('selectedIndex',0);
        // Reset the selection text
        $("#txt_detail_selection").val('');
    }
    else{
        // For daily filters, the reset logic would go here
    }
}

/**
 * This function checks if a given value is within a specified range.
 * @param {number} value - The value to check.
 * @returns {boolean} Returns true if the value is outside the range, false otherwise.
 */
function get_value_error(value){
    // Get the minimum and maximum values from the user interface
    var minimum = Number($("#id_minimum").val());
    var maximum = Number($("#id_maximum").val());

    // Initialize the error flag as false
    var value_error = false;

    // If the value is greater than the maximum or less than the minimum, set the error flag to true
    if (Number(value) > maximum || Number(value) < minimum )
    {
        value_error = true;
    }

    // Return the error flag
    return value_error;
}


/**
 * This function enables or disables the "New" button based on the selected variable ID.
 */
function enable_new(){
    // Get the selected variable ID from the user interface
    var variable_id = $("#id_variable").val();

    // If the variable ID is not "11" or is "4" or "5", enable the "New" button
    if ( variable_id != "11" || variable_id == "4" || variable_id == "5" )
        $("#btn_detail_new").attr("disabled", false);
    // Otherwise, disable the "New" button
    else
        $("#btn_detail_new").attr("disabled", true);
}


Array.prototype.unique=function(a){
  return function(){return this.filter(a)}}(function(a,b,c){return c.indexOf(a,b+1)<0
});

