from django.core.paginator import Paginator
from django.db import connection


def pagination(lista, page, num_reg):
    paginator = Paginator(lista, num_reg)
    factor = paginator.num_pages // 2

    if factor > 4:
        factor = 4
    if page is None:
        page = 1
    else:
        page = int(page)
    if page <= 3 and factor >= 3:
        start = 1
        last = 5
    elif page <= 5 and factor < 3:
        start = 1
        last = paginator.num_pages
    elif (paginator.num_pages - page) <= 1 and factor >= 3:
        last = paginator.num_pages
        start = last - 5
    else:
        start = page - factor // 2
        last = page + factor // 2
    context = {
        'first': '1',
        'last': paginator.num_pages,
        'range': range(start, last + 1),
    }
    return context


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_links(model, model_id):

    model_str = str(model.__name__).lower()
    link_view = '<a href="/%%model%%/detail/' + str(model_id) + '">'
    link_view += '<i class="far fa-eye"></i>'
    link_view += '</a> '
    link_view = link_view.replace('%%model%%', model_str)

    link_edit = '<a href="/%%model%%/edit/' + str(model_id) + '">'
    link_edit += '<i class="far fa-edit" aria-hidden="true"></i>'
    link_edit += '</a> '
    link_edit = link_edit.replace('%%model%%', model_str)

    link_delete = '<a href="/%%model%%/' + str(model_id) + '/delete/">'
    link_delete += '<i class="far fa-trash-alt" ></i>'
    link_delete += '</a>'
    link_delete = link_delete.replace('%%model%%', model_str)

    operate = link_view + link_edit + link_delete

    return operate
