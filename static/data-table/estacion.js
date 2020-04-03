var $table = $('#table');

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
                    field: 'est_codigo',
                    title: 'Código',
                    sortable: true
                },
                {
                    field: 'est_nombre',
                    title: 'Nombre',
                    sortable: true
                },
                {
                    field: 'tipo',
                    title: 'Tipo',
                    sortable: true
                },
                {
                    field: 'provincia',
                    title: 'Provincia',
                    sortable: true
                },
                {
                    field: 'administrador',
                    title: 'Administrador',
                    sortable: true
                },
                {
                    field: 'est_latitud',
                    title: 'Latitud',
                    visible: $(this).val() === 'all'
                },
                {
                    field: 'est_longitud',
                    title: 'Longitud',
                    visible: $(this).val() === 'all'
                },
                {
                    field: 'est_altura',
                    title: 'Altura',
                    visible: $(this).val() === 'all'
                },

                {
                    field: 'estado',
                    title: 'Estado',
                    visible: false
                },

                {
                    field: 'fecha_inicio',
                    title: 'Fecha Inicio Operación',
                    sortable: true,
                    visible: false
                },

                {
                    field: 'area_aporte',
                    title: 'Área de Aporte (km)',
                    sortable: true,
                    visible: false
                },

                {
                    field: 'sistema_cuenca',
                    title: 'Sistema-Cuenca',
                    sortable: true,
                    visible: false
                },

                {
                    field: 'accion',
                    title: 'Acción'
                }

            ]
        })
    }).trigger('change')
})