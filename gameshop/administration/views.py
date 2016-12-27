from django.shortcuts import render, HttpResponseRedirect,get_object_or_404, reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *

# @user_passes_test(lambda u: u.is_superuser)

def admin_page(request):
    # TODO: сделать доступ у админке только суперпользователю
    users = User.objects.all()
    return render(request, 'admin_page.html', {'users': users})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponseRedirect('/admin/')


def gameProductList(request):
    games = GameProduct.objects.all()
    paginator = Paginator(games, 50)
    page = request.GET.get('page')
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)

    return render(request, 'adminGameProducts.html', {'games': games})


def gameProductDetail(request,pk):
    game = get_object_or_404(GameProduct, pk = pk)
    return render(request, 'adminGameProductDetail.html', {'game': game})


def gameProductCreate(request):
    if request.method == 'POST':
        form = GameProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gameProductList'))
        context = {'form': form}
        return render(request, 'adminGameProductCreate.html', context)
    context = {'form': GameProductForm}
    return render(request, 'adminGameProductCreate.html', context)


def gameProductUpdate(request, pk):
    game = get_object_or_404(GameProduct,pk = pk)
    if request.method == 'POST':
        form = GameProductForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gameProductList'))
        context = {'form': form}
        return render(request, 'adminGameProductCreate.html', context)
    context = {'form': GameProductForm(instance=game)}
    return render(request, 'adminGameProductCreate.html', context)


def gameProductDelete(request,pk):
    game = get_object_or_404(GameProduct, pk = pk)
    game.delete()
    return HttpResponseRedirect(reverse('gameProductList'))