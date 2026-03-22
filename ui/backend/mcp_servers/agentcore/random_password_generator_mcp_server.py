"""
Custom MCP Server - Password Generator & Security Tools
Built during AWS Workshop: Everyday Productivity Accelerators
"""

from mcp.server import FastMCP
from typing import Dict
from datetime import datetime
import random
import string
import re
import hashlib
import os

# Initialize MCP server
mcp = FastMCP("Password Generator & Security Tools")


@mcp.tool(description="Generate a secure password with specified criteria")
def generate_password(
    length: int = 12,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_numbers: bool = True,
    include_symbols: bool = True
) -> Dict:
    """Generate a secure password based on specified criteria."""
    try:
        if length < 4:
            return {"success": False, "error": "Password must be at least 4 characters"}

        chars = ""
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*"

        if not chars:
            return {"success": False, "error": "Must include at least one character type"}

        password = ''.join(random.choice(chars) for _ in range(length))
        strength = check_password_strength_internal(password)

        return {
            "success": True,
            "password": password,
            "length": length,
            "strength": strength,
            "criteria": {
                "uppercase": include_uppercase,
                "lowercase": include_lowercase,
                "numbers": include_numbers,
                "symbols": include_symbols
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Check the strength of a password")
def check_password_strength(password: str) -> Dict:
    """Analyze password strength and provide recommendations."""
    try:
        strength = check_password_strength_internal(password)

        # Analyze password components
        has_lower = bool(re.search(r"[a-z]", password))
        has_upper = bool(re.search(r"[A-Z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_symbol = bool(re.search(r"[!@#$%^&*]", password))

        recommendations = []
        if len(password) < 8:
            recommendations.append("Use at least 8 characters")
        if not has_lower:
            recommendations.append("Add lowercase letters")
        if not has_upper:
            recommendations.append("Add uppercase letters")
        if not has_digit:
            recommendations.append("Add numbers")
        if not has_symbol:
            recommendations.append("Add special characters")

        return {
            "success": True,
            "password_length": len(password),
            "strength": strength,
            "components": {
                "lowercase": has_lower,
                "uppercase": has_upper,
                "numbers": has_digit,
                "symbols": has_symbol
            },
            "recommendations": recommendations
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Generate a memorable passphrase")
def generate_passphrase(word_count: int = 4, separator: str = "-") -> Dict:
    """Generate a memorable passphrase using common words."""
    try:
        # Simple word list (in production, use a larger dictionary)
        words = [
            "apple", "brave", "cloud", "dance", "eagle", "flame", "grace", "happy",
            "island", "jungle", "knight", "light", "magic", "noble", "ocean", "peace",
            "quiet", "river", "storm", "tiger", "unity", "voice", "water", "youth"
        ]

        if word_count < 2 or word_count > 8:
            return {"success": False, "error": "Word count must be between 2 and 8"}

        selected_words = random.sample(words, word_count)
        passphrase = separator.join(selected_words)

        return {
            "success": True,
            "passphrase": passphrase,
            "word_count": word_count,
            "separator": separator,
            "length": len(passphrase)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Generate hash of text using various algorithms")
def hash_text(text: str, algorithm: str = "md5") -> Dict:
    """Generate hash of input text using specified algorithm."""
    try:
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }

        if algorithm.lower() not in algorithms:
            return {
                "success": False,
                "error": f"Unsupported algorithm. Use: {', '.join(algorithms.keys())}"
            }

        hash_func = algorithms[algorithm.lower()]
        hash_value = hash_func(text.encode()).hexdigest()

        return {
            "success": True,
            "original_text": text[:50] + "..." if len(text) > 50 else text,
            "algorithm": algorithm.upper(),
            "hash": hash_value,
            "length": len(hash_value)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def check_password_strength_internal(password: str) -> str:
    """Internal function to check password strength."""
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 3:
        return "Medium"
    elif score <= 4:
        return "Strong"
    else:
        return "Very Strong"


if __name__ == "__main__":
    print(f"🚀 Starting {mcp.name}...")
    mcp.run(transport="stdio")
