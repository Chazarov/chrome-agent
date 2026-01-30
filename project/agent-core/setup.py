"""
Setup script for Chrome Agent
Run this to install dependencies and set up the environment
"""

import subprocess
import sys
import os

def main():
    print("🚀 Chrome Agent Setup")
    print("=" * 60)
    
    # Install requirements
    print("\n1. Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Install Playwright browsers
    print("\n2. Installing Playwright browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✓ Playwright browsers installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("\n3. Creating .env file...")
        with open(".env", "w") as f:
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
        print("✓ .env file created")
        print("\n⚠️  IMPORTANT: Edit .env file and add your Groq API key!")
        print("   Get your key at: https://console.groq.com/")
    else:
        print("\n3. .env file already exists")
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Add your GROQ_API_KEY to .env file")
    print("2. Run: python main.py")
    print("=" * 60 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
