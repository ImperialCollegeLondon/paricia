
function actualizar_lista(enlace){
  $("#btn_filtrar").attr('disabled',true);
  $.ajax({
    url: enlace,
    data: $("#form_consulta").serialize(),
    type:'POST',
    beforeSend: function () {
      $("#div_informacion").hide();
      $("#div_loading").show();
      $("#div_error").hide();
    },
    success: function (data) {
      $("#div_informacion").show();
      $("#div_informacion").html(data)
      $("#div_loading").hide();
      $("#div_error").hide();
      $("#btn_filtrar").removeAttr('disabled');
    },
    error: function () {
      $("#div_loading").hide();
      $("#div_error").show();
      $("#btn_filtrar").removeAttr('disabled');
    }
  });
}
// Función Abrir Cuadro de Dialogo Bootstrap
function abrir_formulario(enlace, type){
    var $modal_dialog = $("#modal_"+type);
    var $div_data = $("#div_"+type);
    /*var $div_loading = $('#div_loading_'+type);
    var $div_error = $('#div_message_'+type)*/
    $btn_guardar.removeAttr('disabled');
    $btn_borrar.removeAttr('disabled');

    $modal_dialog.modal("show");
    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
            activar_espera(type);
        },
        success: function (data) {
            $div_data.html(data);
            desactivar_espera(type);
        },
        error: function (request, status, error) {
            console.log(request, status, error);
            set_message_error(type);
        }
    });
}

// Guardar registro cuando se crea o se modifica
function guardar_registro(){
    $btn_guardar.attr('disabled',true);
    $.ajax({
        url:$("#form_save").attr('action'),
        type:'POST',
        data: $("#form_save").serialize(),
        beforeSend: function () {
            activar_espera('form');
        },
        success: actualizar_tabla,
        error: set_message_error_form
    });
}

// Función para eliminar un registro
function eliminar_registro(){
    $.ajax({
        url:$("#form_delete").attr('action'),
        type:'POST',
        data: $("#form_delete").serialize(),
        beforeSend: function () {
            activar_espera('delete')
        },
        success: actualizar_tabla,
        error: function (request, status, error) {
            set_message_error(request);
        }
    });

}

// Actualizar tabla
function actualizar_tabla(data){
    console.log(data)
    desactivar_espera('form');
    desactivar_espera('delete');
    var $div_form = $("#div_form");
    var $div_delete = $("#div_delete");
    var div_success = '<div class="alert alert-success">';
    div_success += data.mensaje + '</div>';
    $div_form.html(div_success);
    $div_delete.html(div_success);
    //$modal_form.modal("hide");
    //$btn_guardar.removeAttr('disabled');
    //$btn_borrar.removeAttr('disabled');
    $table.bootstrapTable('refresh');

}

// función para el manejo de errores
function manejar_error(request, status, error){
    // readyState 0, sin respuesta del servidor
    if (request.readyState === 0) {


    }
    // readyState 4, error en el formulacion
    else if (request.readyState === 0)  {

    }

}
// Función para mostrar mensaje de error general
function set_message_error(type){
    var message = '<div class="alert alert-danger alert-dismissible" role="alert">';
    message += 'Existe un problema con el servidor. Por favor contactar con el administrador';
    message += '</div>'
    mostrar_mensaje(type);
    var $div_message = $("#div_message_"+type)
    $div_message.html(message)
}
// Mostrar los errores del Formulario
function set_message_error_form(request, status, error){
    console.log(request, status, error);
    $btn_guardar.removeAttr('disabled');
    var $div_error = $("#div_message_form");
    var $div_data = $("#div_form");
    /*var $div_loading = $("#div_loading_form");
    $div_data.show();
    $div_error.show();
    $div_loading.hide();*/
    mostrar_mensaje('form');
    $div_error.html('');
    $div_data.show();

    var form_field_errors = request.responseJSON.form_field_errors;

    var form_non_field_errors = request.responseJSON.form_non_field_errors;

    if (form_field_errors.length > 0){
        for (i in form_field_errors){
            var div_error = '<div class="alert alert-warning">';
            div_error += form_field_errors[i]['label_tag'] +' : ' ;
            div_error += '<strong>'+form_field_errors[i]['error']+'</strong>';
            div_error += '</div>'

            $div_error.append(div_error);
        }
    }
    if (form_non_field_errors.length>0){
        for (i in form_non_field_errors){
            var div_error = '<div class="alert alert-danger">';
            div_error += form_non_field_errors[i]['error'];
            div_error += '</div>'
            $div_error.append(div_error);

        }
    }

}


function abrir_cuadro_dialogo(div,enlace){
    $("#div_error").hide();
    var object="#"+div;
    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
            $("#div_loading").show();
            $("#div_informacion").hide();
        },
        success: function (data) {
            $(object).html(data);
            $(object).dialog( "open" );
            desactivar_espera()
        },
        error: function () {
            $("#div_loading").hide();
            $("#div_error").show();
        }
    });
    //$(object).dialog( "open" );
}





function cerrar_cuadro_dialogo(){
    var isOpen = $( "#div_edit" ).dialog( "isOpen" );
    console.log(isOpen)
    if (isOpen) {
        $( "#div_edit" ).dialog( "close" );
    }
    isOpen = $( "#div_create" ).dialog( "isOpen" );
    console.log(isOpen)
    if (isOpen) {
        $( "#div_create" ).dialog( "close" );
    }
    isOpen = $( "#div_delete" ).dialog( "isOpen" );
    console.log(isOpen)
    if (isOpen) {
        $( "#div_delete" ).dialog( "close" );
    }
}
/*function activar_espera(){
  $("#div_loading").show();
  $("#div_informacion").hide();
}*/

function activar_espera(type){

    var type = type || ''
    if (type !== '') {
        var $div_data = $('#div_'+type);
        var $div_loading = $('#div_loading_'+type);
        var $div_message = $('#div_message_'+type)
    }
    else{
        var $div_data = $('#div_informacion');
        var $div_loading = $('#div_loading');
        var $div_error = $('#div_error')

    }
    $div_loading.show();
    $div_data.hide();
    $div_message.hide();
}

/*function desactivar_espera(){
  $("#div_loading").hide();
  $("#div_informacion").show();
}*/


function desactivar_espera(type){
    var type = type || ''
    if (type !== '') {
        var $div_data = $('#div_'+type);
        var $div_loading = $('#div_loading_'+type);
        var $div_message = $('#div_message_'+type)
    }
    else{
        var $div_data = $('#div_informacion');
        var $div_loading = $('#div_loading');
        var $div_message = $('#div_error')

    }
    $div_loading.hide();
    $div_data.show();
    $div_message.hide();
}

function mostrar_mensaje(type){
    /*var message = '<div class="alert alert-danger alert-dismissible" role="alert">';
    message += 'Ocurrio un problema con el procesamiento de la información, por favor intentelo nuevamente';
    message += '</div>'*/

    var type = type || ''
    if (type !== ''){
        var $div_data = $('#div_'+type);
        var $div_loading = $('#div_loading_'+type);
        var $div_message = $('#div_message_'+type)
    }
    else{
        var $div_data = $('#div_informacion');
        var $div_loading = $('#div_loading');
        var $div_message = $('#div_error');

    }

    $div_loading.hide();
    $div_data.hide();
    //$div_message.html(message);
    $div_message.show();

}


function actualizar_informacion(){
  $.ajax({
    url: $("#link_consulta").attr('href'),
    type:'GET',
    beforeSend: function () {
      $("#div_informacion").hide();
      $("#div_loading").show();
      $("#div_error").hide();
    },
    success: function (data) {
      $("#div_informacion").show();
      $("#div_informacion").html(data)
      $("#div_loading").hide();
      $("#div_error").hide();

    },
    error: function () {
      $("#div_loading").hide();
      $("#div_error").show();
      $("#div_delete").dialog("open");
    }
  });

}



function getDate(element) {
    var date;
    try {
        date = $.datepicker.parseDate(dateFormat, element.value);
    } catch( error ) {
        date = null;
    }
    return date;
}


$(document).ready(function() {

  $("#form_consulta").submit(function(event){
    //actualizar_lista($("#form_consulta").attr('action'));
    event.preventDefault();
  });
});