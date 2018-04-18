from django.core.paginator import Paginator


def pagination(lista, page, num_reg):
    # lista=model.objects.all()
    paginator = Paginator(lista, num_reg)
    factor = paginator.num_pages // 2

    if factor > 4:
        factor = 4
    if page is None:
        page = 1
    else:
        page = int(page)
    if page <= 3 and factor >= 3:
        print("caso 1")
        start = 1
        last = 5
    elif page <= 5 and factor < 3:
        start = 1
        last = paginator.num_pages
    elif (paginator.num_pages - page) <= 1 and factor >= 3:
        print("caso2")
        last = paginator.num_pages
        start = last - 5
    else:
        print("caso5")
        start = page - factor // 2
        last = page + factor // 2
    context = {
        'first': '1',
        'last': paginator.num_pages,
        'range': range(start, last + 1),
    }
    return context
