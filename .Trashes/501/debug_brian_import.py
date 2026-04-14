import sys
import os
import traceback

print("--- Debugging Import Issues ---")
print(f"Current Working Directory: {os.getcwd()}")
print("\nDirectory Listing:")
try:
    for item in os.listdir("."):
        print(f" - {item}")
        if item == "brian" and os.path.isdir("brian"):
            print("   (brian contents):")
            for sub in os.listdir("brian"):
                print(f"     - {sub}")
except Exception as e:
    print(f"Error listing directory: {e}")

print("\nSystem Path (sys.path):")
for p in sys.path:
    print(f" - {p}")

print("\nAttempting to import brian...")
try:
    import brian
    print("SUCCESS: brian imported.")
    print(f"brian file: {brian.__file__}")
except ImportError:
    print("FAILURE: ImportError caught.")
    traceback.print_exc()
except Exception:
    print("FAILURE: Other exception caught.")
    traceback.print_exc()
