import json
import collections
import argparse
import random
import numpy as np
import requests
import re

def your_netid():
    # TODO: replace with your NYU NetID
    YOUR_NET_ID = 'rg4930'
    return YOUR_NET_ID

def your_hf_token():
    # TODO: replace with your Hugging Face token
    YOUR_HF_TOKEN = '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'
    return YOUR_HF_TOKEN

def your_prompt():
    """
    Few-shot prompt with consistent 'Question/Answer' formatting.
    Covers 1–7 digit additions so the model learns carry behavior.
    The actual test input will be inserted between prefix and suffix.
    """
    prefix = (
        "You are a calculator. Output only the final integer.\n"
        "Question: what is 7+5?\nAnswer: 12\n"
        "Question: what is 98+17?\nAnswer: 115\n"
        "Question: what is 1234+9876?\nAnswer: 11110\n"
        "Question: what is 56001+44009?\nAnswer: 100010\n"
        "Question: what is 123456+654321?\nAnswer: 777777\n"
        "Question: what is 1234567+2345678?\nAnswer: 3580245\n"
        "Question: what is "
    )
    suffix = "?\nAnswer: "
    return prefix, suffix

def your_config():
    """
    Use neutral temperature (=1.0). We keep required keys only.
    This avoids the ValueError while remaining deterministic
    (HF defaults to greedy when do_sample is not set).
    """
    return {
        'max_tokens': 50,
        'temperature': 1.0,      # was 0.0 → set to a strictly positive neutral value
        'top_k': 50,
        'top_p': 1.0,
        'repetition_penalty': 1.0,
        'stop': []
    }


def your_pre_processing(s):
    # Light cleanup only; no arithmetic.
    return s.strip()

def your_post_processing(output_string):
    """
    Extract the first integer that appears immediately after 'Answer:'.
    No arithmetic performed. Falls back to the first integer anywhere.
    """
    m = re.search(r"Answer:\s*([0-9]+)", output_string)
    if not m:
        m = re.search(r"([0-9]+)", output_string)  # fallback
    try:
        return int(m.group(1)) if m else 0
    except Exception:
        return 0
