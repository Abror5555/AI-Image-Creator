from django.contrib import admin
from django.utils.html import format_html
from .models import AnonymousUserToken, UserHistory, UserSubjectHistory, ImageGenerationConfig

# Register your models here.


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('prompt_preview', 'subject', 'image_urls_display', 'image_preview', 'created_at')
    list_filter = ('prompt_subject__user', 'prompt_subject__anon_user', 'created_at')
    search_fields = ('prompt', 'prompt_subject__subject')
    readonly_fields = ('created_at', 'image_preview')

    def prompt_preview(self, obj):
        """Promptning qisqa ko'rinishi (50 belgi)."""
        return obj.prompt[:50] + '...' if obj.prompt and len(obj.prompt) > 50 else obj.prompt
    prompt_preview.short_description = 'Prompt'

    def subject(self, obj):
        """Mavzu nomini ko'rsatish."""
        return obj.prompt_subject.subject or 'No Subject'
    subject.short_description = 'Mavzu'

    def image_urls_display(self, obj):
        """image_url ro'yxatidagi barcha URL larni ko'rsatish."""
        if obj.image_url:
            return ", ".join(obj.image_url)
        return 'No Images'
    image_urls_display.short_description = 'Rasm URL lari'

    def image_preview(self, obj):
        """image_url ro'yxatidagi rasmlarni ko'rsatish."""
        if obj.image_url:
            html = ''.join(
                f'<img src="{url}" style="max-height: 100px; max-width: 100px; margin-right: 10px;" />'
                for url in obj.image_url
            )
            return format_html(html)
        return 'No Images'
    image_preview.short_description = 'Rasmlar'
    
@admin.register(UserSubjectHistory)
class UserSubjectHistoryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'anon_user', 'created_at')
    list_filter = ('user', 'anon_user', 'created_at')
    search_fields = ('subject', 'user__username', 'anon_user__ip_address')

@admin.register(AnonymousUserToken)
class AnonymousUserTokenAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'token_count', 'created_at')
    list_editable = ('token_count',)
    search_fields = ('ip_address',)
    list_filter = ('created_at',)


admin.site.register(ImageGenerationConfig)