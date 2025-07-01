# config.py

# Path to your custom SSL certificate file (PEM format).
# Set this to the full path of your custom proxy certificate if needed.
# Example: "C:/Users/balis/custom_proxy_cert.pem"
CUSTOM_CERT_PATH = None  # or r"C:/Users/balis/custom_proxy_cert.pem"

# Set to True to disable SSL verification.
# WARNING: Disabling SSL verification is NOT recommended for production environments.
# This should only be used temporarily for local testing or debugging.
DISABLE_SSL_VERIFY = False
