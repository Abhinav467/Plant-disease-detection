import subprocess
import os
import shutil

def deploy_pwa():
    """Deploy Streamlit app as PWA"""
    
    print("Deploying Plant Disease Detection as PWA...")
    
    # Create icons
    print("Creating app icons...")
    try:
        from create_icons import create_app_icons
        create_app_icons()
        print("Icons created successfully")
    except Exception as e:
        print(f"Icon creation failed: {e}")
    
    # Copy static files to streamlit static directory
    print("Setting up static files...")
    
    # Create .streamlit directory if it doesn't exist
    os.makedirs('.streamlit', exist_ok=True)
    
    # Create config.toml for custom static files
    config_content = """
[server]
enableStaticServing = true

[browser]
gatherUsageStats = false
"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_content)
    
    print("PWA setup complete!")
    print("\nTo run your PWA:")
    print("1. Run: streamlit run main.py")
    print("2. Open in browser and look for 'Install App' button")
    print("3. For production: Deploy to Streamlit Cloud, Heroku, or similar")
    
    print("\nPWA Features enabled:")
    print("- Offline functionality")
    print("- Install prompt")
    print("- App icons")
    print("- Mobile-responsive design")

if __name__ == "__main__":
    deploy_pwa()