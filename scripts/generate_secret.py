#!/usr/bin/env python3
"""
Generate a secure secret key for production deployment
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(32)
    print("=" * 60)
    print("Generated SECRET_KEY for production:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("\nSet this in your deployment platform's environment variables:")
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
