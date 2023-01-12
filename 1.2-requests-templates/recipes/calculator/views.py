from django.shortcuts import render, reverse, redirect


def landing_page(request):
    pages = {
        'Omelette': reverse('omelette'),
        'Pasta': reverse('pasta'),
        "Sandwich": reverse('sandwich')
    }
    context = {'pages': pages}
    return render(request, 'calculator/landing_page.html', context)


def calculate_dishes(request, dish, recipe):
    servings = request.GET.get("servings", 1)
    try:
        serv_int = int(servings)
        if serv_int <= 0:
            return redirect('page_404')
    except ValueError:
        return redirect('page_404')
    recipe.update((k, v * serv_int) for k, v in recipe.items())
    context = {
        'dish': dish,
        'recipe': recipe,
        'servings': serv_int
    }
    return render(request, 'calculator/dish.html', context)


def omelette_view(request):
    omelette_ingr = {
        'eggs, pc': 2,
        'milk, l': 0.1,
        'salt, sp': 0.5,
    }
    return calculate_dishes(request, 'Omelette', omelette_ingr)


def pasta_view(request):
    pasta_ingr = {
        'macaroni, g': 0.3,
        'cheese, g': 0.05,
    }
    return calculate_dishes(request, 'Pasta', pasta_ingr)


def sandwich_view(request):
    sandwich_ingr = {
        'bread, pc': 1,
        'sausage, pc': 1,
        'cheese, pc': 1,
        'tomato, pc': 1
    }
    return calculate_dishes(request, 'Sandwich', sandwich_ingr)


def page_404(request):
    return render(request, 'calculator/page_404.html')
