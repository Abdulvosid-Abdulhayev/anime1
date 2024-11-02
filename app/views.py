from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import*
# Create your views here.

class Home(View):
    def get(self, request):
        animes = Anime.objects.all()
        categories = Category.objects.all()

        context = {
            "animes": animes,
            "categories": categories,
        }
        return render(request, 'index.html', context=context)
    

class Caregory(View):
    def get(self, request, slug=None):
        # Initialize categories first to avoid UnboundLocalError
        categories = Category.objects.all()

        if slug is None:
            animes = Anime.objects.all()
            category = "All"
            context = {
                "animes": animes,
                "categories": categories, 
                "selected_category": category,
            }
        else:
            # Use get_object_or_404 to fetch the category safely
            category = get_object_or_404(Category, slug=slug)
            animes = Anime.objects.filter(category=category)
            context = {
                "animes": animes,
                "categories": categories,
                "selected_category": category
            }

        return render(request, 'categories.html', context=context)

class Anime_detail(View):
    def get(self, request, selected_category, slug):
        # `Anime` ob'ektini `category__slug` va `slug` orqali olish
        anime = get_object_or_404(Anime,slug=slug)
        
        # Qo'shimcha ma'lumotlarni olish
        categories = Category.objects.all()
        anime_4 = Anime.objects.order_by("?")[:4]
        comments = Coments.objects.filter(anime=anime).order_by('-created_at')  # Kommentlarni olish

        # Ko'rishlar sonini oshirish
        anime.views += 1
        anime.save()

        # Kontekst yaratish
        context = {
            "anime": anime,
            "categories": categories,
            "selected_category": selected_category,
            "anime_4": anime_4,
            "comments": comments,
        }
        return render(request, 'anime-details.html', context=context)

    def post(self, request, selected_category, slug):
            # `Anime` ob'ektini olish
            anime = get_object_or_404(Anime, slug=slug)
            
            # Form ma'lumotlarini olish
            text = request.POST.get("text")
            name = request.POST.get("name", "Anonymous")  # Agar ism berilmagan bo'lsa, "Anonymous"

            # Komment matni mavjudligini tekshirish va saqlash
            if text:
                Coments.objects.create(anime=anime, name=name, text=text)

            # Komment saqlangandan so'ng, qayta yo'naltirish
            return redirect('detail', selected_category=selected_category, slug=slug)