
$(document).ready(function() {
  $("#btn_graficar").click(function(){
    $(this).attr('disabled',true);
    $.ajax({
      url: '/reportes/consultas/',
      data: $("#form_busqueda").serialize(),
      type:'POST',
      dataType: 'json',
      beforeSend: function () {
        $("#div_informacion").hide();
        $("#div_loading").show();
        $("#div_error").hide();
      },
      success: function (data) {
        $("#div_informacion").show();

         var count = Object.keys(data.data[0].y).length;
         if (count>0) {
            Plotly.newPlot('div_informacion', data.data,data.layout);
         }
         else{
            $("#div_informacion").html('<label>No hay información para los parametros ingresados</label>')
         }
         $("#btn_graficar").removeAttr('disabled');

        $("#div_loading").hide();

        $("#div_error").hide();
      },
      error: function () {
        //$("#div_informacion").hide();
        $("#div_loading").hide();
        $("#div_error").show();
        $("#btn_graficar").removeAttr('disabled');
      }
    });
  });


});
