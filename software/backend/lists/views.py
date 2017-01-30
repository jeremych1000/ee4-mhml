from django.shortcuts import render, redirect
from lists.models import Item
from lists.models import List
from lists.forms import text_form


# Create your views here.
def home_page(request):
    return render(request, 'homepage.html', {'list_ids': [l.id for l in List.objects.all()], 'form': text_form()})


def view_list(request, list_id):
    form = text_form()
    id = int(list_id)
    all_list = List.objects.filter(id=id)
    if all_list.count() == 0:
        return redirect('/')
    else:
        all_item = Item.objects.filter(list=all_list[0]).order_by('id')
        return render(request, 'list.html', {'items': all_item, 'listID': id, 'form': form})



def new_item(request, list_id):
    list_id = int(list_id)
    all_list = List.objects.filter(id=list_id)
    list_ = all_list[0]
    if request.method == 'POST':
        form =text_form(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST.get('text'),
                            list=list_)
            return redirect(list_)


def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        if request.POST.get('text', '') != '':
            new_text = request.POST.get('text')
            Item.objects.create(text=new_text, list=list_)
        return redirect(list_)


def delete_item(request, itemID, listID):
    if request.method == 'POST':
        Item.objects.filter(id=itemID).delete()
        return redirect('/lists/%d/' % int(listID))


def delete_list(request, listID):
    if request.method == 'POST':
        List.objects.filter(id=listID).delete()
        return redirect('/lists/%d/' % int(listID))
