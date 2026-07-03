from aiohttp import web

async def upload_handler(request):
    reader = await request.multipart()

    part = await reader.next()
    if part is None:
        return web.json_response({'error': 'No part in request'}, status=400)

    if not part.filename:
        return web.json_response({'error': 'Expected a file'}, status=400)

    total_size = 0
    while True:
        chunk = await part.read_chunk()
        if not chunk:
            break
        total_size += len(chunk)

    return web.json_response({'size_bytes': total_size})

app = web.Application()
app.router.add_post('/api/upload/', upload_handler)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)