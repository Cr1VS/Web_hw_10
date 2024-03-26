from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, QuoteForm, SearchForm
from .models import Tag, Quote, Author
from django.core.paginator import Paginator
from django.db.models import Count



def main(request):
    quotes = Quote.objects.all()
    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]
    return render(request, 'quotes/index.html', {'quotes': quotes, 'top_tags': top_tags})
# def index(request):
#     # Получаем все цитаты и авторов
#     quotes = Quote.objects.all()
#     authors = Author.objects.all()

#     # Передаем данные в контекст шаблона
#     context = {
#         'quotes': quotes,
#         'authors': authors,
#     }

#     # Отображаем шаблон
#     return render(request, 'index.html', context)

# def main(request, page=1):

#     quotes = Quote.objects.all()
#     form = SearchForm()
#     if 'search_tags' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             search_tags = form.cleaned_data['search_tags']
#             quotes = quotes.filter(tags__name__icontains=search_tags)
    
#     top_ten_tags = Tag.objects.annotate(num_quotes=Count('name')).order_by('-num_quotes')[:10]
#     per_page = 10
#     paginator = Paginator(list(quotes), per_page)
#     quotes_on_page = paginator.page(page)
#     return render(request, "quotes/index.html", context={'name': quotes_on_page, 'top_ten_tags': top_ten_tags, "form": form})


def author(request,fullname):
    author=Author.objects.get(fullname=fullname)
    return render(request,'quotes/author.html', context={'author': author})

def tag_info(request, name, page=1):
    quotes = Quote.objects.filter(tags__name=name)
    form = SearchForm()
    if 'search_tags' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search_tags = form.cleaned_data['search_tags']
            quotes = quotes.filter(tags__name__icontains=search_tags)
    
    top_ten_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    per_page = 3
    paginator2 = Paginator(list(quotes), per_page)
    quotes_on_page = paginator2.page(page)
    return render(request, "quotes/taginfo.html", context={'quotes': quotes_on_page, 'top_ten_tags': top_ten_tags})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/tag.html", {"form": form})

    return render(request, "quotes/tag.html", {"form": TagForm()})



@login_required
def quote(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"), user=request.user)
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/quote.html", {"tags": tags, "form": form})

    return render(request, "quotes/quote.html", {"tags": tags, "form": QuoteForm()})




@login_required
def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id, user=request.user)
    return render(request, "quotes/detail.html", {"quote": quote})

@login_required
def set_done(request, quote_id):
    Quote.objects.filter(pk=quote_id, user=request.user).update(done=True)
    return redirect(to="quotes:main")

@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id, user=request.user).delete()
    return redirect(to="quotes:main")
