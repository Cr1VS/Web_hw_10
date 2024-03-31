from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


from .forms import TagForm, QuoteForm, SearchForm, AuthorForm
from .models import Tag, Quote, Author


def main(request, page=1):  # Добавляем параметр 'page' со значением по умолчанию 1
    query = request.GET.get('query', '')

    if query:
        # Поиск цитат по тегам или имени автора
        quotes = Quote.objects.filter(tags__name__icontains=query) | Quote.objects.filter(author__icontains=query)
    else:
        # Отображение всех цитат
        quotes = Quote.objects.all()

    # Реализация пагинации
    paginator = Paginator(quotes, 10)  # Показываем по 10 цитат на странице
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        # Если 'page' не является целым числом, отображаем первую страницу
        quotes = paginator.page(1)
    except EmptyPage:
        # Если 'page' находится за пределами допустимого диапазона (например, 9999), отображаем последнюю страницу
        quotes = paginator.page(paginator.num_pages)

    # Получение топ-10 тегов
    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]

    return render(request, 'quotes/index.html', {'quotes': quotes, 'top_tags': top_tags, 'query': query})


def author(request,fullname):
    author=Author.objects.get(fullname=fullname)
    return render(request,'quotes/author.html', context={'author': author})

def tag_info(request, name, page=1):
    quotes = Quote.objects.filter(tags__name__iexact=name)
    form = SearchForm(request.GET or None)
    
    if "search_tags" in request.GET and form.is_valid():
        search_tags = form.cleaned_data["search_tags"]
        quotes = quotes.filter(tags__name__icontains=search_tags)
    
    top_ten_tags = Tag.objects.annotate(num_quotes=Count("quotes")).order_by("-num_quotes")[:10]
    per_page = 10
    paginator = Paginator(quotes, per_page)
    
    try:
        quotes_on_page = paginator.page(page)
    except PageNotAnInteger:
        quotes_on_page = paginator.page(1)
    except EmptyPage:
        quotes_on_page = paginator.page(paginator.num_pages)
    
    return render(request, "quotes/quotes_by_tag.html", context={
        "quotes": quotes_on_page,
        "top_ten_tags": top_ten_tags,
        "form": form,
        "tag_name": name
    })


@login_required
def tag_add(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/tag_add  .html", {"form": form})

    return render(request, "quotes/tag_add.html", {"form": TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.filter(user=request.user)

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()

            selected_tags = request.POST.getlist("tags")

            for tag_name in selected_tags:
                tag = Tag.objects.get(name=tag_name)
                new_quote.tags.add(tag)

            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/quote.html", {"tags": tags, "form": form})

    return render(request, "quotes/quote.html", {"tags": tags, "form": QuoteForm()})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_author.html", {"form": form})

    return render(request, "quotes/add_author.html", {"form": AuthorForm()})


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
