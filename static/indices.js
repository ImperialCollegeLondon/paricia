$(document).ready(function () {
    $("#div_informacion").hide();
    //datepicker con intervalo registringido
    var dateFormat = "dd/mm/yy";
    $("#id_inicio").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy"
    });
    $("#id_inicio").on("change", function () {
        $("#id_fin").datepicker("option", "minDate", getDate(this));
    });
    $("#id_fin").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy"
    });
    $("#id_fin").on("change", function () {
        $("#id_inicio").datepicker("option", "maxDate", getDate(this));
    });



    function getDate(element) {
        var date;
        try {
            date = $.datepicker.parseDate(dateFormat, element.value);
        } catch (error) {
            date = null;
        }
        return date;
    }


    /*boton para btener datos validados desde indices/doblemasa*/
    $("#btn_validado").click(function () {
        $(this).attr('disabled', true);
        $.ajax({
            url: $("#SearchForm").attr('action'),
            data: $("#SearchForm").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                //add scroll to datatable

                var cont = data.length
                if (data.length == 0){
                    $("#div_error").show();
                    $("#div_error").removeClass("div-hiden").addClass( "div-show" );
                    $("#div_informacion").hide();
                    $("#div_error").html('No existe información para una de las estaciones');
                }else{
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();
                    var rows = "";
                    var x = [];
                    var y = [];
                    var ydate = []
                    for (var i in data) {
                        //console.log(data[i].fecha);
                        rows += '<tr>';
                        rows += '<td class="col-sm-4">'+data[i].fecha+'</td>';
                        rows += '<td class="col-sm-2">'+data[i].valore1+'</td>';
                        rows += '<td class="col-sm-2">'+data[i].acume1+'</td>';
                        rows += '<td class="col-sm-2">'+data[i].valore2+'</td>';
                        rows += '<td class="col-sm-2">'+data[i].acume2+'</td>';
                        rows += '</tr>';
                        x.push(data[i].acume1);
                        y.push(data[i].acume2);
                        ydate.push(data[i].fecha);
                    }

                    $("#tbody").html(rows);
                    $("#grfico").html(gdblmasa(x,y))
                    gAcum(x,ydate,y)
                }
                //graficar(data)
                $("#btn_validado").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function (xhr, status, error, data) {
                console.log("Soy un error " + error)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });

    function gAcum(xx,ydate,yy){
        var trace1 = {
          x: ydate,
          y: xx,
          mode: 'lines',
          name: 'Estacion 1',
          //text: ['United States', 'Canada'],
          marker: {
            color: 'rgb(204, 0, 244)',
            size: 12,
            line: {
              color: 'red',
              width: 0.9
            }
          },
          type: 'scatter'
        };
        var trace2 = {
          x: ydate,
          y: yy,
          mode: 'lines',
          name: 'Estacion 2',
          //text: ['United States', 'Canada'],
          marker: {
            color: 'rgb(0, 0, 204)',
            size: 12,
            line: {
              color: 'red',
              width: 0.9
            }
          },
          type: 'scatter'
        };
        var data = [trace1,trace2];

        var layout = {
          title: 'Curva lluvia acumulada',
          xaxis: {
            title: '',
            showgrid: true,
            zeroline: true,
            type: 'time',
                        time: {
                            unit: 'day'
                        }
          },
          yaxis: {
            title: 'RR Acumulada (mm)',
            showline: false
          }
        };

        Plotly.newPlot('grfico2', data, layout);
    }

    function gdblmasa(xx,yy){
        var trace1 = {
          x: xx,
          y: yy,
          mode: 'lines',
          name: 'RR acumulada',
          //text: ['United States', 'Canada'],
          marker: {
            color: 'rgb(164, 194, 244)',
            size: 12,
            line: {
              color: 'red',
              width: 1
            }
          },
          type: 'scatter'
        };

        var data = [trace1];

        var layout = {
          title: 'Curva de doble masa',
          xaxis: {
            title: 'Estacion 1',
            showgrid: true,
            zeroline: true
          },
          yaxis: {
            title: 'Estacion 2',
            showline: false
          }
        };

        Plotly.newPlot('grfico', data, layout);
    };

/**********************************************
***********************************************
        *indices de precipitación
    */
    $("#btn_ind_pre").click(function () {
        $(this).attr('disabled', true);
        $.ajax({
            url: $("#IndPrecipForm").attr('action'),
            data: $("#IndPrecipForm").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                //add scroll to datatable

                if(JSON.stringify(data) !='{}'){
                    console.log(data)
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();
                    var rows = "";
                    rows += '<tr>';
                    rows += '<td class="col-sm-4">Precipitación anual.</td>';
                    rows += '<td class="col-sm-2">'+data.rranual+'</td>';
                    rows += '</tr> <tr>'
                    rows += '<td class="col-sm-4">Precipitación mensual.</td>';
                    rows += '<td class="col-sm-2">'+data.rrmes+'</td>';
                    rows += '</tr> <tr>'
                    rows += '<td class="col-sm-4">Precipitación del mes más seco.</td>';
                    rows += '<td class="col-sm-2">'+data.messeco+'</td>';
                    rows += '</tr> <tr>'
                    rows += '<td class="col-sm-4">Intensidad máxima de precipitación acumulado cada hora.</td>';
                    rows += '<td class="col-sm-2">'+data.maxhora+'</td>';
                    rows += '</tr>';
                    $("#tbody").html(rows);

                }else{

                    $("#div_error").removeClass("div-hiden").addClass("div-show");
                    $("#div_informacion").hide();
                    $("#div_error").html('No existe información para la estaciones');
                    $("#div_error").show();
                }
                //graficar(data)
                $("#btn_validado").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function (xhr, status, error, data) {
                console.log("Soy un error " + error)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });
    /**********************************************
***********************************************
        *indices de caudales
    */
    $("#btn_indi_cau").click(function () {
        $(this).attr('disabled', true);
        $.ajax({
            url: $("#IndCaudForm").attr('action'),
            data: $("#IndCaudForm").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                //add scroll to datatable

                if(JSON.stringify(data) !='{}'){
                    console.log(data)
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();
                    var rows = "";
                    rows += '<tr>';
                    rows += '<td class="col-sm-4">Caudal mínimo diario</td>';
                    rows += '<td class="col-sm-2">'+data.cmim+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Q10.</td>';
                    rows += '<td class="col-sm-2">'+data.per10+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Promedio de caudal del mes más seco.</td>';
                    rows += '<td class="col-sm-2">'+data.cmessec+'</td>';
                    rows += '</tr> <tr> <th class="col-sm-4" colspan="3">Caudales altos</th>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Caudal máximo diario.</td>';
                    rows += '<td class="col-sm-2">'+data.cmax+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Q95.</td>';
                    rows += '<td class="col-sm-2">'+data.per95+'</td>';
                    rows += '</tr> <tr> <th class="col-sm-4" colspan="3">Caudales medios</th>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Caudal o volumen promedio diario anual o mensual.</td>';
                    rows += '<td class="col-sm-2">'+data.cavg+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Q50.</td>';
                    rows += '<td class="col-sm-2">'+data.per50+'</td>';
                    rows += '</tr>';
                    $("#tbody").html(rows);

                }else{

                    $("#div_error").removeClass("div-hiden").addClass("div-show");
                    $("#div_informacion").hide();
                    $("#div_error").html('No existe información para la estaciones');
                    $("#div_error").show();
                }
                //graficar(data)
                $("#btn_validado").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function (xhr, status, error, data) {
                console.log("Soy un error " + error)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });

    // intencidad duracion de precipitacion
     $("#btn_bus_inten").click(function(){
        $(this).attr('disabled', true);
        $.ajax({
            url: $("#SearchForm").attr('action'),
            data: $("#SearchForm").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                console.log("Datos capturados desde el view");
                console.log(data);
                console.log(data.h1);
                rows = "";
                rows += '<tr> <td >60 min</td>';
                rows += '<td >'+data.h1+'</td> </tr>';
                rows += '<tr> <td >120 min</td>';
                rows += '<td >'+data.h2+'</td> </tr>';
                rows += '<tr> <td >300 min</td>';
                rows += '<td >'+data.h5+'</td> </tr>';
                rows += '<tr> <td >600 min</td>';
                rows += '<td >'+data.h10+'</td> </tr>';
                rows += '<tr> <td >1200 min</td>';
                rows += '<td >'+data.h20+'</td> </tr>';
                rows += '<tr> <td >1440 min</td>';
                rows += '<td >'+data.h24+'</td> </tr>';
                rows += '<tr> <td >2880 min</td>';
                rows += '<td >'+data.h48+'</td> </tr>';
                $("#tbody").html(rows);
                $("#div_informacion").show();
                $("#btn_bus_inten").removeAttr('disabled');
                $("#div_loading").hide();
                $("#div_error").hide();
                $("#grfico").html(gIntensidad(data))
            },
            error: function (xhr, status, error, data) {
                console.log("Soy un error " + error)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });

    });

    function gIntensidad(data){
        var trace1 = {
          y: [data.h48,data.h24,data.h20,data.h10,data.h5,data.h2,data.h1],
          x: [ 60,120,300,600,1200,1440,2880],
          //y: [data.h1,data.h2,data.h5,data.h10,data.h20,data.h24,data.h48],
          mode: 'lines',
          name: 'RR acumulada',
          //text: ['United States', 'Canada'],
          marker: {
            color: 'rgb(164, 194, 244)',
            size: 12,
            line: {
              color: 'red',
              width: 1
            }
          },
          type: 'scatter'
        };

        var data = [trace1];

        var layout = {
          title: 'Intensidad - Duración',
          xaxis: {
            title: 'Duración (min)',
            showgrid: true,
            zeroline: true
          },
          yaxis: {
            title: 'Intensidad (mm/h)',
            showline: false
          }
        };

        Plotly.newPlot('grfico', data, layout);
    };

    //funcion para la grafica de duracion del caudal btn_bus_durcau
     $("#btn_bus_durcau").click(function(){
        $(this).attr('disabled', true);
        $.ajax({
            url: $("#SelecCaudalForm").attr('action'),
            data: $("#SelecCaudalForm").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                if(JSON.stringify(data)!='{}'){
                    let x = []
                    let y = []
                    var con = data.length - 1;
                    for (var i in data) {
                        //console.log(con);
                        x.push(data[i].frecuencia);
                        y.push(data[con].CauEsp);
                        con = con - 1;
                    }
                    $("#grfico").html(duracaudal(x,y))
                    $("#div_informacion").show();
                }else{
                    $("#div_informacion").hide();
                    $("#div_error").html("No hay datos para Procesar")
                    $("#div_error").removeAttr('div-hiden');
                }
                $("#btn_bus_durcau").removeAttr('disabled');
                $("#div_loading").hide();
                //$("#div_error").hide();
                //
            },
            error: function (xhr, status, error) {
                console.log("Soy un error " + error)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });

    });

    /// grafica duracion de caudal
    function duracaudal(xx,yy){
       var trace1 = {
          x: xx,
          y: yy,
          mode: 'lines',
          name: 'CDC',
          //text: ['United States', 'Canada'],
          line: {
              color: 'blue',
              width: 3
          },
          type: 'scatter'
        };

        var data = [trace1];

        var layout = {
          title: 'Duración de caudal',
          xaxis: {
            title: 'Frecuencia',
            showgrid: true,
            zeroline: true
          },
          yaxis: {
            title: 'Caudal (l/s Km^2)',
            showline: false
          }
        };

        Plotly.newPlot('grfico', data, layout);
    };

});