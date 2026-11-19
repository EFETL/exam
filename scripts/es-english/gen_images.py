#!/usr/bin/env python3
"""用 Gemini 為國小英文闖關的每個動畫場景畫可愛插圖。

產出：es/english/<冊別>/img/<單元>-<場景序號>.png（已存在就跳過）；畫完再跑 build.py，頁面就會用圖取代 emoji。
金鑰：雲端環境的 Network secret（標頭 x-goog-api-key）由代理自動帶入；本機可設環境變數 GEMINI_API_KEY。
用法：python3 scripts/es-english/gen_images.py [冊別…]　　python3 scripts/es-english/gen_images.py --models（列出可用的畫圖模型）
"""
import base64, io, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402

API = 'https://generativelanguage.googleapis.com/v1beta'
MODEL = os.environ.get('GEMINI_IMAGE_MODEL', 'gemini-2.5-flash-image')
STYLE = ('Cute kawaii children\'s picture-book illustration for Taiwanese elementary school kids learning English. '
         'Pastel colors, soft rounded shapes, thick friendly outlines, gentle shading, plain light background, '
         'happy chubby characters, 16:9 composition. Absolutely no text, letters, numbers or words in the image.')


def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method='POST' if body else 'GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('x-goog-api-key', os.environ.get('GEMINI_API_KEY', 'placeholder-replaced-by-proxy'))
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def draw(prompt, out):
    r = call(f'{API}/models/{MODEL}:generateContent', {
        'contents': [{'parts': [{'text': STYLE + '\nScene: ' + prompt}]}],
        'generationConfig': {'responseModalities': ['IMAGE']}})
    for part in r['candidates'][0]['content']['parts']:
        data = part.get('inlineData') or part.get('inline_data')
        if data:
            raw = base64.b64decode(data['data'])
            try:
                from PIL import Image
                im = Image.open(io.BytesIO(raw)).convert('RGB')
                im.thumbnail((960, 540))
                im.save(out, 'PNG', optimize=True)
            except ImportError:
                open(out, 'wb').write(raw)
            return True
    return False


def main(names):
    if names == ['--models']:
        for m in call(f'{API}/models?pageSize=200')['models']:
            if 'image' in m['name'] or 'imagen' in m['name']:
                print(m['name'])
        return
    bdir = os.path.join(HERE, 'books')
    names = names or sorted(f[:-3] for f in os.listdir(bdir) if f.endswith('.py'))
    for n in names:
        book = build.load(os.path.join(bdir, n + '.py'))
        idir = os.path.join(build.OUT, book['path'], 'img')
        os.makedirs(idir, exist_ok=True)
        for k, d in book['units'].items():
            for i, sc in enumerate(d.get('scenes', [])):
                out = os.path.join(idir, f'{k}-{i}.png')
                if os.path.exists(out):
                    continue
                prompt = f"{sc['tag']} (show: {sc['emo']}; topic: {d['title']})"
                try:
                    print(n, k, i, 'OK' if draw(prompt, out) else '沒有回傳圖片')
                except Exception as e:
                    print(n, k, i, '失敗', e)


if __name__ == '__main__':
    main(sys.argv[1:])
