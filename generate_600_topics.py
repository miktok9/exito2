"""
Generate 600 Spanish topics about ancient women's history.
"""

import requests
from urllib.parse import quote
from pathlib import Path
import time

def generate_spanish_topics_batch(batch_num, count=100):
    """Generate a batch of Spanish topics."""
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        raise ValueError("POLLINATIONS_API_KEY environment variable is required")
        
    base_url = "https://gen.pollinations.ai/text/"
    
    # Simpler system prompt
    system = (
        "Eres un historiador especializado en la historia de las mujeres en las civilizaciones antiguas. "
        f"Crea {count} tópicos únicos en español sobre mujeres en las civilizaciones antiguas. "
        "Cada tópico debe ser de 5 a 10 palabras, interesante y educativo. "
        "Cubre: leyes, costumbres, mujeres famosas, profesiones, religión, cultura, arte. "
        "Produce SOLAMENTE los tópicos, uno por línea, sin números ni viñetas."
    )
    
    prompt = f"Genera {count} tópicos únicos en español sobre mujeres en las civilizaciones antiguas"
    
    url = base_url + quote(prompt)
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"model": "nova-fast", "temperature": 0.9, "system": system}
    
    print(f"[batch {batch_num}] Generating {count} Spanish topics...")
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=120)
        r.raise_for_status()
        
        # Parse topics
        topics = []
        for line in r.text.strip().split('\n'):
            cleaned = line.strip()
            # Remove common prefixes
            for prefix in ['- ', '* ', '• ', '→ ', '> ']:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):]
            # Remove numbering
            import re
            cleaned = re.sub(r'^\d+[\.\:\)\-]\s*', '', cleaned)
            
            if cleaned and len(cleaned) > 5:
                topics.append(cleaned)
        
        print(f"[batch {batch_num}] Generated {len(topics)} topics")
        return topics[:count]
    
    except Exception as e:
        print(f"[batch {batch_num}] Error: {e}")
        return []

def main():
    """Generate 600 Spanish topics in batches."""
    
    all_topics = []
    batches = 6  # 6 batches of 100 = 600 topics
    
    for i in range(batches):
        topics = generate_spanish_topics_batch(i+1, 100)
        all_topics.extend(topics)
        
        print(f"[progress] Total topics so far: {len(all_topics)}")
        
        # Wait between batches to avoid rate limits
        if i < batches - 1:
            print("[progress] Waiting 5 seconds before next batch...")
            time.sleep(5)
    
    # Write to file
    topics_file = Path('topics.txt')
    with open(topics_file, 'w', encoding='utf-8') as f:
        for topic in all_topics:
            f.write(f"{topic}\n")
    
    print(f"\n[done] Generated {len(all_topics)} Spanish topics!")
    print(f"[done] Saved to {topics_file}")

if __name__ == '__main__':
    main()
