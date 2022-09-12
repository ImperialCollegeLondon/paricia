from rest_framework.renderers import BrowsableAPIRenderer


class TableAPIRenderer(BrowsableAPIRenderer):
    format = "table"
    template = "table.html"
