import streamlit as st
import streamlit.components.v1 as components

def setup_pwa():
    """Setup PWA configuration for Streamlit app"""
    
    # PWA Meta tags and manifest
    pwa_html = """
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#ff006e">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Plant Doctor">
        
        <link rel="manifest" href="./manifest.json">
        <link rel="apple-touch-icon" href="./icon-192.png">
        
        <script>
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                    navigator.serviceWorker.register('./sw.js')
                        .then(function(registration) {
                            console.log('SW registered: ', registration);
                        }, function(registrationError) {
                            console.log('SW registration failed: ', registrationError);
                        });
                });
            }
        </script>
    </head>
    """
    
    components.html(pwa_html, height=0)
    
    # Install prompt
    install_prompt = """
    <div id="install-container" style="
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    ">
        <button id="install-btn" onclick="installPWA()" style="
            background: linear-gradient(45deg, #ff006e, #8338ec);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(255, 0, 110, 0.4);
            display: block;
        ">
            📱 Install App
        </button>
    </div>
    
    <script>
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('install-btn').style.display = 'block';
        });
        
        function installPWA() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        document.getElementById('install-container').style.display = 'none';
                    }
                    deferredPrompt = null;
                });
            } else {
                // Fallback for browsers that don't support install prompt
                alert('To install: Tap browser menu (3 dots) > "Add to Home Screen" or "Install App"');
            }
        }
        
        // Hide button if already installed
        window.addEventListener('appinstalled', () => {
            document.getElementById('install-container').style.display = 'none';
        });
    </script>
    """
    
    components.html(install_prompt, height=50)