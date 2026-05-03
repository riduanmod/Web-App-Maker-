import os
import urllib.parse
from flask import Flask, request, jsonify, send_from_directory, Response

# Vercel-এর জন্য Absolute Path সেট করা
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ফাইলগুলো public ফোল্ডারে থাকলে সেটি ব্যবহার করবে, নাহলে মেইন ফোল্ডার ব্যবহার করবে
PUBLIC_DIR = os.path.join(BASE_DIR, 'public') if os.path.isdir(os.path.join(BASE_DIR, 'public')) else BASE_DIR

app = Flask(__name__, static_folder=PUBLIC_DIR)

@app.route('/manifest.json')
def get_manifest():
    name = request.args.get('name', 'Generated PWA')
    url = request.args.get('url', '')
    icon = request.args.get('icon', 'https://via.placeholder.com/512.png?text=PWA')
    theme = request.args.get('theme', '#0b0f19')

    manifest = {
        "Developer_Credit": "Developer: Riduanul Islam",
        "name": name,
        "short_name": name[:12],
        "start_url": f"/app?name={urllib.parse.quote(name)}&url={urllib.parse.quote(url)}&icon={urllib.parse.quote(icon)}&theme={urllib.parse.quote(theme)}",
        "display": "standalone",
        "background_color": theme,
        "theme_color": theme,
        "icons": [
            {"src": icon, "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": icon, "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
        ]
    }
    return jsonify(manifest)

@app.route('/app')
def get_app():
    name = request.args.get('name', 'Generated PWA')
    url = request.args.get('url', '')
    icon = request.args.get('icon', 'https://via.placeholder.com/512.png?text=PWA')
    theme = request.args.get('theme', '#3B82F6')

    if not url:
        return "Target URL is required.", 400

    manifest_query = f"name={urllib.parse.quote(name)}&url={urllib.parse.quote(url)}&icon={urllib.parse.quote(icon)}&theme={urllib.parse.quote(theme)}"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Install {name}</title>
        <link rel="manifest" href="/manifest.json?{manifest_query}">
        <meta name="theme-color" content="{theme}">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body, html {{ margin: 0; padding: 0; height: 100%; font-family: system-ui, -apple-system, sans-serif; background-color: #0b0f19; color: white; }}
            #app-frame {{ display: none; width: 100%; height: 100%; border: none; background: #fff; }}
            .install-card {{ background: linear-gradient(180deg, rgba(20,27,45,1) 0%, rgba(11,15,25,1) 100%); border: 1px solid rgba(255,255,255,0.05); }}
        </style>
    </head>
    <body class="flex flex-col items-center justify-center min-h-screen relative">
        
        <div class="absolute top-0 w-full h-1" style="background-color: {theme}; box-shadow: 0 0 20px {theme};"></div>

        <div id="install-screen" class="w-11/12 max-w-sm install-card rounded-3xl p-8 text-center shadow-2xl z-10">
            
            <div class="w-28 h-28 mx-auto mb-5 rounded-3xl p-1 shadow-lg" style="background: linear-gradient(135deg, {theme}, transparent);">
                <img src="{icon}" alt="Icon" class="w-full h-full rounded-2xl object-cover bg-white">
            </div>
            
            <h1 class="text-2xl font-bold mb-1 tracking-tight">{name}</h1>
            <p class="text-gray-400 text-sm mb-8 font-medium">Installable Web Application</p>

            <button id="install-btn" class="w-full text-white font-bold py-4 rounded-xl transition-all flex items-center justify-center gap-2 text-lg shadow-lg hover:brightness-110 mb-6" style="background-color: {theme};">
                <i class="fa-solid fa-download"></i> Install App
            </button>

            <div class="pt-6 border-t border-gray-800/50 bg-black/20 rounded-2xl p-4 mt-2 border border-white/5">
                <h3 class="text-gray-300 font-semibold mb-1 text-sm">Install on another device</h3>
                <p class="text-gray-500 text-xs mb-4">Scan the QR code or copy the link</p>
                
                <div class="flex items-center justify-center gap-4">
                    <div class="bg-white p-1.5 rounded-xl">
                        <img id="qrImage" src="" alt="QR" class="w-16 h-16 object-contain">
                    </div>
                    <div class="flex flex-col gap-2 w-full max-w-[140px]">
                        <button onclick="copyInstallLink()" id="copy-btn" class="w-full bg-blue-600/10 hover:bg-blue-600/30 text-blue-400 border border-blue-500/20 font-medium py-2 rounded-lg transition-colors text-sm flex items-center justify-center gap-2">
                            <i class="fa-regular fa-copy"></i> Copy Link
                        </button>
                        <span id="copy-msg" class="text-green-400 text-[10px] uppercase font-bold tracking-wider opacity-0 transition-opacity">Link Copied!</span>
                    </div>
                </div>
            </div>
        </div>

        <iframe id="app-frame" src="{url}" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>

        <script>
            // Generate QR code URL
            const currentUrl = window.location.href;
            document.getElementById('qrImage').src = `https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=${{encodeURIComponent(currentUrl)}}&color=0b0f19&bgcolor=ffffff`;

            // Copy Link Functionality
            function copyInstallLink() {{
                navigator.clipboard.writeText(currentUrl).then(() => {{
                    const msg = document.getElementById('copy-msg');
                    const btn = document.getElementById('copy-btn');
                    btn.classList.add('border-green-500/50', 'text-green-400');
                    btn.innerHTML = `<i class="fa-solid fa-check"></i> Copied`;
                    msg.classList.remove('opacity-0');
                    
                    setTimeout(() => {{
                        btn.classList.remove('border-green-500/50', 'text-green-400');
                        btn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy Link`;
                        msg.classList.add('opacity-0');
                    }}, 2000);
                }});
            }}

            // Service Worker Registration
            if ('serviceWorker' in navigator) {{
                window.addEventListener('load', () => {{
                    navigator.serviceWorker.register('/sw.js');
                }});
            }}

            // Standalone Mode Detection
            const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
            
            if (isStandalone) {{
                document.getElementById('install-screen').style.display = 'none';
                document.body.classList.remove('justify-center', 'items-center');
                document.getElementById('app-frame').style.display = 'block';
            }} else {{
                let deferredPrompt;
                const installBtn = document.getElementById('install-btn');

                window.addEventListener('beforeinstallprompt', (e) => {{
                    e.preventDefault();
                    deferredPrompt = e;
                }});

                installBtn.addEventListener('click', async () => {{
                    if (!deferredPrompt) {{
                        alert("Install prompt not ready. Use the browser menu to 'Add to Home screen'.");
                        return;
                    }}
                    
                    deferredPrompt.prompt();
                    const {{ outcome }} = await deferredPrompt.userChoice;
                    deferredPrompt = null;
                }});

                window.addEventListener('appinstalled', () => {{
                    document.getElementById('install-screen').style.display = 'none';
                    document.body.classList.remove('justify-center', 'items-center');
                    document.getElementById('app-frame').style.display = 'block';
                }});
            }}
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

@app.route('/')
def serve_index():
    return send_from_directory(PUBLIC_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(PUBLIC_DIR, path)):
        return send_from_directory(PUBLIC_DIR, path)
    return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
