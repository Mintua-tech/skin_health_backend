from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from .utils import predict_skin_disease
from .models import SkinDisease
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_predict_skin_disease(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        file_path = fs.path(filename)

        # Get AI Prediction
        prediction_label = predict_skin_disease(file_path)

        # Get DB info
        try:
            db_entry = SkinDisease.objects.get(name=prediction_label)
            data = {
                'prediction': prediction_label,
                'common_name': db_entry.common_name,
                'description': db_entry.description,
                'cause': db_entry.cause,
                'medicine': db_entry.medicine
            }
        except SkinDisease.DoesNotExist:
            data = {'prediction': prediction_label, 'common_name': 'Unknown Condition'}

        return JsonResponse(data, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def diagnostic_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save image temporarily
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            file_path = fs.path(filename)
            file_url = fs.url(filename)

            # 2. Run AI Prediction
            prediction_label = predict_skin_disease(file_path)

            # 3. Fetch from DB (Searching by the technical name 'nv', 'mel', etc.)
            try:
                details = SkinDisease.objects.get(name=prediction_label)
            except SkinDisease.DoesNotExist:
                details = None

            return render(request, 'detector/result.html', {
                'details': details,
                'image_url': file_url,
                'prediction': prediction_label
            })
    else:
        form = ImageUploadForm()
    return render(request, 'detector/upload.html', {'form': form})