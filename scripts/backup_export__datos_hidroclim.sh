#!/bin/bash

source /home/adminparamh2o/server/venv/bin/activate
alias py_manage="python /home/adminparamh2o/server/paramh2o/manage.py"
EXPORT_PATH="/media/backup/20210926"
py_manage dumpdata --indent 2 anuarios.var1anuarios > $EXPORT_PATH/anuarios_var1anuarios.json
py_manage dumpdata --indent 2 anuarios.var2anuarios > $EXPORT_PATH/anuarios_var2anuarios.json
py_manage dumpdata --indent 2 anuarios.var3anuarios > $EXPORT_PATH/anuarios_var3anuarios.json
py_manage dumpdata --indent 2 anuarios.var4anuarios > $EXPORT_PATH/anuarios_var4anuarios.json
py_manage dumpdata --indent 2 anuarios.viento > $EXPORT_PATH/anuarios_viento.json
py_manage dumpdata --indent 2 anuarios.var6anuarios > $EXPORT_PATH/anuarios_var6anuarios.json
py_manage dumpdata --indent 2 anuarios.var7anuarios > $EXPORT_PATH/anuarios_var7anuarios.json
py_manage dumpdata --indent 2 anuarios.radiacionmaxima > $EXPORT_PATH/anuarios_radiacionmaxima.json
py_manage dumpdata --indent 2 anuarios.radiacionminima > $EXPORT_PATH/anuarios_radiacionminima.json
py_manage dumpdata --indent 2 anuarios.var8anuarios > $EXPORT_PATH/anuarios_var8anuarios.json
py_manage dumpdata --indent 2 anuarios.var9anuarios > $EXPORT_PATH/anuarios_var9anuarios.json
py_manage dumpdata --indent 2 anuarios.var10anuarios > $EXPORT_PATH/anuarios_var10anuarios.json
py_manage dumpdata --indent 2 anuarios.var11anuarios > $EXPORT_PATH/anuarios_var11anuarios.json

py_manage dumpdata --indent 2 mensual.var1mensual > $EXPORT_PATH/mensual_var1mensual.json
py_manage dumpdata --indent 2 mensual.var2mensual > $EXPORT_PATH/mensual_var2mensual.json
py_manage dumpdata --indent 2 mensual.var3mensual > $EXPORT_PATH/mensual_var3mensual.json
py_manage dumpdata --indent 2 mensual.var4mensual > $EXPORT_PATH/mensual_var4mensual.json
py_manage dumpdata --indent 2 mensual.var5mensual > $EXPORT_PATH/mensual_var5mensual.json
py_manage dumpdata --indent 2 mensual.var6mensual > $EXPORT_PATH/mensual_var6mensual.json
py_manage dumpdata --indent 2 mensual.var7mensual > $EXPORT_PATH/mensual_var7mensual.json
py_manage dumpdata --indent 2 mensual.var8mensual > $EXPORT_PATH/mensual_var8mensual.json
py_manage dumpdata --indent 2 mensual.var9mensual > $EXPORT_PATH/mensual_var9mensual.json
py_manage dumpdata --indent 2 mensual.var10mensual > $EXPORT_PATH/mensual_var10mensual.json
py_manage dumpdata --indent 2 mensual.var11mensual > $EXPORT_PATH/mensual_var11mensual.json

py_manage dumpdata --indent 2 anual.var1anual > $EXPORT_PATH/anual_var1anual.json

exit


source /home/program/desarrollo/venv_imhea/bin/activate
alias py_manage="python /home/program/desarrollo/imhea/manage.py"
IMPORT_PATH="/home/program/Desktop/baks_paramh2o/20210926"
py_manage loaddata $IMPORT_PATH/anuarios_var1anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var2anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var3anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var4anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_viento.json
py_manage loaddata $IMPORT_PATH/anuarios_var6anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var7anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_radiacionmaxima.json
py_manage loaddata $IMPORT_PATH/anuarios_radiacionminima.json
py_manage loaddata $IMPORT_PATH/anuarios_var8anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var9anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var10anuarios.json
py_manage loaddata $IMPORT_PATH/anuarios_var11anuarios.json