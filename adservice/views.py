import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Trade, Image

# Create your views here.
def serialize_trade(trade, include_images=False):
    data = {
        'id': trade.id,
        'title': trade.title,
        'created': trade.created.isoformat(),
        'updated': trade.updated.isoformat(),
        'author': trade.author.id,
        'status': trade.status,
        'text': trade.text,
    }
    if include_images:
        data['images'] = [
            {'id': img.id, 'image': img.image.url}
            for img in trade.images.all()
        ]
    return data

def serialize_trade_list(trade):
    
    return {
        'id': trade.id,
        'title': trade.title,
        'created': trade.created.isoformat()
    }

@csrf_exempt
@require_http_methods(['GET', "POST"])
def trades_list(request):
    if request.method == "GET":
        trades = Trade.objects.filter(status=True)
        data = [serialize_trade_list(t) for t in trades]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        title = body.get('title')
        text = body.get('text')
        status = body.get('status', True)
        
        if not title or not text:
            return JsonResponse({'error': 'title and text are required fields'}, status=400)
        
        if not isinstance(status, bool):
            return JsonResponse({'error': 'status must be boolean'}, status=400)
        
        trade = Trade.objects.create(
            author = request.user,
            title = title,
            text = text,
            status = status
        )
        data = serialize_trade(trade)
        return JsonResponse(data, status=201)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def trade_detail(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    
    if request.method == 'GET':
        data = serialize_trade(trade, include_images=True)
        
        return JsonResponse(data)
    
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        if trade.author != request.user:
            return JsonResponse({'error': 'You are not an author'}, status=403)
        
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        title = body.get('title')
        text = body.get('text')
        status = body.get('status')
        
        if title is not None:
            trade.title = title
        if text is not None:
            trade.text = text
        if status is not None:
            if not isinstance(status, bool):
                return JsonResponse({'error': 'Status must be boolean'})
            trade.status = status
            
        try:
            trade.full_clean()
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict}, status=400)
        
        trade.save()
        data = serialize_trade(trade)
        return JsonResponse(data)
    

@csrf_exempt
@login_required
@require_http_methods(['POST'])
def add_image(request, trade_id):
        trade = get_object_or_404(Trade, id=trade_id)
        
        if request.user != trade.author:
            return JsonResponse({'error': 'You are not the author'})
        
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'Image file is required'}, status=400)
        
        
        image_file = request.FILES['image']
        
        image = Image.objects.create(
            author = request.user,
            trade = trade,
            image = image_file
        )
        
        data = {
            'id': image.id,
            'created_at': image.created_at.isoformat(),
            'updated_at': image.updated_at.isoformat(),
            'image': image.image.url,
            'author': image.author.id,
            'trade': image.trade.id,
        }
        
        return JsonResponse(data, status=200)
    
@csrf_exempt
@login_required
@require_http_methods(['DELETE'])
def delete_image(request, trade_id, image_id):
    trade = get_object_or_404(Trade, id=trade_id)
    image = get_object_or_404(Image, id=image_id, trade=trade)
    
    if request.user != image.author:
        return JsonResponse({'error': 'You are not the author'}, status=403)
    
    image.delete()
    return JsonResponse({}, status=204)