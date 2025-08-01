import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from .models import AnonymousUserToken, UserSubjectHistory, UserHistory, ImageGenerationConfig
from .translation_utils import translate_to_english
from .image_generator import generate_image_from_text
from .utils import get_client_ip
from .collage import save_individual_images

MEDIA_DIR = "media"

@csrf_exempt
def new_subject(request):
    if request.method == "POST":
        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

        if request.user.is_authenticated:
            user = request.user
            anon_user = None
        else:
            anon, created = AnonymousUserToken.objects.get_or_create(
                ip_address=ip,
                defaults={'user_agent': user_agent}
            )
            if not created:
                anon.user_agent = user_agent
                anon.save(update_fields=["user_agent"])
            user = None
            anon_user = anon

        # Yangi mavzu yaratish
        subject = UserSubjectHistory.objects.create(
            user=user,
            anon_user=anon_user,
            subject="Yangi mavzu"  # Dastlabki standart nom
        )

        # Tanlangan mavzuni session'da saqlash
        request.session['selected_subject_id'] = subject.id

        # Mavzular ro'yxatini qaytarish
        subjects = UserSubjectHistory.objects.filter(
            user=user if user else None,
            anon_user=anon_user if anon_user else None
        ).order_by("created_at")

        return JsonResponse({
            'new_subject_id': subject.id,
            'selected_subject_id': subject.id,
            'subjects': [{'id': s.id, 'subject': s.subject} for s in subjects]
        })

def get_subject_history(request, subject_id):
    if request.method == "GET":
        ip = get_client_ip(request)
        if request.user.is_authenticated:
            user = request.user
            anon_user = None
        else:
            anon, _ = AnonymousUserToken.objects.get_or_create(
                ip_address=ip,
                defaults={'user_agent': request.META.get("HTTP_USER_AGENT", "")[:500]}
            )
            user = None
            anon_user = anon

        history = UserHistory.objects.filter(
            prompt_subject__id=subject_id,
            prompt_subject__user=user if user else None,
            prompt_subject__anon_user=anon_user if anon_user else None
        ).select_related('prompt_subject').order_by("created_at")

        return JsonResponse({
            'history': [{
                'prompt': h.prompt,
                'image_url': h.image_url,
                'created_at': h.created_at.isoformat()
            } for h in history]
        })

def generate_collage(request):
    user_text = request.POST.get("text") if request.method == "POST" else None
    selected_subject_id = request.POST.get("subject_id") or request.session.get('selected_subject_id')
    token_error = False
    image_urls = []

    if request.method == "POST" and user_text:
        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

        subject = None
        user_history_instance = None

        # Foydalanuvchi autentifikatsiya qilinganmi?
        if request.user.is_authenticated:
            user = request.user
            anon_user = None
        else:
            anon, created = AnonymousUserToken.objects.get_or_create(
                ip_address=ip,
                defaults={'user_agent': user_agent}
            )
            if not created:
                anon.user_agent = user_agent
                anon.save(update_fields=["user_agent"])

            if anon.token_count <= 0:
                token_error = True
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'token_error': True,
                        'user_text': user_text,
                        'subjects': [],
                        'image_urls': []
                    })
                return render(request, "form.html", {
                    "token_error": True,
                    "user_text": user_text,
                    "subjects": [],
                    "history": [],
                    "image_urls": [],
                    "selected_subject_id": selected_subject_id
                })
            anon.token_count -= 1
            anon.save()
            user = None
            anon_user = anon

        # Mavzuni aniqlash yoki yaratish
        if selected_subject_id:
            subject = UserSubjectHistory.objects.filter(
                id=selected_subject_id,
                user=user if user else None,
                anon_user=anon_user if anon_user else None
            ).first()
        if not subject:
            subject = UserSubjectHistory.objects.create(
                user=user,
                anon_user=anon_user,
                subject="Yangi mavzu"
            )
            request.session['selected_subject_id'] = subject.id

        # Birinchi prompt mavzu nomini yangilaydi
        if not subject.subject or subject.subject == "Yangi mavzu":
            subject.subject = user_text[:500]  # Promptni mavzu nomi sifatida saqlash
            subject.save()

        # Promptni saqlash
        user_history_instance = UserHistory.objects.create(
            prompt_subject=subject,
            prompt=user_text,
            image_url=[]
        )

        # Rasm generatsiya qilish uchun konfiguratsiya
        config = ImageGenerationConfig.objects.first()
        max_images = config.max_images if config else 4

        # Rasm generatsiya qilish
        translated_text = translate_to_english(user_text)
        for _ in range(max_images):
            image_path = generate_image_from_text(translated_text)
            saved_image_path = save_individual_images(MEDIA_DIR, [os.path.basename(image_path)])[0]
            image_url = "/" + saved_image_path
            image_urls.append(image_url)

        # Barcha rasm URL larini UserHistory ga saqlash
        user_history_instance.image_url = image_urls
        user_history_instance.save()

        # Tanlangan mavzuni session'da saqlash
        request.session['selected_subject_id'] = subject.id

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            subjects = UserSubjectHistory.objects.filter(
                user=request.user if request.user.is_authenticated else None,
                anon_user=anon_user if not request.user.is_authenticated else None
            ).order_by("created_at")
            return JsonResponse({
                'image_urls': image_urls,
                'user_text': user_text,
                'token_error': token_error,
                'subjects': [{'id': s.id, 'subject': s.subject} for s in subjects],
                'selected_subject_id': subject.id
            })

    # Tarix va mavzularni ko'rsatish
    subjects = []
    history = []

    if request.user.is_authenticated:
        subjects = UserSubjectHistory.objects.filter(user=request.user).order_by("created_at")
        if selected_subject_id:
            history = UserHistory.objects.filter(
                prompt_subject__id=selected_subject_id,
                prompt_subject__user=request.user
            ).select_related('prompt_subject').order_by("created_at")[:10]
    elif 'anon_user' in locals():
        subjects = UserSubjectHistory.objects.filter(anon_user=anon_user).order_by("created_at")
        if selected_subject_id:
            history = UserHistory.objects.filter(
                prompt_subject__id=selected_subject_id,
                prompt_subject__anon_user=anon_user
            ).select_related('prompt_subject').order_by("created_at")[:10]

    return render(request, "form.html", {
        "image_urls": image_urls,
        "history": history,
        "user_text": user_text,
        "subjects": subjects,
        "selected_subject_id": selected_subject_id,
        "token_error": token_error
    })