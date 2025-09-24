#!/usr/bin/env python3
"""
🚀 Advanced Traffic Generator for Myntra
==================================================
Professional-grade traffic simulation with anti-tracking features
Author: Bhikan Deshmukh
Version: 5.0
"""

# ============================================================================
# 📦 IMPORTS & DEPENDENCIES
# ============================================================================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  # Not needed in newer versions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import time
import csv
import json
import pandas as pd
import os
import logging
import warnings
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Redirect stderr to null at the system level
import io

# Suppress specific Chrome warnings
import subprocess
import contextlib
import threading

# ============================================================================
# ⚙️ CONFIGURATION SETTINGS
# ============================================================================

# === BASIC CONFIG ===
TARGET_URLS = []  # Multiple URLs support
TOTAL_VISITS = 1000
BATCH_SIZE = 10 # Increased for faster processing
DELAY_BETWEEN_BATCHES = 0.1  # Reduced delay
VISIT_LOG_FILE = "visit_log.csv"
COOKIES_FILE = "session_cookies.json"
HEADLESS_MODE = True #(True/False)
MAX_RETRIES = 3
ENABLE_ANALYTICS = True

# === NEW ADVANCED CONFIG ===
ENABLE_INTERACTIVE_MENU = True
ENABLE_MULTIPLE_URLS = True
ENABLE_CUSTOM_TIMING = True
ENABLE_ADVANCED_HUMAN_BEHAVIOR = True
ENABLE_MOBILE_FOCUS = True
ENABLE_SHOPPING_ACTIONS = True

# === NETHUNTER/ANDROID CONFIG ===
ENABLE_NETHUNTER_MODE = False  # Set to True for NetHunter
ANDROID_CHROME_PATH = "/data/data/com.android.chrome/app_chrome/chrome"  # Android Chrome path
NETHUNTER_CHROME_PATH = "/usr/bin/google-chrome"  # NetHunter Chrome path
ENABLE_LOW_RESOURCE_MODE = False  # For limited Android resources

# === ADVANCED FEATURES ===
ENABLE_MULTI_PAGE_NAVIGATION = False  # Disabled for faster processing
ENABLE_SEARCH_SIMULATION = True
ENABLE_CATEGORY_BROWSING = True
SIMULATE_RETURN_VISITS = True
PAGE_VIEWS_PER_SESSION = (1, 1)  # Min, Max pages per session (REDUCED for speed)

# === PRIVACY & ANTI-TRACKING ===
ENABLE_IP_ROTATION = True
ENABLE_FINGERPRINT_RANDOMIZATION = True
CLEAR_COOKIES_FREQUENCY = 10
ROTATE_SESSION_FREQUENCY = 10
ENABLE_CANVAS_FINGERPRINT_PROTECTION = True
ENABLE_WEBGL_FINGERPRINT_PROTECTION = True

# === PEAK HOURS ===
PEAK_HOURS = [(9, 11), (14, 16), (19, 22)]  # Morning, afternoon, evening

# ============================================================================
# 📱 DEVICE & BROWSER DATA
# ============================================================================

# === VIEWPORT SIZES ===
VIEWPORT_SIZES = [
    (1920, 1080),  # Desktop FHD
    (1366, 768),   # Laptop
    (1440, 900),   # MacBook
    (375, 812),    # iPhone X
    (414, 896),    # iPhone XR
    (360, 640),    # Android
    (768, 1024),   # iPad Portrait
    (1024, 768),   # iPad Landscape
]

# === MOBILE-FOCUSED VIEWPORTS ===
MOBILE_VIEWPORT_SIZES = [
    (375, 812),    # iPhone X/XS
    (414, 896),    # iPhone XR/11
    (390, 844),    # iPhone 12/13
    (428, 926),    # iPhone 12/13 Pro Max
    (360, 640),    # Samsung Galaxy S8
    (412, 869),    # Samsung Galaxy S20
    (384, 854),    # Samsung Galaxy S21
    (375, 667),    # iPhone 6/7/8
    (414, 736),    # iPhone 6/7/8 Plus
    (320, 568),    # iPhone 5/SE
    (768, 1024),   # iPad
    (820, 1180),   # iPad Air
    (1024, 1366),  # iPad Pro
]

# === MOBILE USER AGENTS (Enhanced) ===
MOBILE_USER_AGENTS = [
    # iPhone iOS 16-17
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.99 Mobile/15E148 Safari/604.1",
    
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; RMX3471) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
]

# === USER AGENTS ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.136 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.64 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A715F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Linux; Android 10; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.79 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; RMX3471) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/115.0.1901.183 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Mi A3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Infinix X6816) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
]

# === CUSTOM HEADERS ===
CUSTOM_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0"
}

# ============================================================================
# 🌍 GEOLOCATION DATA - 100+ INDIAN CITIES
# ============================================================================

LOCATIONS = [
    # === TIER 1 CITIES (Metro Cities) ===
    {"latitude": 28.6139, "longitude": 77.2090, "city": "Delhi"},
    {"latitude": 19.0760, "longitude": 72.8777, "city": "Mumbai"},
    {"latitude": 12.9716, "longitude": 77.5946, "city": "Bangalore"},
    {"latitude": 22.5726, "longitude": 88.3639, "city": "Kolkata"},
    {"latitude": 13.0827, "longitude": 80.2707, "city": "Chennai"},
    {"latitude": 17.3850, "longitude": 78.4867, "city": "Hyderabad"},
    {"latitude": 23.0225, "longitude": 72.5714, "city": "Ahmedabad"},
    {"latitude": 18.5204, "longitude": 73.8567, "city": "Pune"},
    
    # === TIER 2 CITIES (Major Cities) ===
    {"latitude": 26.9124, "longitude": 75.7873, "city": "Jaipur"},
    {"latitude": 21.1458, "longitude": 79.0882, "city": "Nagpur"},
    {"latitude": 26.8467, "longitude": 80.9462, "city": "Lucknow"},
    {"latitude": 30.7333, "longitude": 76.7794, "city": "Chandigarh"},
    {"latitude": 25.5941, "longitude": 85.1376, "city": "Patna"},
    {"latitude": 23.2599, "longitude": 77.4126, "city": "Bhopal"},
    {"latitude": 21.2787, "longitude": 81.8661, "city": "Raipur"},
    {"latitude": 19.9975, "longitude": 73.7898, "city": "Nashik"},
    {"latitude": 22.3072, "longitude": 73.1812, "city": "Vadodara"},
    {"latitude": 21.1702, "longitude": 72.8311, "city": "Surat"},
    {"latitude": 11.0168, "longitude": 76.9558, "city": "Coimbatore"},
    {"latitude": 8.5241, "longitude": 76.9366, "city": "Trivandrum"},
    {"latitude": 9.9312, "longitude": 76.2673, "city": "Kochi"},
    {"latitude": 20.2961, "longitude": 85.8245, "city": "Bhubaneswar"},
    {"latitude": 18.1124, "longitude": 79.0193, "city": "Warangal"},
    {"latitude": 16.5062, "longitude": 80.6480, "city": "Vijayawada"},
    {"latitude": 13.6288, "longitude": 79.4192, "city": "Tirupati"},
    {"latitude": 11.1271, "longitude": 78.6569, "city": "Salem"},
    {"latitude": 10.7905, "longitude": 78.7047, "city": "Trichy"},
    {"latitude": 22.7196, "longitude": 75.8577, "city": "Indore"},
    {"latitude": 15.2993, "longitude": 74.1240, "city": "Panaji"},
    {"latitude": 17.6868, "longitude": 83.2185, "city": "Visakhapatnam"},
    {"latitude": 12.2958, "longitude": 76.6394, "city": "Mysore"},
    {"latitude": 15.3173, "longitude": 75.7139, "city": "Hubli"},
    {"latitude": 28.4595, "longitude": 77.0266, "city": "Gurgaon"},
    {"latitude": 28.5355, "longitude": 77.3910, "city": "Noida"},
    {"latitude": 19.2183, "longitude": 72.9781, "city": "Navi Mumbai"},
    {"latitude": 18.6298, "longitude": 73.7997, "city": "Lonavala"},
    {"latitude": 14.4426, "longitude": 79.9865, "city": "Nellore"},
    {"latitude": 24.5854, "longitude": 73.7125, "city": "Udaipur"},
    {"latitude": 27.0238, "longitude": 74.2179, "city": "Ajmer"},
    
    # === TIER 3 CITIES (Important Cities) ===
    {"latitude": 25.3176, "longitude": 82.9739, "city": "Varanasi"},
    {"latitude": 26.4499, "longitude": 80.3319, "city": "Kanpur"},
    {"latitude": 28.0229, "longitude": 73.3119, "city": "Bikaner"},
    {"latitude": 27.5530, "longitude": 76.6346, "city": "Alwar"},
    {"latitude": 24.8887, "longitude": 74.6269, "city": "Bhilwara"},
    {"latitude": 25.0961, "longitude": 85.3131, "city": "Gaya"},
    {"latitude": 26.2183, "longitude": 78.1828, "city": "Gwalior"},
    {"latitude": 25.4484, "longitude": 78.5685, "city": "Jhansi"},
    {"latitude": 27.8974, "longitude": 78.0880, "city": "Aligarh"},
    {"latitude": 28.8386, "longitude": 78.7733, "city": "Moradabad"},
    {"latitude": 29.3919, "longitude": 79.4663, "city": "Nainital"},
    {"latitude": 30.0668, "longitude": 79.0193, "city": "Rishikesh"},
    {"latitude": 30.3165, "longitude": 78.0322, "city": "Dehradun"},
    {"latitude": 31.1048, "longitude": 77.1734, "city": "Shimla"},
    {"latitude": 32.2432, "longitude": 77.1892, "city": "Dharamshala"},
    {"latitude": 34.0837, "longitude": 74.7973, "city": "Srinagar"},
    {"latitude": 32.7266, "longitude": 74.8570, "city": "Jammu"},
    {"latitude": 31.6340, "longitude": 74.8723, "city": "Amritsar"},
    {"latitude": 30.9010, "longitude": 75.8573, "city": "Ludhiana"},
    {"latitude": 31.3260, "longitude": 75.5762, "city": "Jalandhar"},
    {"latitude": 30.3398, "longitude": 76.3869, "city": "Patiala"},
    {"latitude": 29.9457, "longitude": 76.8178, "city": "Kurukshetra"},
    {"latitude": 28.4089, "longitude": 77.3178, "city": "Faridabad"},
    {"latitude": 28.6692, "longitude": 77.4538, "city": "Ghaziabad"},
    {"latitude": 28.9845, "longitude": 77.7064, "city": "Meerut"},
    {"latitude": 27.1767, "longitude": 78.0081, "city": "Agra"},
    {"latitude": 26.8393, "longitude": 75.8023, "city": "Jodhpur"},
    {"latitude": 25.2138, "longitude": 75.8648, "city": "Kota"},
    {"latitude": 24.2048, "longitude": 76.4951, "city": "Chittorgarh"},
    {"latitude": 27.3239, "longitude": 73.0430, "city": "Barmer"},
    {"latitude": 28.0180, "longitude": 73.3119, "city": "Bikaner"},
    
    # === TIER 4 CITIES (Emerging Cities) ===
    {"latitude": 23.8315, "longitude": 91.2868, "city": "Agartala"},
    {"latitude": 26.1445, "longitude": 91.7362, "city": "Guwahati"},
    {"latitude": 25.5788, "longitude": 91.8933, "city": "Shillong"},
    {"latitude": 23.1645, "longitude": 92.9376, "city": "Aizawl"},
    {"latitude": 27.0844, "longitude": 95.0944, "city": "Dibrugarh"},
    {"latitude": 26.7509, "longitude": 94.2037, "city": "Jorhat"},
    {"latitude": 27.4728, "longitude": 95.3269, "city": "Tinsukia"},
    {"latitude": 25.8070, "longitude": 93.9443, "city": "Imphal"},
    {"latitude": 25.6751, "longitude": 94.1086, "city": "Kohima"},
    {"latitude": 27.3314, "longitude": 88.6138, "city": "Gangtok"},
    {"latitude": 23.3441, "longitude": 85.3096, "city": "Ranchi"},
    {"latitude": 22.8046, "longitude": 86.2029, "city": "Jamshedpur"},
    {"latitude": 23.6693, "longitude": 86.1511, "city": "Dhanbad"},
    {"latitude": 24.6340, "longitude": 84.9984, "city": "Hazaribagh"},
    {"latitude": 24.7914, "longitude": 85.0002, "city": "Bokaro"},
    {"latitude": 21.2514, "longitude": 81.6296, "city": "Raipur"},
    {"latitude": 22.0797, "longitude": 82.1391, "city": "Bilaspur"},
    {"latitude": 21.1938, "longitude": 79.0728, "city": "Nagpur"},
    {"latitude": 20.9320, "longitude": 77.7523, "city": "Akola"},
    {"latitude": 19.7515, "longitude": 75.7139, "city": "Aurangabad"},
    {"latitude": 18.8973, "longitude": 72.8379, "city": "Thane"},
    {"latitude": 19.2183, "longitude": 72.9781, "city": "Navi Mumbai"},
    {"latitude": 18.1124, "longitude": 79.0193, "city": "Warangal"},
    {"latitude": 17.9689, "longitude": 79.5957, "city": "Khammam"},
    {"latitude": 18.4386, "longitude": 79.1288, "city": "Karimnagar"},
    {"latitude": 16.5062, "longitude": 80.6480, "city": "Vijayawada"},
    {"latitude": 15.8281, "longitude": 78.0373, "city": "Kurnool"},
    {"latitude": 14.4426, "longitude": 79.9865, "city": "Nellore"},
    {"latitude": 13.6288, "longitude": 79.4192, "city": "Tirupati"},
    {"latitude": 14.9140, "longitude": 79.9865, "city": "Kadapa"},
    {"latitude": 15.4909, "longitude": 78.8242, "city": "Anantapur"},
    {"latitude": 16.2160, "longitude": 77.3566, "city": "Bellary"},
    {"latitude": 15.3647, "longitude": 76.4600, "city": "Raichur"},
    {"latitude": 14.6819, "longitude": 77.5985, "city": "Chitradurga"},
    {"latitude": 13.3379, "longitude": 77.1186, "city": "Tumkur"},
    {"latitude": 12.9719, "longitude": 77.5937, "city": "Bangalore Rural"},
    {"latitude": 12.2958, "longitude": 76.6394, "city": "Mysore"},
    {"latitude": 11.8745, "longitude": 75.3704, "city": "Kannur"},
    {"latitude": 11.2588, "longitude": 75.7804, "city": "Kozhikode"},
    {"latitude": 10.5276, "longitude": 76.2144, "city": "Thrissur"},
    {"latitude": 9.9312, "longitude": 76.2673, "city": "Kochi"},
    {"latitude": 8.8932, "longitude": 76.6141, "city": "Kollam"},
    {"latitude": 8.5241, "longitude": 76.9366, "city": "Trivandrum"},
    {"latitude": 11.9416, "longitude": 79.8083, "city": "Pondicherry"},
    {"latitude": 11.3410, "longitude": 77.7172, "city": "Erode"},
    {"latitude": 10.7867, "longitude": 79.1378, "city": "Thanjavur"},
    {"latitude": 9.9252, "longitude": 78.1198, "city": "Madurai"},
    {"latitude": 8.7642, "longitude": 78.1348, "city": "Tirunelveli"},
    {"latitude": 8.0883, "longitude": 77.5385, "city": "Kanyakumari"},
    {"latitude": 12.9165, "longitude": 79.1325, "city": "Vellore"},
    {"latitude": 13.0878, "longitude": 80.2785, "city": "Chennai"},
    {"latitude": 11.1271, "longitude": 78.6569, "city": "Salem"},
    {"latitude": 10.7905, "longitude": 78.7047, "city": "Trichy"},
    {"latitude": 11.9416, "longitude": 79.8083, "city": "Cuddalore"},
    {"latitude": 12.5266, "longitude": 78.2150, "city": "Hosur"},
    {"latitude": 13.3379, "longitude": 77.1186, "city": "Tumkur"},
    {"latitude": 14.4673, "longitude": 75.9218, "city": "Shimoga"},
    {"latitude": 15.8497, "longitude": 74.4977, "city": "Belgaum"},
    {"latitude": 16.8302, "longitude": 74.7442, "city": "Kolhapur"},
    {"latitude": 17.6599, "longitude": 75.9064, "city": "Solapur"},
    {"latitude": 19.8762, "longitude": 75.3433, "city": "Jalna"},
    {"latitude": 20.7050, "longitude": 78.1288, "city": "Chandrapur"},
    {"latitude": 21.7679, "longitude": 72.1519, "city": "Bharuch"},
    {"latitude": 22.5645, "longitude": 72.9289, "city": "Anand"},
    {"latitude": 23.7957, "longitude": 72.4131, "city": "Mehsana"},
    {"latitude": 24.1752, "longitude": 72.6397, "city": "Patan"},
    {"latitude": 23.0225, "longitude": 72.5714, "city": "Ahmedabad"},
    {"latitude": 21.7679, "longitude": 72.1519, "city": "Bharuch"},
    {"latitude": 22.4707, "longitude": 70.0577, "city": "Rajkot"},
    {"latitude": 21.5222, "longitude": 70.4579, "city": "Jamnagar"},
    {"latitude": 22.2587, "longitude": 71.1924, "city": "Morbi"},
    {"latitude": 23.0395, "longitude": 70.1066, "city": "Bhuj"},
]

# ============================================================================
# 🔗 REFERRER & TRAFFIC SOURCES
# ============================================================================

REFERRERS = [
    # === SEARCH ENGINES ===
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://search.yahoo.com/",
    "https://duckduckgo.com/",
    "https://www.google.co.in/",
    "https://www.google.com/search?q=women+kurta",
    "https://www.google.com/search?q=ethnic+wear",
    "https://www.google.com/search?q=flared+kurta",
    "https://www.bing.com/search?q=traditional+dress",
    
    # === SOCIAL MEDIA ===
    "https://www.facebook.com/",    
    "https://www.instagram.com/",    
    "https://twitter.com/",
    "https://www.linkedin.com/",
    "https://www.pinterest.com/",
    "https://www.reddit.com/",
    "https://www.tumblr.com/",
    "https://www.snapchat.com/",
    "https://www.tiktok.com/",
    "https://www.youtube.com/",
    "https://web.whatsapp.com/",
    "https://telegram.org/",
    
    # === FASHION BLOGS & MAGAZINES ===
    "https://www.vogue.in/",
    "https://www.elle.in/",
    "https://www.cosmopolitan.in/",
    "https://www.femina.in/",
    "https://www.grazia.co.in/",
    "https://www.harpersbazaar.in/",
    "https://www.marieclaire.in/",
    "https://www.popxo.com/",
    "https://www.bewakoof.com/",
    "https://www.stylecraze.com/",
    
    # === NEWS & LIFESTYLE ===
    "https://www.nytimes.com/",
    "https://www.bbc.com/",
    "https://www.cnn.com/",
    "https://www.hindustantimes.com/",
    "https://www.timesofindia.com/",
    "https://www.ndtv.com/",
    "https://www.indianexpress.com/",
    "https://www.news18.com/",
    "https://www.zee5.com/",
    "https://www.hotstar.com/",
    
    # === TECH & FORUMS ===
    "https://www.quora.com/",
    "https://www.medium.com/",
    "https://www.reddit.com/r/IndianFashionAdvice/",
    "https://www.reddit.com/r/india/",
    "https://news.ycombinator.com/",
    "https://www.producthunt.com/",
    "https://www.stackoverflow.com/",
    "https://github.com/",
    
    # === EMAIL & DIRECT ===
    "https://mail.google.com/",
    "https://outlook.live.com/",
]

# ============================================================================
# 📄 PAGE VIEW & NAVIGATION DATA
# ============================================================================

# === SEARCH QUERIES ===
SEARCH_QUERIES = [
    "women kurta",
    "flared kurta",
    "ethnic wear",
    "indian dress",
    "traditional wear",
    "designer kurta",
    "cotton kurta",
    "party wear kurta",
    "casual kurta",
    "office wear kurta"
]

# === ADDITIONAL PAGES ===
ADDITIONAL_PAGES = [
    "/kurtas",
    "/women-ethnic-wear",
    "/women-kurtas-kurtis",
    "/ethnic-wear",
    "/women-clothing",
    "/kurtas-kurtis",
    "/straight-kurtas",
    "/anarkali-kurtas",
    "/a-line-kurtas"
]

# === CATEGORY PAGES ===
CATEGORY_PAGES = [
    "https://www.myntra.com/kurtas",
    "https://www.myntra.com/women-ethnic-wear",
    "https://www.myntra.com/women-kurtas-kurtis",
    "https://www.myntra.com/straight-kurtas",
    "https://www.myntra.com/anarkali-kurtas",
    "https://www.myntra.com/a-line-kurtas",
    "https://www.myntra.com/ethnic-wear",
    "https://www.myntra.com/women-clothing"
]

# ============================================================================
# 🛠️ UTILITY FUNCTIONS
# ============================================================================

def is_peak_time():
    """Check if current time is in peak hours"""
    current_hour = datetime.now().hour
    return any(start <= current_hour <= end for start, end in PEAK_HOURS)

def save_cookies(driver, filename):
    """Save browser cookies to file"""
    try:
        with open(filename, 'w') as file:
            json.dump(driver.get_cookies(), file)
    except Exception:
        pass

def load_cookies(driver, filename):
    """Load cookies from file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
    except Exception:
        pass

def cleanup_old_sessions():
    """Clean up old session files"""
    try:
        if os.path.exists(COOKIES_FILE):
            file_age = time.time() - os.path.getmtime(COOKIES_FILE)
            if file_age > 3600:  # 1 hour
                os.remove(COOKIES_FILE)
                print("🧹 Cleaned up old session cookies")
    except Exception:
        pass

# ============================================================================
# 🔇 LOG SUPPRESSION & ENVIRONMENT SETUP
# ============================================================================

def detect_nethunter_environment():
    """Detect if running on NetHunter/Android"""
    global ENABLE_NETHUNTER_MODE, ENABLE_LOW_RESOURCE_MODE, HEADLESS_MODE, BATCH_SIZE
    
    # Check for NetHunter/Android environment
    is_nethunter = False
    is_android = False
    
    try:
        # Check for Android system properties
        if os.path.exists('/system/build.prop') or os.path.exists('/system/bin/getprop'):
            is_android = True
            print("🤖 Android environment detected!")
            
        # Check for NetHunter specific paths
        if os.path.exists('/usr/share/kali-nethunter') or os.path.exists('/system/xbin/kali'):
            is_nethunter = True
            print("🗡️  NetHunter Kali Linux detected!")
            
        # Check for Termux
        if 'TERMUX' in os.environ or os.path.exists('/data/data/com.termux'):
            print("📱 Termux environment detected!")
            is_android = True
            
        # Auto-configure for mobile environment
        if is_android or is_nethunter:
            ENABLE_NETHUNTER_MODE = True
            ENABLE_LOW_RESOURCE_MODE = True
            HEADLESS_MODE = True  # Force headless on mobile
            BATCH_SIZE = min(BATCH_SIZE, 10)  # Reduce batch size
            ENABLE_MOBILE_FOCUS = True
            print("⚙️  Auto-configured for mobile environment")
            print(f"   - Headless mode: ON")
            print(f"   - Batch size: {BATCH_SIZE}")
            print(f"   - Low resource mode: ON")
            
    except Exception as e:
        print(f"🔍 Environment detection error: {e}")
    
    return is_nethunter, is_android

def get_chrome_binary_path():
    """Get correct Chrome binary path for different environments"""
    
    # Try common Chrome paths for Linux/NetHunter
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable", 
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/opt/google/chrome/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
        "/data/data/com.android.chrome/app_chrome/chrome",  # Android
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"🌐 Found Chrome at: {path}")
            return path
    
    print("⚠️  Chrome binary not found, using system default")
    return None

def optimize_for_mobile():
    """Optimize settings for mobile/low resource environment"""
    global DELAY_BETWEEN_BATCHES, PAGE_VIEWS_PER_SESSION, CLEAR_COOKIES_FREQUENCY
    
    if ENABLE_LOW_RESOURCE_MODE:
        DELAY_BETWEEN_BATCHES = max(DELAY_BETWEEN_BATCHES, 1.0)  # Increase delay
        PAGE_VIEWS_PER_SESSION = (1, 2)  # Reduce page views
        CLEAR_COOKIES_FREQUENCY = max(CLEAR_COOKIES_FREQUENCY, 5)  # More frequent cleanup
        
        print("📱 Mobile optimization applied:")
        print(f"   - Increased delay: {DELAY_BETWEEN_BATCHES}s")
        print(f"   - Reduced page views: {PAGE_VIEWS_PER_SESSION}")
        print(f"   - More frequent cleanup: every {CLEAR_COOKIES_FREQUENCY} visits")

def get_target_url():
    """Get target URL from user input"""
    global TARGET_URLS
    print("🎯 MYNTRA TRAFFIC GENERATOR v6.0")
    print("=" * 50)
    
    if ENABLE_MULTIPLE_URLS:
        print("📋 MULTIPLE URLs MODE")
        print("Enter URLs one by one (press Enter without URL to finish):")
        url_count = 1
        while True:
            url = input(f"URL {url_count}: ").strip()
            if not url:
                break
            if not url.startswith('http'):
                url = 'https://' + url
            TARGET_URLS.append(url)
            print(f"✅ Added: {url}")
            url_count += 1
        
        if not TARGET_URLS:
            print("❌ No URLs entered! Adding default...")
            TARGET_URLS.append("https://www.myntra.com")
    else:
        url = input("Enter the target Myntra URL: ").strip()
        if url:
            if not url.startswith('http'):
                url = 'https://' + url
            TARGET_URLS.append(url)
        else:
            TARGET_URLS.append("https://www.myntra.com")
    
    print(f"🎯 Total URLs configured: {len(TARGET_URLS)}")
    for i, url in enumerate(TARGET_URLS, 1):
        print(f"   {i}. {url}")
    print("=" * 50 + "\n")

def interactive_menu():
    """Interactive configuration menu"""
    global TOTAL_VISITS, BATCH_SIZE, HEADLESS_MODE, DELAY_BETWEEN_BATCHES
    global ENABLE_MULTI_PAGE_NAVIGATION, ENABLE_MOBILE_FOCUS
    
    if not ENABLE_INTERACTIVE_MENU:
        return
    
    print("⚙️  CONFIGURATION MENU")
    print("=" * 40)
    
    while True:
        print("\n🔧 Current Settings:")
        print(f"1. Total Visits: {TOTAL_VISITS}")
        print(f"2. Batch Size: {BATCH_SIZE}")
        print(f"3. Headless Mode: {'ON' if HEADLESS_MODE else 'OFF'}")
        print(f"4. Delay Between Batches: {DELAY_BETWEEN_BATCHES}s")
        print(f"5. Multi-page Navigation: {'ON' if ENABLE_MULTI_PAGE_NAVIGATION else 'OFF'}")
        print(f"6. Mobile Focus: {'ON' if ENABLE_MOBILE_FOCUS else 'OFF'}")
        print("7. Start Traffic Generation")
        print("0. Exit")
        
        choice = input("\n📝 Select option (0-7): ").strip()
        
        if choice == '1':
            try:
                visits = int(input(f"Enter total visits (current: {TOTAL_VISITS}): "))
                TOTAL_VISITS = max(1, visits)
                print(f"✅ Total visits set to: {TOTAL_VISITS}")
            except ValueError:
                print("❌ Invalid number!")
        
        elif choice == '2':
            try:
                batch = int(input(f"Enter batch size (current: {BATCH_SIZE}): "))
                BATCH_SIZE = max(1, min(100, batch))
                print(f"✅ Batch size set to: {BATCH_SIZE}")
            except ValueError:
                print("❌ Invalid number!")
        
        elif choice == '3':
            HEADLESS_MODE = not HEADLESS_MODE
            print(f"✅ Headless mode: {'ON' if HEADLESS_MODE else 'OFF'}")
        
        elif choice == '4':
            try:
                delay = float(input(f"Enter delay in seconds (current: {DELAY_BETWEEN_BATCHES}): "))
                DELAY_BETWEEN_BATCHES = max(0, delay)
                print(f"✅ Delay set to: {DELAY_BETWEEN_BATCHES}s")
            except ValueError:
                print("❌ Invalid number!")
        
        elif choice == '5':
            ENABLE_MULTI_PAGE_NAVIGATION = not ENABLE_MULTI_PAGE_NAVIGATION
            print(f"✅ Multi-page navigation: {'ON' if ENABLE_MULTI_PAGE_NAVIGATION else 'OFF'}")
        
        elif choice == '6':
            ENABLE_MOBILE_FOCUS = not ENABLE_MOBILE_FOCUS
            print(f"✅ Mobile focus: {'ON' if ENABLE_MOBILE_FOCUS else 'OFF'}")
        
        elif choice == '7':
            print("🚀 Starting traffic generation...")
            break
        
        elif choice == '0':
            print("👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid option!")
    
    print("=" * 40 + "\n")

def schedule_traffic():
    """Custom timing and scheduling"""
    if not ENABLE_CUSTOM_TIMING:
        return False
    
    print("⏰ TRAFFIC SCHEDULING")
    print("=" * 30)
    print("1. Start immediately")
    print("2. Schedule for specific time")
    print("3. Run during peak hours only")
    
    choice = input("Select timing option (1-3): ").strip()
    
    if choice == '2':
        try:
            hour = int(input("Enter hour (0-23): "))
            minute = int(input("Enter minute (0-59): "))
            
            target_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            if target_time <= datetime.now():
                target_time += pd.Timedelta(days=1)
            
            wait_seconds = (target_time - datetime.now()).total_seconds()
            print(f"⏳ Scheduled for {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"💤 Waiting {wait_seconds/60:.1f} minutes...")
            
            time.sleep(wait_seconds)
            return True
            
        except ValueError:
            print("❌ Invalid time format!")
            return False
    
    elif choice == '3':
        print("⏰ Peak hours mode activated (9-11, 14-16, 19-22)")
        while not is_peak_time():
            print(f"⏳ Waiting for peak hours... Current time: {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(5)  # Check every 5 seconds
        return True
    
    return True

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)

# Environment variables for complete log suppression
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['CHROME_LOG_FILE'] = 'NUL' if os.name == 'nt' else '/dev/null'
os.environ['CHROME_HEADLESS'] = '1'
os.environ['DISPLAY'] = ':99' if os.name != 'nt' else ''

# Additional Chrome log suppression
os.environ['GOOGLE_API_KEY'] = ''
os.environ['GOOGLE_DEFAULT_CLIENT_ID'] = ''
os.environ['GOOGLE_DEFAULT_CLIENT_SECRET'] = ''
os.environ['CHROME_DEVEL_SANDBOX'] = ''
os.environ['CHROME_LOG_LEVEL'] = '3'

# Suppress specific Chrome/Chromium logs
os.environ['GLOG_minloglevel'] = '3'
os.environ['GLOG_v'] = '0'
os.environ['GLOG_logtostderr'] = '0'
os.environ['GLOG_log_dir'] = os.devnull

# Create a custom stderr that discards everything
class NullWriter:
    def write(self, txt):
        pass
    def flush(self):
        pass

# Apply global stderr suppression for Chrome logs
original_stderr = sys.stderr

# Only suppress stderr during script execution, not during imports
def suppress_chrome_logs():
    """Suppress Chrome logs by redirecting stderr"""
    sys.stderr = NullWriter()

def restore_stderr():
    """Restore original stderr"""
    sys.stderr = original_stderr

# Don't suppress during imports - only during execution
# suppress_chrome_logs()



# Global stderr suppression for Chrome logs - DISABLED
# def suppress_chrome_logs():
#     """Permanently redirect stderr to suppress Chrome logs"""
#     try:
#         # Redirect stderr to null
#         sys.stderr = open(os.devnull, 'w')
#     except Exception:
#         pass

# Apply global suppression at import time - DISABLED
# suppress_chrome_logs()

# Redirect stderr to suppress Chrome logs
@contextlib.contextmanager
def suppress_stderr():
    """Context manager for additional stderr suppression"""
    try:
        with open(os.devnull, "w") as devnull:
            old_stderr = sys.stderr
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stderr = old_stderr
    except Exception:
        yield

class SuppressOutput:
    """Simple context manager that doesn't interfere with threading"""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# ============================================================================
# 🎭 BROWSER FINGERPRINTING & ANTI-TRACKING
# ============================================================================

def set_geolocation(driver, location):
    """Set browser geolocation"""
    try:
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "accuracy": random.randint(1, 100)
        })
    except Exception:
        pass

def randomize_browser_fingerprint(driver):
    """Randomize browser fingerprint to avoid tracking"""
    if not ENABLE_FINGERPRINT_RANDOMIZATION:
        return
    
    try:
        # Randomize screen resolution
        screen_width = random.choice([1920, 1366, 1440, 1536, 1600])
        screen_height = random.choice([1080, 768, 900, 864, 900])
        
        # Randomize timezone
        timezones = [
            "Asia/Kolkata", "Asia/Mumbai", "Asia/Delhi", "Asia/Calcutta",
        ]
        timezone = random.choice(timezones)
        
        # Override screen properties
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": screen_width,
            "height": screen_height,
            "deviceScaleFactor": random.uniform(1.0, 2.0),
            "mobile": random.choice([True, False])
        })
        
        # Override timezone
        driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {
            "timezoneId": timezone
        })
        
        # Randomize language
        languages = ["en-US,en;q=0.9", "en-IN,en;q=0.9,hi;q=0.8", "en-GB,en;q=0.9"]
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": driver.execute_script("return navigator.userAgent"),
            "acceptLanguage": random.choice(languages),
            "platform": random.choice(["Win32", "MacIntel", "Linux x86_64"])
        })
        
    except Exception:
        pass

def simulate_ip_rotation_behavior(driver):
    """Simulate IP rotation behavior patterns"""
    if not ENABLE_IP_ROTATION:
        return
    
    try:
        # Simulate different connection speeds (IP-based behavior)
        driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": False,
            "downloadThroughput": random.randint(500000, 2000000),
            "uploadThroughput": random.randint(100000, 500000),
            "latency": random.randint(20, 200)
        })
        
        # Random DNS resolution delay (simulate different ISPs)
        time.sleep(random.uniform(0.1, 0.5))
        
    except Exception:
        pass

def clear_tracking_data(driver, visit_number):
    """Clear cookies and tracking data periodically"""
    try:
        # Clear cookies every N visits
        if visit_number % CLEAR_COOKIES_FREQUENCY == 0:
            driver.delete_all_cookies()
            print(f"🧹 Cleared cookies at visit {visit_number}")
        
        # Clear local storage and session storage
        if visit_number % (CLEAR_COOKIES_FREQUENCY * 2) == 0:
            driver.execute_script("localStorage.clear();")
            driver.execute_script("sessionStorage.clear();")
            print(f"🗑️ Cleared storage at visit {visit_number}")
            
    except Exception:
        pass

def inject_anti_fingerprinting_scripts(driver):
    """Inject scripts to prevent fingerprinting"""
    if not (ENABLE_CANVAS_FINGERPRINT_PROTECTION or ENABLE_WEBGL_FINGERPRINT_PROTECTION):
        return
    
    try:
        # Canvas fingerprinting protection
        if ENABLE_CANVAS_FINGERPRINT_PROTECTION:
            canvas_script = """
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function() {
                const context = this.getContext('2d');
                if (context) {
                    context.fillStyle = `rgb(${Math.floor(Math.random()*255)}, ${Math.floor(Math.random()*255)}, ${Math.floor(Math.random()*255)})`;
                    context.fillRect(0, 0, 1, 1);
                }
                return originalToDataURL.apply(this, arguments);
            };
            """
            driver.execute_script(canvas_script)
        
        # WebGL fingerprinting protection
        if ENABLE_WEBGL_FINGERPRINT_PROTECTION:
            webgl_script = """
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.'; // VENDOR
                if (parameter === 37446) return 'Intel(R) HD Graphics'; // RENDERER
                return originalGetParameter.apply(this, arguments);
            };
            """
            driver.execute_script(webgl_script)
            
    except Exception:
        pass

# ============================================================================
# 🛒 ADVANCED SHOPPING BEHAVIORS
# ============================================================================

def simulate_shopping_cart_actions(driver):
    """Simulate shopping cart interactions"""
    if not ENABLE_SHOPPING_ACTIONS:
        return False
    
    try:
        # Try to find size selection
        size_selectors = [
            ".size-buttons-size-button",
            ".pdp-size-select-size",
            ".size-button",
            "[data-testid='size-button']",
            ".sizeButton"
        ]
        
        for selector in size_selectors:
            try:
                size_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                if size_buttons:
                    size_button = random.choice(size_buttons)
                    if size_button.is_displayed() and size_button.is_enabled():
                        driver.execute_script("arguments[0].click();", size_button)
                        print("🔹 Selected size")
                        time.sleep(random.uniform(1, 2))
                        break
            except:
                continue
        
        # Try to add to bag/cart
        add_to_bag_selectors = [
            ".pdp-add-to-bag",
            ".btn-add-to-bag", 
            "[data-testid='add-to-bag']",
            ".add-to-bag-button",
            ".pdp-addToBag"
        ]
        
        for selector in add_to_bag_selectors:
            try:
                add_button = driver.find_element(By.CSS_SELECTOR, selector)
                if add_button.is_displayed() and add_button.is_enabled():
                    driver.execute_script("arguments[0].click();", add_button)
                    print("🛒 Added to bag")
                    time.sleep(random.uniform(2, 4))
                    return True
            except:
                continue
        
        # Try to add to wishlist
        wishlist_selectors = [
            ".pdp-wishlist-icon",
            ".wishlist-button",
            "[data-testid='wishlist']",
            ".pdp-save-for-later"
        ]
        
        for selector in wishlist_selectors:
            try:
                wishlist_button = driver.find_element(By.CSS_SELECTOR, selector)
                if wishlist_button.is_displayed() and wishlist_button.is_enabled():
                    driver.execute_script("arguments[0].click();", wishlist_button)
                    print("💖 Added to wishlist")
                    time.sleep(random.uniform(1, 3))
                    return True
            except:
                continue
                
        return False
        
    except Exception:
        return False

def simulate_product_exploration(driver):
    """Enhanced product page exploration"""
    if not ENABLE_ADVANCED_HUMAN_BEHAVIOR:
        return
    
    try:
        # Check product images
        image_selectors = [
            ".image-grid-image",
            ".pdp-image",
            ".product-image",
            "[data-testid='product-image']"
        ]
        
        for selector in image_selectors:
            try:
                images = driver.find_elements(By.CSS_SELECTOR, selector)
                if images and len(images) > 1:
                    # Click on different product images
                    image = random.choice(images[1:4])  # Skip main image
                    if image.is_displayed():
                        driver.execute_script("arguments[0].click();", image)
                        print("🖼️ Viewing product image")
                        time.sleep(random.uniform(2, 3))
                        break
            except:
                continue
        
        # Read product details
        detail_selectors = [
            ".pdp-product-details-content",
            ".product-details",
            ".pdp-productDescriptors",
            "[data-testid='product-details']"
        ]
        
        for selector in detail_selectors:
            try:
                details = driver.find_element(By.CSS_SELECTOR, selector)
                if details.is_displayed():
                    ActionChains(driver).move_to_element(details).perform()
                    print("📝 Reading product details")
                    time.sleep(random.uniform(3, 5))
                    break
            except:
                continue
        
        # Scroll to reviews section
        review_selectors = [
            ".user-review",
            ".pdp-userReview", 
            ".reviews-section",
            "[data-testid='reviews']"
        ]
        
        for selector in review_selectors:
            try:
                reviews = driver.find_element(By.CSS_SELECTOR, selector)
                if reviews.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView(true);", reviews)
                    print("⭐ Checking reviews")
                    time.sleep(random.uniform(4, 6))
                    break
            except:
                continue
                
    except Exception:
        pass

def mobile_specific_interactions(driver):
    """Mobile-specific touch and swipe behaviors"""
    if not ENABLE_MOBILE_FOCUS:
        return
    
    try:
        # Get window size to determine if mobile
        window_size = driver.get_window_size()
        if window_size['width'] > 768:  # Not mobile viewport
            return
        
        # Mobile swipe simulation (using scroll)
        swipe_directions = ['up', 'down', 'left', 'right']
        
        for _ in range(random.randint(3, 6)):
            direction = random.choice(swipe_directions)
            
            if direction == 'up':
                driver.execute_script("window.scrollBy(0, 200);")
            elif direction == 'down':
                driver.execute_script("window.scrollBy(0, -200);")
            elif direction == 'left':
                driver.execute_script("window.scrollBy(100, 0);")
            elif direction == 'right':
                driver.execute_script("window.scrollBy(-100, 0);")
            
            time.sleep(random.uniform(0.5, 1.0))
        
        # Mobile-specific element interactions
        try:
            # Try to expand mobile menu
            menu_selectors = [".hamburger-menu", ".mobile-menu", ".nav-toggle"]
            for selector in menu_selectors:
                try:
                    menu_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    if menu_btn.is_displayed():
                        menu_btn.click()
                        time.sleep(random.uniform(1, 2))
                        # Close menu
                        menu_btn.click()
                        break
                except:
                    continue
        except:
            pass
            
        print("📱 Mobile interactions simulated")
        
    except Exception:
        pass

# ============================================================================
# 📊 ADVANCED ANALYTICS & REAL-TIME DASHBOARD  
# ============================================================================

def create_real_time_dashboard():
    """Create real-time analytics dashboard"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        from datetime import timedelta
        
        if not os.path.exists(VISIT_LOG_FILE):
            return
        
        df = pd.read_csv(VISIT_LOG_FILE)
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('🚀 Myntra Traffic Generator - Real-Time Dashboard', fontsize=16)
        
        # 1. Success Rate Pie Chart
        success_counts = df['Status'].value_counts()
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        ax1.pie(success_counts.values, labels=success_counts.index, autopct='%1.1f%%', colors=colors)
        ax1.set_title('Success Rate Distribution')
        
        # 2. Traffic by Hour
        df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour
        hourly_traffic = df['Hour'].value_counts().sort_index()
        ax2.bar(hourly_traffic.index, hourly_traffic.values, color='#3498db')
        ax2.set_title('Traffic by Hour')
        ax2.set_xlabel('Hour')
        ax2.set_ylabel('Visits')
        
        # 3. Top Locations
        location_counts = df['Location'].value_counts().head(10)
        ax3.barh(location_counts.index, location_counts.values, color='#9b59b6')
        ax3.set_title('Top 10 Locations')
        ax3.set_xlabel('Visits')
        
        # 4. Traffic Timeline
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df_hourly = df.groupby(df['Timestamp'].dt.floor('H')).size()
        ax4.plot(df_hourly.index, df_hourly.values, marker='o', color='#e67e22')
        ax4.set_title('Traffic Timeline')
        ax4.set_xlabel('Time')
        ax4.set_ylabel('Visits per Hour')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('traffic_dashboard.png', dpi=300, bbox_inches='tight')
        print("📊 Dashboard saved as 'traffic_dashboard.png'")
        
    except ImportError:
        print("📊 Install matplotlib for dashboard: pip install matplotlib")
    except Exception as e:
        print(f"📊 Dashboard error: {str(e)}")

def generate_advanced_analytics():
    """Generate comprehensive analytics report"""
    if not ENABLE_ANALYTICS or not os.path.exists(VISIT_LOG_FILE):
        return
    
    try:
        df = pd.read_csv(VISIT_LOG_FILE)
        
        print("\n" + "="*70)
        print("📊 ADVANCED ANALYTICS REPORT")
        print("="*70)
        
        # Basic Stats
        total_visits = len(df)
        successful_visits = len(df[df['Status'] == 'Success'])
        success_rate = (successful_visits / total_visits) * 100 if total_visits > 0 else 0
        
        print(f"📈 PERFORMANCE METRICS:")
        print(f"   Total Visits: {total_visits:,}")
        print(f"   Successful Visits: {successful_visits:,}")
        print(f"   Success Rate: {success_rate:.2f}%")
        print(f"   Failed Visits: {total_visits - successful_visits:,}")
        
        if len(df) > 0:
            # Time Analysis
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Hour'] = df['Timestamp'].dt.hour
            df['DayOfWeek'] = df['Timestamp'].dt.day_name()
            
            print(f"\n⏰ TIME ANALYSIS:")
            peak_hour = df['Hour'].mode().iloc[0] if not df['Hour'].mode().empty else 'N/A'
            peak_day = df['DayOfWeek'].mode().iloc[0] if not df['DayOfWeek'].mode().empty else 'N/A'
            print(f"   Peak Hour: {peak_hour}:00")
            print(f"   Peak Day: {peak_day}")
            
            # Geographic Analysis
            print(f"\n🌍 GEOGRAPHIC DISTRIBUTION:")
            top_locations = df['Location'].value_counts().head(5)
            for i, (location, count) in enumerate(top_locations.items(), 1):
                percentage = (count / total_visits) * 100
                print(f"   {i}. {location}: {count} visits ({percentage:.1f}%)")
            
            # User Agent Analysis
            print(f"\n🌐 BROWSER ANALYSIS:")
            print(f"   Unique User Agents: {df['User-Agent'].nunique()}")
            
            # Referrer Analysis  
            print(f"\n🔗 TRAFFIC SOURCES:")
            top_referrers = df['Referrer'].value_counts().head(5)
            for i, (referrer, count) in enumerate(top_referrers.items(), 1):
                domain = referrer.split('//')[1].split('/')[0] if '//' in referrer else referrer[:30]
                percentage = (count / total_visits) * 100
                print(f"   {i}. {domain}: {count} visits ({percentage:.1f}%)")
            
            # Performance Trends
            print(f"\n📊 PERFORMANCE TRENDS:")
            recent_visits = df.tail(100) if len(df) >= 100 else df
            recent_success_rate = (len(recent_visits[recent_visits['Status'] == 'Success']) / len(recent_visits)) * 100
            print(f"   Recent Success Rate (last 100): {recent_success_rate:.2f}%")
            
            trend = "📈 Improving" if recent_success_rate > success_rate else "📉 Declining" if recent_success_rate < success_rate else "➡️ Stable"
            print(f"   Trend: {trend}")
        
        print("="*70 + "\n")
        
        # Generate dashboard
        create_real_time_dashboard()
        
    except Exception as e:
        print(f"Analytics error: {str(e)}")

# ============================================================================
# 🤖 ENHANCED HUMAN BEHAVIOR SIMULATION
# ============================================================================

def random_interactions(driver):
    """Perform random human-like interactions with error handling"""
    try:
        # Get window size for safe mouse movements
        window_size = driver.get_window_size()
        
        # Safe random mouse movements
        try:
            actions = ActionChains(driver)
            # Move to a safe position first
            actions.move_by_offset(100, 100)
            
            for _ in range(random.randint(1, 3)):
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-50, 50)
                actions.move_by_offset(x_offset, y_offset)
                time.sleep(random.uniform(0.2, 0.5))
            
            actions.perform()
        except Exception:
            pass
        
        # Safe keyboard events
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            keyboard_actions = [Keys.PAGE_DOWN, Keys.END]
            body.send_keys(random.choice(keyboard_actions))
            time.sleep(random.uniform(0.5, 1.0))
        except Exception:
            pass
        
        # Safe element hover
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "div:not([style*='display: none']), img, a")[:3]
            if elements:
                element = random.choice(elements)
                if element.is_displayed() and element.is_enabled():
                    ActionChains(driver).move_to_element(element).perform()
                    time.sleep(random.uniform(0.3, 0.5))
        except Exception:
            pass
            
    except Exception:
        pass

def random_scroll_and_interact(driver):
    """Random scrolling and interaction on any page"""
    try:
        # Random scrolling
        scroll_actions = random.randint(2, 5)
        for _ in range(scroll_actions):
            scroll_direction = random.choice(['down', 'up'])
            if scroll_direction == 'down':
                scroll_y = random.randint(200, 800)
                driver.execute_script(f"window.scrollBy(0, {scroll_y});")
            else:
                scroll_y = random.randint(-400, -100)
                driver.execute_script(f"window.scrollBy(0, {scroll_y});")
            
            time.sleep(random.uniform(0.5, 1))
        
        # Random interactions
        random_interactions(driver)
        
        # Random element hover
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "div, img, a")[:10]
            if elements:
                element = random.choice(elements)
                ActionChains(driver).move_to_element(element).perform()
                time.sleep(random.uniform(0.5, 1))
        except:
            pass
            
    except Exception:
        pass

def simulate_return_visitor(driver):
    """Simulate returning visitor behavior"""
    if not SIMULATE_RETURN_VISITS or random.random() > 0.3:  # 30% chance
        return False
    
    try:
        # Load existing cookies (return visitor)
        load_cookies(driver, COOKIES_FILE)
        
        # Shorter initial wait (familiar with site)
        time.sleep(random.uniform(1, 3))
        
        # More direct navigation (knows what they want)
        scroll_actions = random.randint(1, 3)  # Less scrolling
        for _ in range(scroll_actions):
            driver.execute_script(f"window.scrollBy(0, {random.randint(400, 800)});")
            time.sleep(random.uniform(0.3, 1.0))
        
        print("🔄 Simulating return visitor")
        return True
        
    except Exception:
        return False

# ============================================================================
# 📄 MULTI-PAGE NAVIGATION & SEARCH SIMULATION
# ============================================================================

def simulate_search_traffic(driver):
    """Simulate organic search traffic for Myntra"""
    if not ENABLE_SEARCH_SIMULATION:
        return False
    
    try:
        query = random.choice(SEARCH_QUERIES)
        search_url = f"https://www.myntra.com/{query.replace(' ', '-').lower()}"
        
        print(f"🔍 Simulating search: {query}")
        driver.get(search_url)
        time.sleep(random.uniform(2, 4))
        
        # Wait for dynamic content to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-base, .results-base"))
            )
        except:
            pass
        
        # Random scroll on search page to trigger lazy loading
        for _ in range(random.randint(2, 4)):
            driver.execute_script(f"window.scrollBy(0, {random.randint(400, 800)});")
            time.sleep(random.uniform(1, 2))
        
        # Try to find and click on target product or similar
        try:
            # Myntra uses different selectors for product links
            product_selectors = [
                "a[href*='/buy']",
                ".product-base a",
                ".product-productMetaInfo a",
                "a[data-testid='product']"
            ]
            
            for selector in product_selectors:
                try:
                    product_links = driver.find_elements(By.CSS_SELECTOR, selector)
                    if product_links:
                        link = random.choice(product_links[:5])
                        driver.execute_script("arguments[0].click();", link)
                        time.sleep(random.uniform(2, 3))
                        return True
                except:
                    continue
        except:
            pass
            
        return False
    except Exception:
        return False

def navigate_multiple_pages(driver):
    """Navigate through multiple pages to increase page views for Myntra"""
    if not ENABLE_MULTI_PAGE_NAVIGATION:
        return 1
    
    pages_visited = 1  # Already on main page
    max_pages = random.randint(*PAGE_VIEWS_PER_SESSION)
    
    try:
        for page_num in range(2, max_pages + 1):
            # Choose random page type
            page_type = random.choice(['additional', 'category', 'search'])
            
            if page_type == 'additional' and ADDITIONAL_PAGES:
                page_path = random.choice(ADDITIONAL_PAGES)
                full_url = f"https://www.myntra.com{page_path}"
                
            elif page_type == 'category' and CATEGORY_PAGES:
                full_url = random.choice(CATEGORY_PAGES)
                
            elif page_type == 'search':
                query = random.choice(SEARCH_QUERIES)
                # Myntra uses different search URL structure
                full_url = f"https://www.myntra.com/{query.replace(' ', '-').lower()}"
            
            else:
                continue
            
            print(f"📄 Page {page_num}/{max_pages}: {page_type}")
            driver.get(full_url)
            time.sleep(random.uniform(2, 4))  # Increased for dynamic loading
            
            # Wait for Myntra's dynamic content to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-base")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".results-base")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-productMetaInfo")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product']"))
                    )
                )
            except:
                pass
            
            # Interact with the page - more scrolling for dynamic loading
            random_scroll_and_interact(driver)
            
            # Additional scroll to trigger lazy loading on Myntra
            for _ in range(random.randint(2, 4)):
                driver.execute_script(f"window.scrollBy(0, {random.randint(400, 800)});")
                time.sleep(random.uniform(1, 2))
            
            pages_visited += 1
            
            # Random chance to return to main product
            if random.random() < 0.4:  # 40% chance
                driver.get(TARGET_URL)
                time.sleep(random.uniform(2, 3))
                
                # Wait for product page to load
                try:
                    WebDriverWait(driver, 10).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp-product-name")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-title")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".pdp-name"))
                        )
                    )
                except:
                    pass
                
                random_scroll_and_interact(driver)
                pages_visited += 1
                
    except Exception:
        pass
    
    return pages_visited

# ============================================================================
# 📊 ANALYTICS & REPORTING
# ============================================================================

def generate_analytics_report():
    """Generate detailed analytics report"""
    if not ENABLE_ANALYTICS or not os.path.exists(VISIT_LOG_FILE):
        return
    
    try:
        df = pd.read_csv(VISIT_LOG_FILE)
        
        print("\n" + "="*50)
        print("📊 ANALYTICS REPORT")
        print("="*50)
        print(f"Total visits: {len(df)}")
        print(f"Success rate: {len(df[df['Status'] == 'Success']) / len(df) * 100:.2f}%")
        print(f"Failed visits: {len(df[df['Status'] != 'Success'])}")
        
        if len(df) > 0:
            print(f"\nMost used referrer: {df['Referrer'].mode().iloc[0] if not df['Referrer'].mode().empty else 'N/A'}")
            print(f"Total unique user agents: {df['User-Agent'].nunique()}")
            
            # Time analysis
            df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour
            peak_hour = df['Hour'].mode().iloc[0] if not df['Hour'].mode().empty else 'N/A'
            print(f"Peak activity hour: {peak_hour}:00")
            
        print("="*50 + "\n")
        
    except Exception:
        pass

def calculate_dynamic_delay():
    """Calculate dynamic delay based on recent success rate"""
    try:
        if not os.path.exists(VISIT_LOG_FILE):
            return DELAY_BETWEEN_BATCHES
        
        df = pd.read_csv(VISIT_LOG_FILE)
        if len(df) < 10:
            return DELAY_BETWEEN_BATCHES
        
        # Check last 20 visits
        recent_visits = df.tail(20)
        success_rate = len(recent_visits[recent_visits['Status'] == 'Success']) / len(recent_visits)
        
        if success_rate > 0.9:
            return max(0.5, DELAY_BETWEEN_BATCHES - 0.5)
        elif success_rate < 0.7:
            return DELAY_BETWEEN_BATCHES + 1
        else:
            return DELAY_BETWEEN_BATCHES
            
    except Exception:
        return DELAY_BETWEEN_BATCHES

def log_visit(i, status, referrer, user_agent, location, viewport, target_url=""):
    """Log visit details to CSV"""
    try:
        with open(VISIT_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                i + 1,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                referrer,
                user_agent[:50] + "..." if len(user_agent) > 50 else user_agent,
                location,
                viewport,
                status,
                target_url
            ])
        
        # Console output with better formatting
        status_emoji = "✅" if status == "Success" else "❌"
        referrer_domain = referrer.split('//')[1].split('/')[0] if '//' in referrer else referrer
        url_display = target_url.split('/')[-1] if target_url else "N/A"
        print(f"{status_emoji} [{i+1}] {status} | {location} | {referrer_domain} | {url_display}")
        
    except Exception:
        pass

# ============================================================================
# 🚀 MAIN VISIT FUNCTIONS
# ============================================================================

def visit_site_advanced(i):
    """Advanced site visit with all features"""
    # Select target URL (rotate through multiple URLs)
    current_target_url = random.choice(TARGET_URLS) if TARGET_URLS else "https://www.myntra.com"
    
    # Enhanced mobile focus
    if ENABLE_MOBILE_FOCUS and random.random() < 0.7:  # 70% mobile traffic
        user_agent = random.choice(MOBILE_USER_AGENTS)
        viewport = random.choice(MOBILE_VIEWPORT_SIZES)
    else:
        user_agent = random.choice(USER_AGENTS)
        viewport = random.choice(VIEWPORT_SIZES)
    
    referrer = random.choice(REFERRERS)
    location = random.choice(LOCATIONS)
    
    # Chrome options setup with COMPLETE log suppression
    options = Options()
    
    # === NETHUNTER/ANDROID SPECIFIC OPTIONS ===
    if ENABLE_NETHUNTER_MODE:
        # Android/ARM specific optimizations
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=4096")
        
        # Force headless for mobile
        options.add_argument("--headless=new")
        
        # Set Chrome binary path if found
        chrome_binary = get_chrome_binary_path()
        if chrome_binary:
            options.binary_location = chrome_binary
    
    # === ESSENTIAL OPTIONS ===
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f"--window-size={viewport[0]},{viewport[1]}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # === STEALTH OPTIONS ===
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    
    # === COMPLETE LOG SUPPRESSION ===
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-gpu-logging")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--remote-debugging-port=0")
    options.add_argument("--disable-features=VizDisplayCompositor,AudioServiceOutOfProcess")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--mute-audio")
    
    # === PERFORMANCE & STEALTH ===
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--mute-audio")
    
    # === TENSORFLOW/ML SUPPRESSION ===
    options.add_argument("--disable-features=VizDisplayCompositor,AudioServiceOutOfProcess")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-features=Translate")
    
    # === GCM/NOTIFICATION SUPPRESSION ===
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-desktop-notifications")
    options.add_argument("--disable-push-messaging")
    options.add_argument("--disable-background-sync")
    
    # Headless mode with enhanced stealth
    if HEADLESS_MODE:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu-sandbox")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-features=NetworkService,NetworkServiceLogging")
    
    # === EXPERIMENTAL OPTIONS (Simplified) ===
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # === PREFS TO DISABLE FEATURES ===
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = None
    try:
        # Create service with COMPLETE log suppression
        service = Service()
        # service.log_path = os.devnull  # This line removed due to compatibility
        if os.name == 'nt':  # Windows
            service.creation_flags = 0x08000000  # CREATE_NO_WINDOW flag
        
        # Initialize driver with stderr suppression
        with suppress_stderr():
            driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set custom headers
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": user_agent,
            "acceptLanguage": CUSTOM_HEADERS["Accept-Language"],
            "platform": "Win32"
        })
        
        # Advanced anti-tracking setup
        set_geolocation(driver, location)
        randomize_browser_fingerprint(driver)
        simulate_ip_rotation_behavior(driver)
        inject_anti_fingerprinting_scripts(driver)
        
        # Set referrer and navigate
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"Referer": referrer}})
        
        # Navigate to target URL
        driver.get(current_target_url)
        
        # Load existing cookies
        load_cookies(driver, COOKIES_FILE)
        
        # Wait for page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Advanced human behavior simulation
        time.sleep(random.uniform(0.5, 1.0))
        
        # Enhanced shopping behaviors
        simulate_shopping_cart_actions(driver)
        simulate_product_exploration(driver)
        mobile_specific_interactions(driver)
        
        # Check for return visitor behavior
        is_return_visitor = simulate_return_visitor(driver)
        
        # Random scrolling with natural patterns
        scroll_actions = random.randint(3, 7)
        for _ in range(scroll_actions):
            scroll_direction = random.choice(['down', 'up'])
            if scroll_direction == 'down':
                scroll_y = random.randint(200, 800)
                driver.execute_script(f"window.scrollBy(0, {scroll_y});")
            else:
                scroll_y = random.randint(-400, -100)
                driver.execute_script(f"window.scrollBy(0, {scroll_y});")
            
            time.sleep(random.uniform(0.5, 1.0))
        
        # Random interactions
        random_interactions(driver)
        
        # Multi-page navigation for increased page views
        pages_visited = navigate_multiple_pages(driver)
        
        # Stay for realistic time (REDUCED for speed)
        if is_peak_time():
            stay_time = random.uniform(1, 2)  # Reduced from 8-15
        else:
            stay_time = random.uniform(1, 2)  # Reduced from 5-10
        
        time.sleep(stay_time)
        
        # Clear tracking data periodically
        clear_tracking_data(driver, i)
        
        # Save cookies for session continuity
        save_cookies(driver, COOKIES_FILE)
        
        return log_visit(i, "Success", referrer, user_agent, location["city"], f"{viewport[0]}x{viewport[1]}", current_target_url)
        
    except Exception as e:
        error_msg = f"Error: {str(e)[:100]}"
        return log_visit(i, error_msg, referrer, user_agent, location["city"], f"{viewport[0]}x{viewport[1]}", current_target_url)
        
    finally:
        if driver:
            with suppress_stderr():
                driver.quit()

def visit_site_with_retry(i, max_retries=MAX_RETRIES):
    """Visit site with retry logic and advanced features"""
    for attempt in range(max_retries):
        try:
            return visit_site_advanced(i)
        except Exception as e:
            if attempt == max_retries - 1:
                return log_visit(i, "Failed after retries", "", "", "", "")
            time.sleep(random.uniform(1, 2))

# Legacy function for compatibility
def visit_site(i):
    """Legacy function - redirects to advanced version"""
    return visit_site_with_retry(i)

# ============================================================================
# 🔄 BATCH PROCESSING & EXECUTION
# ============================================================================

def run_bulk_visits():
    """Enhanced bulk visit processing with analytics"""
    print("🚀 Starting Advanced Traffic Generator v6.0")
    target_display = f"{len(TARGET_URLS)} URLs" if len(TARGET_URLS) > 1 else TARGET_URLS[0] if TARGET_URLS else "No URLs"
    print(f"Target: {target_display}")
    print(f"Total visits: {TOTAL_VISITS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Headless mode: {'ON' if HEADLESS_MODE else 'OFF'}")
    print(f"Mobile focus: {'ON' if ENABLE_MOBILE_FOCUS else 'OFF'}")
    print("="*60)
    
    start_time = datetime.now()
    total_batches = (TOTAL_VISITS + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_start in range(0, TOTAL_VISITS, BATCH_SIZE):
        batch_num = (batch_start // BATCH_SIZE) + 1
        batch_end = min(batch_start + BATCH_SIZE, TOTAL_VISITS)
        
        print(f"\n🔄 Processing Batch {batch_num}/{total_batches} (Visits {batch_start+1}-{batch_end})")
        
        # Adjust batch size based on peak hours
        current_batch_size = BATCH_SIZE
        if is_peak_time():
            current_batch_size = min(BATCH_SIZE + 2, 15)
            print(f"⏰ Peak time detected - Using batch size: {current_batch_size}")
        
        batch_start_time = datetime.now()
        
        with ThreadPoolExecutor(max_workers=current_batch_size) as executor:
            executor.map(visit_site, range(batch_start, batch_end))
        
        batch_duration = (datetime.now() - batch_start_time).total_seconds()
        print(f"✅ Batch {batch_num} completed in {batch_duration:.1f}s")
        
        # Show progress
        progress = (batch_end / TOTAL_VISITS) * 100
        print(f"📊 Progress: {progress:.1f}% ({batch_end}/{TOTAL_VISITS})")
        
        # Generate interim analytics every 10 batches
        if batch_num % 10 == 0:
            generate_analytics_report()
        
        # Dynamic delay based on success rate
        if batch_num > 1:
            delay = calculate_dynamic_delay()
            if delay != DELAY_BETWEEN_BATCHES:
                print(f"⚡ Adjusting delay to {delay}s based on performance")
            time.sleep(delay)
        else:
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    # Final report
    total_duration = (datetime.now() - start_time).total_seconds()
    print(f"\n🎉 All visits completed!")
    print(f"⏱️  Total time: {total_duration/60:.1f} minutes")
    print(f"⚡ Average speed: {TOTAL_VISITS/(total_duration/60):.1f} visits/minute")
    
    # Generate final analytics
    generate_analytics_report()

def test_single_visit():
    """Test function for single visit"""
    print("🧪 Testing single visit...")
    visit_site_with_retry(0)
    print("✅ Test completed!")

def show_config():
    """Display current configuration"""
    print("\n📋 CURRENT CONFIGURATION")
    print("="*40)
    target_display = f"{len(TARGET_URLS)} URLs configured" if len(TARGET_URLS) > 1 else TARGET_URLS[0] if TARGET_URLS else "No URLs"
    print(f"Target URLs: {target_display}")
    print(f"Total visits: {TOTAL_VISITS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Delay between batches: {DELAY_BETWEEN_BATCHES}s")
    print(f"Max retries: {MAX_RETRIES}")
    print(f"Headless mode: {HEADLESS_MODE}")
    print(f"Analytics enabled: {ENABLE_ANALYTICS}")
    print(f"Mobile focus: {ENABLE_MOBILE_FOCUS}")
    print(f"Shopping actions: {ENABLE_SHOPPING_ACTIONS}")
    print(f"Available user agents: {len(USER_AGENTS)}")
    print(f"Available mobile UAs: {len(MOBILE_USER_AGENTS)}")
    print(f"Available referrers: {len(REFERRERS)}")
    print(f"Available locations: {len(LOCATIONS)}")
    print(f"Available viewports: {len(VIEWPORT_SIZES)}")
    print(f"Mobile viewports: {len(MOBILE_VIEWPORT_SIZES)}")
    print("="*40 + "\n")

# ============================================================================
# 📝 LOG FILE INITIALIZATION
# ============================================================================

# Initialize Log File
if not os.path.exists(VISIT_LOG_FILE):
    with open(VISIT_LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Visit#", "Timestamp", "Referrer", "User-Agent", "Location", "Viewport", "Status", "Target_URL"])

# ============================================================================
# 🚀 MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Suppress Chrome logs during execution
    suppress_chrome_logs()
    
    try:
        # Detect NetHunter/Android environment
        is_nethunter, is_android = detect_nethunter_environment()
        
        # Optimize for mobile if detected
        if is_nethunter or is_android:
            optimize_for_mobile()
        
        # Get target URLs from user
        get_target_url()
        
        # Interactive configuration menu
        interactive_menu()
        
        # Custom timing/scheduling
        if not schedule_traffic():
            print("❌ Scheduling cancelled!")
            sys.exit(0)
        
        # Cleanup old sessions
        cleanup_old_sessions()
        
        # Show final configuration
        show_config()
        
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            test_single_visit()
        else:
            run_bulk_visits()
            
        # Generate final advanced analytics
        generate_advanced_analytics()
        
    finally:
        # Restore stderr at the end
        restore_stderr()
