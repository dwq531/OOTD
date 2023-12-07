from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Clothes

@require_POST
def add_clothes(request):
    """
        添加衣服
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        content = request.POST
        clothes_ID = Clothes.clothesid + 1
        clothes_name = content.get("name")
        clothes_main_type = content.get("Mtype")
        clothes_detail_type = content.get("Dtype")
        clothes_picture_url = content.get("pictureUrl")

        new_clothes = Clothes(
            clothes_ID = clothes_ID,
            clothes_name = clothes_name,
            clothes_main_type = clothes_main_type,
            clothes_detail_type = clothes_detail_type,
            clothes_picture_url = clothes_picture_url,
        )
        new_clothes.save_image_from_url()
        new_clothes.save()

        return JsonResponse({"message": "Clothes added to the wardrobe successfully"}, status=201)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

