import re

def extract_keywords(jd_text):
    # Simple extraction: words longer than 2 letters, not common stopwords
    stopwords = {'the', 'and', 'for', 'with', 'you', 'are', 'this', 'that', 'from', 'will', 'have', 'your', 'our'}
    words = re.findall(r'\b[a-zA-Z]{3,}\b', jd_text.lower())
    keywords = set(w for w in words if w not in stopwords)
    return keywords