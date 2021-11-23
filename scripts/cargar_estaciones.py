import pandas as pd

archivo = pd.read_excel(archivo_src, header=None, skiprows=firstlin e -1, skipfooter=skipfooter, engine=None,
                        error_bad_lines=False, index_col=None)