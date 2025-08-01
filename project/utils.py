def get_client_info(request):
    ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
    return ip, user_agent

def get_client_ip(request):
    """Foydalanuvchining IP manzilini qaytaradi, agar proxy ishlatilgan bo‘lsa ham."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Agar bir nechta IP bo‘lsa (masalan, load balancer orqali kirilgan), birinchi haqiqiy IP ni olamiz
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    # User agent (browser, qurilma, OS haqida)
    return ip, 