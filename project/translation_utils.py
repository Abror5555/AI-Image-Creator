# from deep_translator import GoogleTranslator

# def translate_to_english(text):
#     try:
#         if not text or not isinstance(text, str):
#             raise ValueError("Input text must be a non-empty string")
#         # Avtomatik aniqlaydi va inglizchaga tarjima qiladi
#         translated = GoogleTranslator(source='auto', target='en').translate(text)
#         if not translated:
#             raise ValueError("Translation returned empty result")
#         return translated
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text  # Agar tarjima muvaffaqiyatsiz bo'lsa, original matnni qaytarish

from deep_translator import GoogleTranslator

def translate_to_english(text):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        # Kontekstni aniqroq qilish uchun qo'shimcha so'zlar
        if "в форме" in text.lower() or "форме" in text.lower():
            text = text.replace("в форме", "in the shape of").replace("форме", "in the shape of")
        
        # Avtomatik aniqlaydi va inglizchaga tarjima qiladi
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        if not translated:
            raise ValueError("Translation returned empty result")
        
        # Tarjima natijasini tekshirish
        if "poultry" in translated.lower():
            # Agar "poultry" bo'lsa, kontekstni qayta shakllantirish
            translated = translated.replace("poultry", "bird")
        
        print(f"Translated text: {translated}")
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        # Agar tarjima muvaffaqiyatsiz bo'lsa, original matnni qaytarish
        return text