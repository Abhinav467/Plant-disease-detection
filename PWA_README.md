# Plant Disease Detection PWA

Your Streamlit app has been converted to a Progressive Web App (PWA)!

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements_pwa.txt
   ```

2. **Run the PWA:**
   ```bash
   streamlit run main.py
   ```

3. **Install as app:**
   - Open in Chrome/Edge browser
   - Look for "Install App" button in top-right
   - Click to install on desktop/mobile

## 📱 PWA Features

- **Offline Support**: Works without internet (cached content)
- **Install Prompt**: Can be installed like a native app
- **App Icons**: Custom icons for home screen
- **Mobile Responsive**: Optimized for mobile devices
- **Fast Loading**: Service worker caching

## 🌐 Deployment Options

### Local Development
```bash
streamlit run main.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy with PWA files included

### Heroku
```bash
# Create Procfile
echo "web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git add .
git commit -m "PWA deployment"
git push heroku main
```

## 📁 PWA Files Created

- `sw.js` - Service worker for offline functionality
- `pwa_setup.py` - PWA configuration module
- `manifest.json` - App manifest (already existed)
- `icon-192.png` & `icon-512.png` - App icons
- `.streamlit/config.toml` - Streamlit configuration

## 🔧 Customization

- Edit `manifest.json` for app details
- Modify `sw.js` for caching strategy
- Update icons in `create_icons.py`
- Customize PWA setup in `pwa_setup.py`

Your plant disease detection app is now a full PWA! 🌱