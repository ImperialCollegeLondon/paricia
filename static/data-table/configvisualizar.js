var $table = $('#table');
var $btn_guardar = $('#btn_guardar');
var $btn_borrar = $('#btn_borrar');
var $modal_form = $('#modal_form');
var $modal_delete = $('#modal_delete');

$(function() {
    $('#toolbar').find('select').change(function () {
        $table.bootstrapTable('destroy').bootstrapTable({
            exportDataType: $(this).val(),
            exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel', 'pdf'],
            columns: [
                {
                    field: 'state',
                    checkbox: true,
                    visible: $(this).val() === 'selected'
                },
                {
                    field: 'id',
                    title: 'Id',
                    visible: false
                },
                {
                    field: 'estacion',
                    title: 'Estación'
                },
                {
                    field: 'variable',
                    title: 'Variable'
                },
                {
                    field: 'umbral_superior',
                    title: 'Umbral Superior'
                },
                {
                    field: 'umbral_inferior',
                    title: 'Umbral Inferior'
                },
                {
                    field: 'accion',
                    title: 'Acción',
                    formatter: operateFormatter,
                    events: {
                       'click .edit': editar,
                       'click .remove': remover
                    }
                }

            ]
        })
    }).trigger('change');

    function operateFormatter(value, row, index) {
        return [
            '<a class="edit" href="javascript:void(0)" title="Editar">',
            '<i class="far fa-edit"></i>',
            '</a>  ',
            '<a class="remove" href="javascript:void(0)" title="Eliminar">',
            '<i class="fa fa-trash-alt"></i>',
            '</a>'
        ].join('')
    }

    $("#link_create").click(function(){
        abrir_formulario($(this).attr('href'),"form");
        return false;
    });

    $btn_guardar.click(function(){

        guardar_registro();
        //$modal_form.modal("hide");
        //$table.bootstrapTable('refresh');

    });

    $btn_borrar.click(function(){
        eliminar_registro();
        //$modal_delete.modal("hide");
        //$table.bootstrapTable('refresh')

    });

    function editar(e, value, row) {
        //alert(JSON.stringify(row));
        link = '/configvisualizar/edit/'+row.id+'/';
        abrir_formulario(link, "form");
    }

    function remover(e, value, row){
        link = '/configvisualizar/'+row.id+'/delete';
        abrir_formulario(link, 'delete');

    }

});
