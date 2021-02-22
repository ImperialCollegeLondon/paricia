/**** seteo inicial de elemntos*/


//$("#btn_ind_pre").attr('', true);


/*************************************************/
/********************************************/
/* select item */
function cambio(){
    var estacion1 = document.getElementById("id_estacion1").value;
    var estacion2 = document.getElementById("id_estacion2").value;
    //console.log("valor => "+estacion2.length +" <="+ estacion1+" : "+estacion2)
    if(estacion1.length > 0  && estacion2.length >0){
        $("#btn_validado").attr('disabled', false);
    }
}
$(document).ready(function () {
    $("select").addClass("use-placeholder");
    window.mostrar_label_dentro_de_select();
    //datepicker con intervalo registringido
    var dateFormat = "yy-mm-dd";
    $("#id_inicio").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd"
    });
    $("#id_inicio").on("change", function () {
        $("#id_fin").datepicker("option", "minDate", getDate(this));
        $("#expo_cd").attr('disabled', true);
    });
    $("#id_fin").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd"
    });
    $("#id_fin").on("change", function () {
        $("#id_inicio").datepicker("option", "maxDate", getDate(this));
        //console.log("Aqui cambia la fecha se debe activar el botn buscar")
        $("#btn_ind_pre").attr('disabled', false);
        $("#btn_indi_cau").attr('disabled', false);
        $("#expo_cd").attr('disabled', true);
    });
    $("#id_estacion").on("change",function(){
        $("#expo_cd").attr('disabled', true);
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
                        //console.log(data[i]foo fighters best of you.fecha);
                        rows += '<tr>';
                        rows += '<td class="col-sm-4" style="width: 20%">'+data[i].fecha+'</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data[i].valore1+'</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data[i].acume1+'</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data[i].valore2+'</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data[i].acume2+'</td>';
                        rows += '</tr>';
                        x.push(data[i].acume1);
                        y.push(data[i].acume2);
                        ydate.push(data[i].fecha);
                    }
                    //console.log("---------------------");
                    //console.log(data[cont-1].e1cod);
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
        *indices de precipitación
    */

    /*dado un valor de estacionalidad retorna la descriptiocn en texto*/
    function toText( valor ){
        valor = parseFloat(valor)
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
        //console.log(mensaje);
        return mensaje;
    }

    $("#btn_ind_pre").click(function () {
        //$(this).attr('disabled', true);
         //console.log("indices precipitación ...")
         //console.log(".....")
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
                    console.log(screen.width);
                //add scroll to datatable
                //console.log("data in  succes function  ::::::::: ",data)
                if(data != null){
                    //console.log(data)
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();

                    var rows = "";
                    rows += '<tr>';
                    if(screen.width <= 720 ){
                        rows += '<td class="col-lg-4 col-md-4 col-sm-2 col-xs-2" style="width: 50%" >Precipitación media  <br> anual (mm).</td>';
                    }
                    else{
                        rows += '<td class="col-lg-4 col-md-4 col-sm-2 col-xs-2" style="width: 50%">Precipitación media anual (mm).</td>';
                    }
                    
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.prom_anual+'</td>';
                    rows += '<td class="col-sm-4"style="display:none;"></td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-lg-4 col-md-4 col-sm-4 col-xs-2" style="width: 50%" >Año más seco (mm).</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.secHum.anio_seco+'</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.secHum.fechsec+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-lg-4 col-md-4 col-sm-4 col-xs-2" style="width: 50%">Año más lluvioso (mm).</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.secHum.anio_humedo+'</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.secHum.fechhum+'</td>';
                    rows += '</tr> <tr >';
                    if(screen.width <= 720 ){
                        rows += '<td class="col-lg-4 col-md-4 col-sm-2 col-xs-2" style="width: 50%" >Intensidad máxima de <br> precipitación  acumulado <br>cada hora (mm).</td>';
                    }
                    else{
                        rows += '<td class="col-lg-4 col-md-4 col-sm-2 col-xs-2" style="width: 50%" >Intensidad máxima de precipitación  acumulado cada hora (mm).</td>';
                    }
                    
                    rows += '<td class="col-sm-4" style="width: 20%">'+Math.round(data.max24.valor_max.__Decimal__ * 100) / 100+'</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.max24.fecha+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-lg-4 col-md-4 col-sm-2 col-xs-2" style="width: 50%" >Percentiles 10 (mm).</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.percen.q10.__Decimal__+'</td>';
                    rows += '<td class="col-sm-4" style="display:none;"></td>';
                    rows += '</tr> <tr>';
                    rows += '<td class="col-lg-4 col-md-4 col-sm-2 col-xs-2" style="width: 50%" >Percentiles 95 (mm).</td>';
                    rows += '<td class="col-sm-4" style="width: 20%">'+data.percen.q95.__Decimal__+'</td>';
                    rows += '<td class="col-sm-4"style="display:none;" ></td>';
                    rows += '</tr>';
                    $("#tbody").html(rows);
                    
                    tableac = $('#tableacum').DataTable({
                        language: window.DATATABLES_LANGUAGE,
                        scrollX: true,
                        ordering: false,
                        paging: false,
                        searching: false,
                        info: false,
                        fixedColumns:  { leftColumns: 1,},
                        destroy: true,
                    });
                    tableac.columns.adjust().draw();
                    
                    //$("#tbody").html(rows);
                    
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
                            rows += '<td class="col-sm-2" style="width: 7%">S/N</td>';
                        }

                        let valorm = parseFloat(data.anios[an].fields.valor)
                        rows += '<td class="col-sm-1" style="width: 7%">'+Math.round(valorm * 10) / 10+'</td>';
                        rows+='</tr>'
                    }
                    //                    console.log(rows);
                    $("#tbodymen").html(rows);
                    tablemen = $('#tbmensual').DataTable({
                        language: window.DATATABLES_LANGUAGE,
                        scrollX: true,
                        ordering: false,
                        paging: false,
                        searching: false,
                        info: false,
                        fixedColumns:  { leftColumns: 1,},
                        destroy: true,
                    });
                    tablemen.columns.adjust().draw();
                    ani = parseInt(data.anios[0].fields.fecha.split('-')[0]);
                    fila = 0
                    for (var me = 0; me < data.mes.length; me++){
                        fem = data.mes[me].fields.fecha.split('-');
                        mm = parseInt(fem[1]);
                        ma = parseInt(fem[0]);
                        valor = Math.round(data.mes[me].fields.valor*10)/10;
                        if (ani == ma){
                            //console.log("ai "+ ani +" alei "+ ma+" Fila "+fila+" mes "+mm+" __::"+$("#tbodymen").find("tr").eq(fila).find("td").eq(0).text());
                            $("#tbodymen").find("tr").eq(fila).find("td").eq(mm).text(valor);
                        }else{
                            ani=ma;
                            fila ++;
                            //console.log("ai "+ ani +" alei "+ ma+" Fila "+fila+" mes "+mm+" __::"+$("#tbodymen").find("tr").eq(fila).find("td").eq(0).text());
                            $("#tbodymen").find("tr").eq(fila).find("td").eq(mm).text(valor);
                        }

                    }

                    var rows = "";
                    var meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
                    for (var an = 0; an < data.anios.length; an++){
                        fan = data.anios[an].fields.fecha.split('-');
                        fan = parseInt(fan[0]);
                        esta = data.anios[an].fields.estacionalidad;
                        //console.log("Estacionalidad valor :=> "+esta);
                        console.log(data.anios[an].fields.mes_seco_valor);
                        let msec = "S/D";
                        let mhum = "S/D";
                        let vms = "";
                        let vmh = "";
                        let dcll = "";
                        let dsll = "";
                        let inst = "";
                        let instCla = " ";
                        if(data.anios[an].fields.mes_seco === null){
                            msec ="S/N"
                            vms = "S/N";
                            dcll = "S/N";
                        }else{
                            console.log("mes : "+data.anios[an].fields.mes_seco)
                            msec = meses[data.anios[an].fields.mes_seco-1]
                            vms = Math.round(data.anios[an].fields.mes_seco_valor * 10) / 10;
                            dcll = data.anios[an].fields.dias_con_lluvia
                        }
                        if(data.anios[an].fields.mes_lluvioso === null){
                            mhum ="S/N"
                            vmh = "S/N";
                            dsll = "S/N";
                        }else{
                            console.log("mes : "+data.anios[an].fields.mes_lluvioso)
                            mhum = meses[data.anios[an].fields.mes_lluvioso-1]
                            vmh = Math.round(data.anios[an].fields.mes_lluvioso_valor * 10) / 10
                            dsll = data.anios[an].fields.dias_sin_lluvia
                        }
                        if(data.anios[an].fields.estacionalidad === null){
                            inst = "";
                            instCla = "";
                        }else{
                            inst = data.anios[an].fields.estacionalidad;
                            instCla = toText(data.anios[an].fields.estacionalidad);
                        }
                        rows+='<tr>'
                        rows += '<td >'+fan+'</td>';
                        rows += '<td >'+msec+'</td>';
                        rows += '<td >'+vms+'</td>';
                        rows += '<td >'+mhum+'</td>';
                        rows += '<td >'+vmh+'</td>';
                        rows += '<td >'+dcll+'</td>';
                        rows += '<td >'+dsll+'</td>';
                        rows += '<td >'+inst+'        '+instCla+'</td>';
                        rows+='</tr>'
                    }
                    $("#tbodyanu").html(rows);
                    tbanual = $('#tbanual').DataTable({
                        language: window.DATATABLES_LANGUAGE,
                        scrollX: true,
                        ordering: false,
                        paging: false,
                        searching: false,
                        info: false,
                        fixedColumns:  { leftColumns: 1,},
                        destroy: true,
                    });
                    tbanual.columns.adjust().draw();
                    
                    //table2.destroy();
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
            },
            complete: function(data) {
                
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
                //console.log("funcion succes")
                if(data != null){
                    //console.log(data)
                    $("#div_error").removeClass("div-show").addClass( "div-hiden" );
                    $("#div_informacion").show();
                    $("#tableacum").attr('hidden',false);
                    var rows = "";
                    rows += '<tr>';
                    if(screen.width <= 720 ){
                        rows += '<td class="col-sm-4" style="width: 50%">Caudal mínimo<br/>diario (m3/s).';
                    }
                    else{
                        rows += '<td class="col-sm-4" style="width: 50%">Caudal mínimo diario (m3/s).';
                    }
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.cmim +'</td>';
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.fdmin+'</td>'; 
                    rows += '</tr> <tr>';
                    rows += '<td class="col-sm-4" style="width: 50%">Q 95  (m3/s).</td>';
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.per10+'</td>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '</tr> <tr>';
                    if(screen.width <= 720 ){
                        rows += '<td col-sm-4" style="width: 60%" >Promedio de caudal<br/>del mes más seco <br>(m3/s).</td>';
                    }
                    else{
                        rows += '<td col-sm-4" style="width: 60%" >Promedio de caudal del mes más seco (m3/s).</td>';
                    }
                    rows += '<td class="col-sm-2" style="width: 20%" >'+data.cmessec+'</td><td class="col-sm-2" style="width: 20%">'+ data.fecmessec+'</td>'; //fecmessec
                    rows += '</tr> <tr> <th col-sm-4" style="width: 50%">Caudales altos</th>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '</tr> <tr>';
                    if(screen.width <= 720 ){
                        rows += '<td col-sm-4" style="width: 60%" >Caudal máximo diario<br/>(m3/s).</td>';
                    }
                    else{
                        rows += '<td col-sm-4" style="width: 60%" >Caudal máximo diario (m3/s).</td>';
                    }
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.cmax+'</td>';
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.fdmax+'</td>';
                    rows += '</tr> <tr>';
                    rows += '<td col-sm-4" style="width: 60%" >Q 10 (m3/s).</td>';
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.per95+'</td>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '</tr> <tr> <th col-sm-4" style="width: 50%">Caudales medios</th>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '</tr> <tr>';
                    if(screen.width <= 720 ){
                        rows += '<td class="col-sm-4" style="width: 20%" >Caudal <br>promedio diario anual<br>o mensual (m3/s).</td>';

                    }
                    else{
                        rows += '<td col-sm-4" style="width: 60%" >Caudal promedio diario (m3/s).</td>';

                    }
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.cavg +'</td>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '</tr> <tr>';
                    rows += '<td col-sm-4" style="width: 50%">Q50 (m3/s).</td>';
                    rows += '<td class="col-sm-2" style="width: 20%">'+data.per50 +'</td>';
                    rows += '<td class="col-sm-2"  style="display:none;"></td>';
                    rows += '</tr>';
                    $("#tbody").html(rows);
                    /////// cálculos con caudales especificos
                    table = $('#tableacum').DataTable({
                        language: window.DATATABLES_LANGUAGE,
                        scrollX: true,
                        ordering: false,
                        paging: false,
                        searching: false,
                        info: false,
                        fixedColumns:  { leftColumns: 1,},
                        destroy: true,
                    });
                    table.columns.adjust().draw();
                    

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
                        if(screen.width <= 720 ){
                            rows += '<td col-sm-4" style="width: 60%" >Caudal mínimo diario<br/> (m3/s/km<sup>2</sup>)</td>';    
                        }
                        else{
                            rows += '<td col-sm-4" style="width: 60%" >Caudal mínimo diario<br/> (m3/s/km<sup>2</sup>)</td>';
    
                        }
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.cmim_es+'</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.fdmin_es+'</td>';
                        rows += '</tr> <tr>';
                        rows += '<td col-sm-4" style="width: 60%" >Q 95.  (m3/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.per10_es +'</td>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '</tr> <tr>';
                        if(screen.width <= 720 ){
                            rows += '<td col-sm-4" style="width: 60%" >Promedio de caudal del <br/>mes más seco (m3/s/km<sup>2</sup>).</td>';    
                        }
                        else{
                            rows += '<td col-sm-4" style="width: 60%" >Promedio de caudal del mes más seco (m3/s/km<sup>2</sup>).</td>';
    
                        }
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.cmessec_es+'</td><td class="col-sm-2" style="width: 20%">'+data.fecmessec_es+'</td>'; //fecmessec
                        rows += '</tr> <tr> <th col-sm-4" style="width: 50%" >Caudales altos</th>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '</tr> <tr>';
                        if(screen.width <= 720 ){
                            rows += '<td col-sm-4" style="width: 60%" >Caudal máximo diario <br/>(m3/s/km<sup>2</sup>).</td>';
                        }
                        else{
                            rows += '<td col-sm-4" style="width: 60%" >Caudal máximo diario(m3/s/km<sup>2</sup>).</td>';
    
                        }
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.cmax_es +'</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.fdmax_es+'</td>';
                        rows += '</tr> <tr>';
                        rows += '<td col-sm-4" style="width: 60%" >Q 10 (m3/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.per95_es+'</td>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '</tr> <tr> <th col-sm-4" style="width: 50%" >Caudales medios</th>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '</tr> <tr>';
                        if(screen.width <= 720 ){
                            rows += '<td col-sm-4" style="width: 60%" >Caudal promedio<br>diario<br> (m3/s/km<sup>2</sup>).</td>';    
                        }
                        else{
                            rows += '<td col-sm-4" style="width: 60%" >Caudal promedio diario. (m3/s/km<sup>2</sup>).</td>';
    
                        }
                        
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.cavg_es +'</td>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '</tr> <tr>';
                        rows += '<td col-sm-4" style="width: 60%" >Q50 (m3/s/km<sup>2</sup>).</td>';
                        rows += '<td class="col-sm-2" style="width: 20%">'+data.per50_es +'</td>';
                        rows += '<td class="col-sm-2"  style="display:none;"></td>';
                        rows += '</tr>';
                        $("#tbodyesp").html(rows);
                        table1 = $('#tableesp').DataTable({
                            language: window.DATATABLES_LANGUAGE,
                            scrollX: true,
                            ordering: false,
                            paging: false,
                            searching: false,
                            info: false,
                            fixedColumns:  { leftColumns: 1,},
                            destroy: true,
                        });
                        table1.columns.adjust().draw();
                        
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
                console.log("xhr "+xhr)
                console.log("status "+status)
                console.log("data "+data)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });

    // intencidad duracion de precipitacion
    //
     $("#btn_bus_inten").click(function(){
        var fecha = $(id_anio).val();
        //console.log(fecha);
        $(this).attr('disabled', true);
        $("#div_nota").attr('hidden', false);
        $.ajax({
            url: $("#SearchForm").attr('action'),
            data: $("#SearchForm").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").attr('hidden', true);
                $("#div_loading").show();
                $("#div_error").attr('hidden', true);
            },
            success: function (data) {
                //console.log("Datos capturados desde el view");
                var $table = $('#tableacum');
                $table.bootstrapTable('destroy');
                //console.log(data);
                if(data.fecha.length===0){
                    $("#div_error").html(data.mensaje);
                    $("#div_error").attr('hidden', false);
                }else{
                    $("#div_informacion").attr('hidden', false);
                    datatable = []
                    for (inx in data.inte){
                        dic = {}
                        dic["itv"]=data.iterval[inx]
                        dic["int"]=data.inte[inx]
                        dic["rr"]=data.maximo[inx]
                        dic["f"]=data.fecha[inx]
                        datatable.push(dic)
                    }
                    $table.bootstrapTable({data: datatable})
                    let dx = data.iterval
                    //console.log('X:',x);
                    let dy = data.inte
                    //console.log('Y:',y);
                    var trace={y:dy,x:dx,mode:'lines',name:data.estacion_id,line:{color:'blue',width:3},type:'scatter' }
                    var data = [trace]
                    $("#grfico").html(gIntensidad("grfico",data))
                }
                $("#btn_bus_inten").removeAttr('disabled');
                $("#div_loading").hide();
                //$("#div_error").attr('hidden', true);
                $("#div_nota").attr('hidden', true);
            },
            error: function (xhr, status, error, data) {
                console.log("Soy un error " + error)
                $("#div_informacion").attr('hidden', true);
                $("#div_loading").hide();
                $("#div_error").attr('hidden', true);
                $("#btn_consultar").removeAttr('disabled');
                $("#div_nota").attr('hidden', true);
            }
        });

    });

// intencidad multiestacion cau_multi
     $("#cau_multi").click(function(){
        $(this).attr('disabled', true);
        $("#div_nota").attr('hidden', false);
        $.ajax({
            url: $("#form_curva_descarga").attr('action'),
            data: $("#form_curva_descarga").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").attr('hidden', true);
                $("#div_loading").show();
                $("#div_error").attr('hidden', true);
            },
            success: function (data) {
                //console.log(data);
                if (data.hasOwnProperty('error')){
                    console.log("data Error "+data.error)
                    $("#msjError").html(data.error)
                    $("#div_error").attr('hidden', false);
                    $("#div_loading").hide();
                    $("#div_informacion").hide();
                }else{
                    var mostrar = false
                    var datamulti = []
                    //console.log("data len "+data.length)
                    for (var it = 0; it < data.length; it ++){
                        //console.log("it value : "+it+"   Fecha desing   "+data[it].fecha.length)
                        if(data[it].fecha.length > 0){
                            mostrar = true
                            let dx = data[it].iterval
                            let dy = data[it].inte
                            var trace={y:dy,x:dx,mode:'lines',name:data[it].estacion_id,line:{width:3},type:'scatter' }
                            //console.log("trace " + trace)
                            datamulti.push(trace)
                        }
                    }
                    //console.log("datamulti "+datamulti)
                    //console.log("mostrar " + mostrar)
                    if(mostrar){
                        $("#div_informacion").attr('hidden', false);
                        $("#graficoMul").html(gIntensidad("graficoMul",datamulti))
                    }else{
                        $("#msjError").html("No existen datos para las estaciones selecionadas en el año selecionado")
                        $("#div_error").attr('hidden', false);
                    }
                }
                //console.log("antes de activar el boton")
                $("#cau_multi").attr('disabled', false);
                $("#div_loading").hide();
                //$("#div_error").attr('hidden', true);
                $("#div_nota").attr('hidden', true);
            },
            error: function (xhr, status, error, data) {
                //console.log("Soy un error " + error)
                $("#div_informacion").attr('hidden', true);
                $("#div_loading").hide();
                $("#div_error").attr('hidden', true);
                $("#btn_consultar").removeAttr('disabled');
                $("#div_nota").attr('hidden', true);
            }
        });

    });


    
    //Cargar fechas por estacion

    $("#id_estacion").change(function () {
        $("#div_error").addClass("div-hiden").removeClass("div-show");
       var estacion = $(this).val();
       var action = $(".form").attr('action');
       if (action == '/indices/intensidad/') {
        var estacion = $(this).val(); 
        $("#btn_bus_inten").prop('disabled', false);
        $("#id_anio").find('option').remove().end()
         $.ajax({
             url: '/indices/listar_anio/'+estacion,
             dataType: 'json',
             success: function (data) {
                 $.each(data, function(index, value) {
                     $("#id_anio").append('<option value="' + value + '">' + value + '</option>');
                     if (value == "No existen datos") {
                        $("#btn_bus_inten").prop('disabled', true);
                    }
                 });
             }
         }); 
       }
       if (action == '/indices/intensidadmulti/') {
        $("#id_anio").find('option').remove().end();
        $("#cau_multi").prop('disabled', false);
        $.ajax({
            url: '/indices/listar_anio_multi/',
            type: 'POST',
            data: $("#form_curva_descarga").serialize(),
            cache: false,
            dataType: 'json',
            success: function (data) {
                $.each(data, function(index, value) {
                    $("#id_anio").append('<option value="' + value + '">' + value + '</option>');
                    if (value == "No existen datos") {
                        $("#cau_multi").prop('disabled', true);
                    }
                });

            }
        }); 
       } 
       if (action == '/indices/caudal/') {
        $("#cau_multi").prop('disabled', false);
        $("#btn_indi_cau").prop('disabled', false);
        $.ajax({
                url: '/indices/listar_fecha_caudal/'+estacion,
                dataType: 'json',
                success: function (data) {
                    //console.log(data);
                    if (data != "No existen datos") {
                        $("#id_inicio").datepicker("option", "minDate",data['fecha__min']);
                        $("#id_inicio").datepicker("option", "maxDate", data['fecha__max']);
                        $("#id_fin").datepicker("option", "minDate", getDate(this));
                        $("#id_fin").datepicker("option", "maxDate", data['fecha__max']);
                    } else {
                        $("#btn_indi_cau").prop('disabled', true);
                        $("#div_error").removeClass("div-hiden").addClass("div-show");
                        $("#div_error").html('No existe información para la estaciones');
                        $("#div_error").show();
                    }
                }
            });
       }    
       if (action == '/indices/precipitacion/') {
        $("#cau_multi").prop('disabled', false);
        $("#btn_indi_cau").prop('disabled', false);
        $.ajax({
                url: '/indices/listar_fecha_precipitacion/'+estacion,
                dataType: 'json',
                success: function (data) {
                    //console.log(data);
                    if (data != "No existen datos") {
                        $("#id_inicio").datepicker("option", "minDate",data['fecha__min']);
                        $("#id_inicio").datepicker("option", "maxDate", data['fecha__max']);
                        $("#id_fin").datepicker("option", "minDate", getDate(this));
                        $("#id_fin").datepicker("option", "maxDate", data['fecha__max']);
                    } else {
                        $("#btn_indi_cau").prop('disabled', true);
                        $("#div_error").removeClass("div-hiden").addClass("div-show");
                        $("#div_error").html('No existe información para la estaciones');
                        $("#div_error").show();
                    }
                }
            });
       }    
    });

    function gIntensidad(divref,data){
        $(divref).html("");
        var width_graph = $(".container").width();
        var layout = {
          title: 'Intensidad - Duración de precipitación',
          showlegend:true,
          width: width_graph,
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
        Plotly.newPlot(divref, data, layout);
    };

    //funcion para la grafica de duracion del caudal btn_bus_durcau
     $("#btn_bus_durcau").click(function(){
        $(this).attr('disabled', true);
        $("#expo_cd").attr('disabled', false);
        $.ajax({
            //url: $("#SelecCaudalForm").attr('action'),
            url: "/indices/duracaudal/",
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
            var $table = $('#table');
            $table.bootstrapTable('destroy');
            var procesar = false
            if ( data !== null ){
                if( data.hasOwnProperty("anios") && data.anios.length > 0){
                    procesar = true;
                }
            }
           // console.log("Debo procesar " +  procesar)
            if(procesar){
                var traces = [];
                var traces1 = [];
                //console.log("valor del data "+ data.mayor)
                //console.log(data);
                //console.log("propiedades "+Object.getOwnPropertyNames(data.anuales).length);
                max = 0 ;
                tht = "<tr>" //años
                thl = "<tr>"// titulos
                for (var idx = 0 ; idx < data.anios.length;idx++){
                    var cau = "cau"+data.anios[idx];
                    var caue = "cauEsp"+data.anios[idx];
                    var fre = "fre"+data.anios[idx];
                    //console.log("agregando "+cau+" : "+caue+" : "+fre)
                    tra={ x: data.anuales[fre], y: data.anuales[cau], mode: 'lines', name: ''+data.anios[idx], line: { width: 3 }, type: 'scatter' };
                    traces.push(tra);
                    tra1={x: data.anuales[fre], y: data.anuales[caue], mode: 'lines', name: ''+data.anios[idx], line: { width: 3 },type: 'scatter' };
                    traces1.push(tra1);
                    /// cabecera de la tabla
                    /*if(data.aporte){
                        tht += "<th colspan ="+3+" >"+data.anios[idx]+"</th>"
                        thl += "<th data-field="+cau+"> Caudal </th>"
                        thl += "<th data-field="+caue+"> Caudal Esp</th>"
                        thl += "<th data-field="+fre+"> Frecuencia</th>"
                    }else{
                        tht += "<th colspan ="+2+" >"+data.anios[idx]+"</th>"
                        thl += "<th data-field="+cau+"> Caudal </th>"
                        thl += "<th data-field="+fre+"> Frecuencia</th>"
                    }*/
                }
                //tht += "</tr>"
                //thl += "</tr>"
                tra ={ x: data.total.fre, y: data.total.cau, mode: 'lines', name: 'Periodo Completo', line: { width: 3 }, type: 'scatter'};
                traces.push(tra);
                tra1={ x: data.total.fre, y: data.total.cauEsp, mode: 'lines', name: 'Periodo Completo', line: { width: 3 }, type: 'scatter' };
                traces1.push(tra1);
                $("#grfico").html(duracaudal('grfico',traces,'Duración de caudal','Frecuencia','Caudal (m3/s)'));
                $("#grficosf").html('</br>');
                if (data.aporte){
                    $("#grficosf").html('</br>');
                    $("#grficosf").html(duracaudal('grficosf',traces1,'Duración de caudal específico','Frecuencia','Caudal (m3/s/km^2)'));//grficosf
                }
                $("#expo_cd").attr('disabled', false);
                //creacion de datos para la tabla
                /*lact = data.anuales[cau].length
                datatable = []
                for(var lo = 0; lo < data.mayor ; lo ++ ){
                    dic = {}
                    for (var idx = 0 ; idx < data.anios.length;idx++){
                        var cau = "cau"+data.anios[idx];
                        var caue = "cauEsp"+data.anios[idx];
                        var fre = "fre"+data.anios[idx];
                        if (data.aporte){ ///comprueba si existe el area de aporte y agrega el caudal especifico alas columnas
                            if(lo >= lact){ // mayor longitud de las series
                                dic[cau] =  null;
                                dic[caue] = null;
                                dic[fre] = null;
                            }else{
                                dic[cau] =  data.anuales[cau][lo]
                                dic[caue] =  data.anuales[caue][lo]
                                dic[fre] =  data.anuales[fre][lo]
                            }
                        }else{
                            if(lo >= lact){ // mayor longitud de las series
                                dic[cau] =  null;
                                dic[fre] = null;
                            }else{
                                dic[cau] =  data.anuales[cau][lo]
                                dic[fre] =  data.anuales[fre][lo]
                            }
                        }
                        datatable.push(dic);
                    }
                }*/
                ///console.log(datatable)
                //$("#table > thead").html(tht+thl);
                //$table.bootstrapTable({data: datatable})
                $("#div_informacion").show();
            }else{
                    $("#div_informacion").hide();
                    $("#div_error").html("No hay datos para Procesar")
                    $("#div_error").show();
            }
            $("#btn_bus_durcau").removeAttr('disabled');
            $("#div_loading").hide();
            },
            error: function (xhr, status, error) {
                console.log("Soy un error " + error+ "xhr "+xhr)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
        $(this).attr('disabled', false);

    });

    /// grafica duracion de caudal
    function duracaudal(id_div,data, mtit,xtit,ytit){
        $(id_div).html("");
        var width_graph = $(".container").width();
        //console.log(width_graph);

        var layout = {
          title: mtit,
          showlegend:true,
          width: width_graph,
          xaxis: {
            title: xtit,
            showgrid: true,
            zeroline: true
            //type:'log'
          },
          yaxis: {
            title: ytit,
            showline: false,
            type:'log'
          }
        };
        //fig.update_layout(xaxis_type="log", yaxis_type="log")
        Plotly.newPlot(id_div, data, layout);
    }

    ////// duracion caudal multiestacion
    //visualizar
    $("#btn_visualizar").click(function(){
    //console.log("click event btn_visualizar")
        //$(this).attr('disabled', true);
        $.ajax({
            url: $("#form_curva_descarga").attr('action'),
            data: $("#form_curva_descarga").serialize(),
            type: 'POST',
            dataType: 'json',
            cache: false,
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                //console.log(data)
                //console.log(data.hasOwnProperty('estaciones'))
                if (data.hasOwnProperty('menjaseErr')){
                    $("#div_error").show();
                    $("#msjError").html(data.menjaseErr)
                    $("#div_loading").hide();
                    $("#div_informacion").hide();
                }
                if(data.hasOwnProperty('estaciones')){
                    $(this).attr('disabled', false);
                    var $table = $('#table');
                    $table.bootstrapTable('destroy');
                    //console.log(data)
                    var traces = [];
                    //console.log('estaciones con datos '+data.estaciones)
                    for (e in data.estaciones){
                        var fre = "fre"+data.codigos[e]
                        var cau = "cauEsp"+data.codigos[e]
                        //console.log(data.estaciones[e])
                        //console.log(data.datos[cau])
                        tra={ x: data.datos[fre], y: data.datos[cau], mode: 'lines', name: ''+data.estaciones[e].estacion, line: { width: 3 }, type: 'scatter' };
                        traces.push(tra);
                    }
                    $("#tbtitle").html("Periodos por estación utilizados para el cálculo")
                    thead="<tr> <th data-field='estacion'>Estacion </th> <th data-field='inicio'>Fecha de inicio</th> <th data-field='fin'>Fecha de fin</th> </tr>"
                    $("#table > thead").html(thead)
                    $table.bootstrapTable({data: data.estaciones})
                    $("#grficosf").html(duracaudal('grficosf',traces,'Duración de caudal específico','Frecuencia','Caudal (m3/s/km^2)'));//grficosf
                    $("#div_error").hide();
                    $("#div_loading").hide();
                    $("#div_informacion").show();
                    $(this).attr('disabled', false);
                }


            },
            error: function (xhr, status, error) {
                console.log("Soy un error " + error+ "xhr "+xhr)
                //$("#div_informacion").show();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });
});