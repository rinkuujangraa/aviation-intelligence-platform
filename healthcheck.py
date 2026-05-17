"""
healthcheck.py
Quick script to verify all dependencies and APIs before starting
"""
import sys
import os

print("=" * 60)
print("🔍 Aviation Intelligence Platform - Health Check")
print("=" * 60)
print()

# Check Python version
print(f"✓ Python version: {sys.version.split()[0]}")

# Check critical dependencies
critical_deps = [
    'streamlit',
    'pandas',
    'requests',
    'numpy'
]

print("\n📦 Checking dependencies...")
missing = []
for dep in critical_deps:
    try:
        __import__(dep)
        print(f"  ✓ {dep}")
    except ImportError:
        print(f"  ✗ {dep} - MISSING!")
        missing.append(dep)

if missing:
    print(f"\n❌ Missing dependencies: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Check environment variables
print("\n🔑 Checking environment variables...")
required_vars = ['AIRLABS_API_KEY', 'MAPBOX_TOKEN']
missing_vars = []

for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"  ✓ {var} (length: {len(value)})")
    else:
        print(f"  ✗ {var} - NOT SET!")
        missing_vars.append(var)

if missing_vars:
    print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
    print("App will run but features may be limited")

# Test API connectivity (optional)
print("\n🌐 Testing API connectivity...")
try:
    import requests
    api_key = os.getenv('AIRLABS_API_KEY')
    if api_key:
        response = requests.get(
            f"https://airlabs.co/api/v9/airlines?api_key={api_key}",
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ AirLabs API responding")
        else:
            print(f"  ⚠️  AirLabs API returned status {response.status_code}")
    else:
        print("  ⊘ AirLabs API key not set - skipping test")
except Exception as e:
    print(f"  ⚠️  API test failed: {str(e)[:50]}")

print("\n" + "=" * 60)
if not missing and not missing_vars:
    print("✅ All checks passed! Ready to start.")
    print("=" * 60)
    sys.exit(0)
else:
    print("⚠️  Some checks failed but app may still work")
    print("=" * 60)
    sys.exit(0)  # Don't fail, just warn
