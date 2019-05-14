
$(document).ready(function() {
    $("#btn_graficar").click(function(){
        $(this).attr('disabled',true);
        $.ajax({
            url: $("#form_consulta").attr('action'),
            data: $("#form_consulta").serialize(),
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


    $("#btn_consultar").click(function(){
        $(this).attr('disabled',true);
        $.ajax({
            url: $("#form_busqueda").attr('action'),
            data: $("#form_busqueda").serialize(),
            type:'POST',
            dataType: 'json',
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
                $("#div_mensaje").hide();
            },
            success: function (data) {

                if (Object.keys(data)=="mensaje"){
                    $("#div_mensaje").html(data.mensaje);
                    $("#div_mensaje").show();
                }
                else{
                    $("#div_informacion").show();
                    var count = Object.keys(data.data[0].y).length;
                    if (count>0) {
                        Plotly.newPlot('div_informacion', data.data,data.layout);
                    }
                    else{
                        //$("#div_informacion").html('<label>No hay información para los parametros ingresados</label>')
                        $("#div_mensaje").html('<label>No hay información para los parametros ingresados</label>');
                        $("#div_mensaje").show();
                    }

                }

                $("#btn_consultar").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function () {
                //$("#div_informacion").hide();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });

    //datepicker con intervalo registringido
    var dateFormat = "dd/mm/yy";
    $( "#id_inicio" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"dd/mm/yy"
    });
    $( "#id_inicio" ).on( "change", function() {
        $( "#id_fin" ).datepicker( "option", "minDate", getDate( this ) );
    });
    $( "#id_fin" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"dd/mm/yy"
    });
    $( "#id_fin" ).on( "change", function() {
        $( "#id_inicio" ).datepicker( "option", "maxDate", getDate( this ) );
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

    function graficar(data){
        var data02= [{
            x: new Date(),
            y: 1
        }, {
            t: new Date(),
            y: 10
        }]
        var data03= [{
            x: 10,
            y: 20
        }, {
            x: 15,
            y: 10
        }]
        var ctx = document.getElementById('myChart');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                //labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [{
                    label: 'Precipitacion',
                    data: data,
                }]
            },
            //data:data03,
            options: {
                scales: {

                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day'
                        }
                    }]
                }
            }
        });
    }


});
