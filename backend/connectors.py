import os
import random
from typing import List, Dict

# Connector scaffolding for Indian marketplaces.
# Returns mock data — replace with real API calls when keys are available.

def fetch_from_amazon(query: str) -> List[Dict]:
    return [
        {
            'title': f'{query} - Amazon Choice',
            'price': '₹' + str(random.choice([19999, 24999, 29999, 34999])),
            'category': 'Electronics',
            'description': f'Top-rated Amazon listing for {query}. Fast delivery with Prime.',
            'source': 'Amazon',
            'rating': round(random.uniform(4.0, 4.8), 1),
            'reviews': ["Great value for money", "Battery lasts long"],
            'colors': ['Black', 'Blue']
        }
    ]

def fetch_from_flipkart(query: str) -> List[Dict]:
    return [
        {
            'title': f'{query} - Flipkart Choice',
            'price': '₹' + str(random.choice([9999, 12499, 14999, 18999])),
            'category': 'Mobile',
            'description': f'Flipkart assured listing for {query}. Good for budget buyers.',
            'source': 'Flipkart',
            'rating': round(random.uniform(3.8, 4.6), 1),
            'reviews': ["Value for money", "Good display quality"],
            'colors': ['White', 'Red']
        }
    ]

def fetch_from_myntra(query: str) -> List[Dict]:
    return [
        {
            'title': f'{query} - Myntra Select',
            'price': '₹' + str(random.choice([1299, 1999, 2499])),
            'category': 'Fashion',
            'description': f'Myntra listing for {query}. Stylish and comfortable.',
            'source': 'Myntra',
            'rating': round(random.uniform(4.0, 4.7), 1),
            'reviews': ["Fits perfectly", "Nice fabric quality"],
            'colors': ['Green', 'Yellow']
        }
    ]

def fetch_from_ajio(query: str) -> List[Dict]:
    return [
        {
            'title': f'{query} - Ajio Exclusive',
            'price': '₹' + str(random.choice([1499, 2199, 2799, 3499])),
            'category': 'Fashion',
            'description': f'Ajio exclusive listing for {query}. Trendy and affordable.',
            'source': 'Ajio',
            'rating': round(random.uniform(3.9, 4.5), 1),
            'reviews': ["Good quality", "Delivered on time"],
            'colors': ['Navy', 'Black']
        }
    ]

def fetch_from_meesho(query: str) -> List[Dict]:
    return [
        {
            'title': f'{query} - Meesho Deal',
            'price': '₹' + str(random.choice([499, 799, 999, 1299])),
            'category': 'General',
            'description': f'Budget-friendly Meesho listing for {query}. Best price guaranteed.',
            'source': 'Meesho',
            'rating': round(random.uniform(3.5, 4.3), 1),
            'reviews': ["Cheap and decent", "Good for the price"],
            'colors': ['Mixed']
        }
    ]

def fetch_by_platform(platform: str, query: str) -> List[Dict]:
    platform = platform.lower()
    if platform == 'amazon':
        return fetch_from_amazon(query)
    if platform == 'flipkart':
        return fetch_from_flipkart(query)
    if platform == 'myntra':
        return fetch_from_myntra(query)
    if platform == 'ajio':
        return fetch_from_ajio(query)
    if platform == 'meesho':
        return fetch_from_meesho(query)
    return []
