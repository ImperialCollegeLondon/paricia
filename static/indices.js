/**** seteo inicial de elemntos*/


//$("#btn_ind_pre").attr('', true);


/*************************************************/
/********************************************/
/* select item */
function cambio(){
    var estacion1 = document.getElementById("id_estacion1").value;
    var estacion2 = document.getElementById("id_estacion2").value;
    console.log("valor => "+estacion2.length +" <="+ estacion1+" : "+estacion2)
    if(estacion1.length > 0  && estacion2.length >0){
        $("#btn_validado").attr('disabled', false);
    }
}
$(document).ready(function () {

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
        console.log("Aqui cambia la fecha se debe activar el botn buscar")
        $("#btn_ind_pre").attr('disabled', false);
        $("#btn_indi_cau").attr('disabled', false);
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
        $("#div_informacion").show();

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
                    for (var i = 0; i < cont - 1; i++ ) {
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
                    console.log("---------------------");
                    console.log(data[cont-1].e1cod);
                    $('#est1lb').html(data[cont-1].e1cod);
                    $('#est2lb').html(data[cont-1].e2cod);
                    fec = '<tr><td class="col-sm-3 col-md-3 col-md-3">'+data[cont-1].f1max +'</td>'
                    fec += '<td class="col-sm-3 col-md-3 col-md-3">'+data[cont-1].f1mim +'</td>'
                    fec += '<td class="col-sm-3 col-md-3 col-md-3">'+data[cont-1].f2max +'</td>'
                    fec += '<td class="col-sm-3 col-md-3 col-md-3">'+data[cont-1].f1mim +'</td></tr>'
                    $('#tbodyper').html(fec)

                    $("#tbody").html(rows);
                    $("#grfico").html(gdblmasa(x,y,data[cont-1].e1cod,data[cont-1].e2cod))
                    gAcum(x,ydate,y,data[cont-1].e1cod,data[cont-1].e2cod)
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

    function gAcum(xx,ydate,yy,e1,e2){
        var trace1 = {
          x: ydate,
          y: xx,
          mode: 'lines',
          name: e1,
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
          name: e2,
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

    function gdblmasa(xx,yy,e1,e2){
        var trace1 = {
          x: xx,
          y: yy,
          mode: 'lines',
          name: 'RR acumulada',
          //text: ['United States', 'Canada'],
          line: {
              color: 'rgb(55, 128, 191)',
              width: 3

          },
          type: 'scatter'
        };

        var data = [trace1];

        var layout = {
          title: 'Curva de doble masa',
          xaxis: {
            title: e1,
            showgrid: true,
            zeroline: true
          },
          yaxis: {
            title: e2,
            showline: false
          }
        };

        Plotly.newPlot('grfico', data, layout);
    };

/**********************************************
***********************************************
        *indices de precipitación btn_ind_pre
    */

    /*dado un valor de estacionalidad retorna la descriptiocn en texto*/
    function toText( valor ){
        console.log(typeof(valor));
        valor = parseFloat(valor)
        console.log(typeof(valor));
        console.log(valor);
        mensaje = "vacio";
        if (valor < 0.10){
            mensaje = "Muy homogéneo";
        }
        if ( valor >= 0.10 && valor < 0.21){
            mensaje = "Homogéneo pero con una temporada más húmeda";
        }
        if ( valor >= 0.21 && valor < 0.32){
            mensaje = "Algo estacional con una temporada seca corta";
        }
        if ( valor >= 0.32 && valor < 0.43){
            mensaje = "Estacional";
        }
        if ( valor >= 0.43 && valor < 0.54){
            mensaje = "Marcadamente estacional con una temporada seca larga";
        }
        if ( valor >= 0.54 && valor < 0.65){
            mensaje = "Mayoría de la lluvia en 3 meses o menos";
        }
        if ( valor >= 0.65){
            mensaje = "Extrema, casi toda la lluvia en 1-2 meses";
        }
        console.log(mensaje);
        return mensaje;
    }

    $("#btn_ind_pre").click(function () {
        //$(this).attr('disabled', true);
         console.log("soy la data que pasa del view ...")
            //console.log(data);

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
            $("#div_informacion").attr('hidden', false);
                $("#btn_ind_pre").attr('disabled', false);

                //add scroll to datatable
                console.log("data in  succes function  ::::::::: ",data)
                if(data != null){
                    //console.log(data)
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();

                    var rows = "";
                    rows += '<tr>';
                    rows += '<td class="col-sm-4">Precipitación media anual (mm).</td>';
                    rows += '<td class="col-sm-2">'+data.prom_anual+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Año más seco. (mm).</td>';
                    rows += '<td class="col-sm-2">'+data.secHum.anio_seco+'</td>';
                    rows += '<td class="col-sm-2">'+data.secHum.fechsec+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Año más lluvioso. (mm).</td>';
                    rows += '<td class="col-sm-2">'+data.secHum.anio_humedo+'</td>';
                    rows += '<td class="col-sm-2">'+data.secHum.fechhum+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Intensidad máxima de precipitación acumulado cada hora. (mm).</td>';
                    rows += '<td class="col-sm-2">'+data.max24.valor_max.__Decimal__+'</td>';
                    rows += '<td class="col-sm-2">'+data.max24.fecha+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Percentiles 10. (mm).</td>';
                    rows += '<td class="col-sm-2">'+data.percen.q10.__Decimal__+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Percentiles 95. (mm).</td>';
                    rows += '<td class="col-sm-2">'+data.percen.q95.__Decimal__+'</td>';
                    rows += '</tr>';
                    $("#tbody").html(rows);

                    /*completa la tabla de mensual interanual*/
                    //primero llena los anuales para tener la referencia
                    var rows = "";
                    let datoa = data.anios.length;
                    for (var an = 0; an < datoa; an++){
                        fan = data.anios[an].fields.fecha.split('-');
                        fan = parseInt(fan[0]);
                        rows+='<tr>'
                        rows += '<td class="col-sm-1" style="width: 7%">'+fan+'</td>';
                        for (var mes  = 0 ; mes < 12 ; mes++){
                            rows += '<td class="col-sm-2">S/N</td>';
                        }
                        rows += '<td class="col-sm-1" style="width: 7%">'+data.anios[an].fields.valor+'</td>';
                        rows+='</tr>'
                    }
                    //                    console.log(rows);
                    $("#tbodymen").html(rows);
                    ani = parseInt(data.anios[0].fields.fecha.split('-')[0]);
                    fila = 0
                    for (var me = 0; me < data.mes.length; me++){
                        fem = data.mes[me].fields.fecha.split('-');
                        mm = parseInt(fem[1]);
                        ma = parseInt(fem[0]);
                        valor = data.mes[me].fields.valor;
                        if (ani == ma){
                            console.log("ai "+ ani +" alei "+ ma+" Fila "+fila+" mes "+mm+" __::"+$("#tbodymen").find("tr").eq(fila).find("td").eq(0).text());
                            $("#tbodymen").find("tr").eq(fila).find("td").eq(mm).text(valor);
                        }else{
                            ani=ma;
                            fila ++;
                            console.log("ai "+ ani +" alei "+ ma+" Fila "+fila+" mes "+mm+" __::"+$("#tbodymen").find("tr").eq(fila).find("td").eq(0).text());
                            $("#tbodymen").find("tr").eq(fila).find("td").eq(mm).text(valor);
                        }

                    }

                    var rows = "";
                    for (var an = 0; an < data.anios.length; an++){
                        fan = data.anios[an].fields.fecha.split('-');
                        fan = parseInt(fan[0]);
                        esta = data.anios[an].fields.estacionalidad;
                        //console.log("Estacionalidad valor :=> "+esta);
                        rows+='<tr>'
                        rows += '<td class="col-sm-1" style="width: 10%">'+fan+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.mes_seco+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.mes_seco_valor+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.mes_lluvioso+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.mes_lluvioso_valor+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.dias_con_lluvia+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.dias_sin_lluvia+'</td>';
                        rows += '<td class="col-sm-1" style="width: 10%">'+data.anios[an].fields.estacionalidad+'</td>';
                        rows += '<td class="col-sm-1" style="width: 20%">'+toText(data.anios[an].fields.estacionalidad)+'</td>';
                        rows+='</tr>'
                    }
                    $("#tbodyanu").html(rows);

                }else{

                    $("#div_error").removeClass("div-hiden").addClass("div-show");
                    $("#div_informacion").hide();
                    $("#div_error").html('No existe información para la estación');
                    $("#div_error").show();
                }
                //graficar(data)
                $("#btn_validado").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function (xhr, status, error, data) {
                console.log("xhr :");
                console.log(xhr);
                console.log("status :")
                console.log(status);
                console.log("data :")
                console.log(data);
                console.log("Soy un error " + error)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
        $(this).attr('disabled', false);
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
                $("#btn_indi_cau").attr('disabled', false);

                if(data != null){
                    console.log(data)
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();
                    $("#tableacum").attr('hidden',false);
                    var rows = "";
                    rows += '<tr>';
                    rows += '<td class="col-sm-4">Caudal mínimo diario. (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.cmim+'</td>';
                    rows += '<td class="col-sm-2">'+data.fdmin+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Q 95.  (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.per10+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Promedio de caudal del mes más seco. (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.cmessec+'</td><td class="col-sm-2">'+data.fecmessec+'</td>'; //fecmessec
                    rows += '</tr> <tr> <th class="col-sm-4" colspan="3">Caudales altos</th>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Caudal máximo diario. (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.cmax+'</td>';
                    rows += '<td class="col-sm-2">'+data.fdmax+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Q 10. (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.per95+'</td>';
                    rows += '</tr> <tr> <th class="col-sm-4" colspan="3">Caudales medios</th>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Caudal o volumen promedio diario anual o mensual. (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.cavg+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4">Q50. (l/s).</td>';
                    rows += '<td class="col-sm-2">'+data.per50+'</td>';
                    rows += '</tr>';
                    $("#tbody").html(rows);
                    /////// cálculos con caudales especificos
                    ///
                    ///muestra las tablas /
                    if (data.inf === "vacio"){
                        $("#tableesp").attr('hidden',true);
                         $("#esp_title").html("");
                        $("#esp_inf").html("");
                    }else{
                        $("#tableesp").attr('hidden',false);
                        $("#esp_title").html("<h3>Cálculos con caudales específicos </h3>");
                        $("#esp_inf").html("<h4>Area de aporte = "+data.inf+" Km<sup>2</sup></h4>");
                        var rows = "";
                        rows += '<tr>';
                        rows += '<td class="col-sm-4">Caudal mínimo diario. (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.cmim_es+'</td>';
                        rows += '<td class="col-sm-2">'+data.fdmin_es+'</td>';
                        rows += '</tr> <tr>';
                        rows += '<td class="col-sm-4">Q 95.  (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.per10_es+'</td>';
                        rows += '</tr> <tr>';
                        rows += '<td class="col-sm-4">Promedio de caudal del mes más seco. (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.cmessec_es+'</td><td class="col-sm-2">'+data.fecmessec_es+'</td>'; //fecmessec
                        rows += '</tr> <tr> <th class="col-sm-4" colspan="3">Caudales altos</th>';
                        rows += '</tr> <tr>';
                        rows += '<td class="col-sm-4">Caudal máximo diario. (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.cmax_es+'</td>';
                        rows += '<td class="col-sm-2">'+data.fdmax_es+'</td>';
                        rows += '</tr> <tr>';
                        rows += '<td class="col-sm-4">Q 10. (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.per95_es+'</td>';
                        rows += '</tr> <tr> <th class="col-sm-4" colspan="3">Caudales medios</th>';
                        rows += '</tr> <tr>';
                        rows += '<td class="col-sm-4">Caudal o volumen promedio diario anual o mensual. (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.cavg_es+'</td>';
                        rows += '</tr> <tr>';
                        rows += '<td class="col-sm-4">Q50. (l/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2">'+data.per50_es+'</td>';
                        rows += '</tr>';
                        $("#tbodyesp").html(rows);
                    }

                }else{

                    $("#div_error").removeClass("div-hiden").addClass("div-show");
                    $("#div_informacion").hide();
                    $("#div_error").html('No existe información para la estaciones');
                    $("#div_error").show();
                }
                //graficar(data)


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
                rows += '<td >'+data.h48+' (mm/h).</td> </tr>';
                rows += '<tr> <td >120 min</td>';
                rows += '<td >'+data.h24+' (mm/h).</td> </tr>';
                rows += '<tr> <td >300 min</td>';
                rows += '<td >'+data.h20+' (mm/h).</td> </tr>';
                rows += '<tr> <td >600 min</td>';
                rows += '<td >'+data.h10+' (mm/h).</td> </tr>';
                rows += '<tr> <td >1200 min</td>';
                rows += '<td >'+data.h5+' (mm/h).</td> </tr>';
                rows += '<tr> <td >1440 min</td>';
                rows += '<td >'+data.h2+' (mm/h).</td> </tr>';
                rows += '<tr> <td >2880 min</td>';
                rows += '<td >'+data.h1+' (mm/h).</td> </tr>';
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
          line: {
              color: 'blue',
              width: 3
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
            console.log("ya en el javascript")
            console.log(data," Longitud ");
            if(data.length > 0){
                rows = "";
                var traces = [];
                console.log("valor del data"+ data.length)
                for (var aix = 0; aix < data.length; aix ++){
                    let dx = [];
                    let dy = [];
                    var con = data[aix].frecuencias.length - 1;
                    rows+='<tr> <td colspan="2">'+data[aix].anio+'</td> </tr>';
                    for (var vin  = 0 ;vin < data[aix].frecuencias.length; vin++  ){
                        //console.log("valor del data.frecuencias"+ data[aix].frecuencias[vin])
                        dx.push(data[aix].frecuencias[vin]);
                        dy.push(data[aix].valores[con]);
                        rows+='<tr> <td >'+data[aix].frecuencias[vin]+'</td>';
                        rows += '<td >'+data[aix].valores[con]+'</td> </tr>';
                        con = con - 1;
                    }
                    let tra={
                        x: dx,
                        y: dy,
                        mode: 'lines',
                        name: ''+data[aix].anio,
                        line: {
                        //color: 'blue',
                            width: 3
                        },
                        type: 'scatter'
                    };
                    traces.push(tra);
                }
                    $("#tbody").html(rows);
                    $("#grfico").html(duracaudal(traces));
                    $("#div_informacion").show();
            }else{
                    $("#div_informacion").hide();
                    $("#div_error").html("No hay datos para Procesar")
                    $("#div_error").show();
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
        $(this).attr('disabled', false);

    });

    /// grafica duracion de caudal
    function duracaudal(data){

        var layout = {
          title: 'Duración de caudal',
          showlegend:true,
          xaxis: {
            title: 'Frecuencia',
            showgrid: true,
            zeroline: true
            //type:'log'
          },
          yaxis: {
            title: 'Caudal (l/s)',
            showline: false,
            type:'log'
          }
        };
        //fig.update_layout(xaxis_type="log", yaxis_type="log")
        Plotly.newPlot('grfico', data, layout);
    };

});