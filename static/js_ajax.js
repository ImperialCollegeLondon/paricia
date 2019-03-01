
$(document).ready(function() {
  $( "#div_new" ).dialog({
    autoOpen: false,
    width:400,
    height:400
  });
  $( "#div_update" ).dialog({
    autoOpen: false,
    width:400,
    height:400
  });
  $( "#div_delete" ).dialog({
    autoOpen: false,
    width:400,
    height:400
  });
  $("#link_new").click(function(){
      $("#div_new").dialog("open");
      return false;
  });
  $("#btn_guardar").click(function(){
    $.ajax({
      url: $("#form_new").attr('action'),
      data: $("#form_new").serialize(),
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
        $("#div_new").dialog("close");
      },
      error: function () {
        $("#div_loading").hide();
        $("#div_error").show();
        $("#btn_filtrar").removeAttr('disabled');
        $("#div_new").dialog("close");
      }
    });
    return false;
  });
  //modificar un registro
  $(".link_update").on('click',function(){
    $.ajax({
      url: $(this).attr('href'),
      type:'GET',
      beforeSend: function () {
        $("#div_informacion").hide();
        $("#div_loading").show();
        $("#div_error").hide();
      },
      success: function (data) {
        $("#div_informacion").show();
        $("#div_update").html(data)
        $("#div_loading").hide();
        $("#div_error").hide();
        $("#div_update").dialog("open");
      },
      error: function () {
        $("#div_loading").hide();
        $("#div_error").show();
        $("#div_update").dialog("open");
      }
    });
    return false;
  });

  //eliminar un registro
  $(".link_delete").on('click',function(){
    $.ajax({
      url: $(this).attr('href'),
      type:'GET',
      beforeSend: function () {
        $("#div_informacion").hide();
        $("#div_loading").show();
        $("#div_error").hide();
      },
      success: function (data) {
        $("#div_informacion").show();
        $("#div_delete").html(data)
        $("#div_loading").hide();
        $("#div_error").hide();
        $("#div_delete").dialog("open");
      },
      error: function () {
        $("#div_loading").hide();
        $("#div_error").show();
        $("#div_delete").dialog("open");
      }
    });
    return false;
  });


});
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

