#!/usr/bin/env python3
"""
Extract and clean the legal reporters JSON from RTF format
"""
import re
import json

def extract_json_from_rtf(rtf_file):
    with open(rtf_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find the start of the JSON array
    array_start = content.find('[\\')
    if array_start == -1:
        print("Could not find JSON array start")
        return None
    
    # Extract content from array start to end
    json_content = content[array_start:]
    
    # Find the end of the JSON array
    array_end = json_content.find(']\\')
    if array_end == -1:
        print("Could not find JSON array end")
        return None
    
    json_content = json_content[:array_end + 1]
    
    # Clean RTF formatting
    json_content = json_content.replace('\\', '')
    json_content = json_content.replace('\n', ' ')
    json_content = json_content.replace('\r', ' ')
    
    # Fix common RTF artifacts
    json_content = re.sub(r'\'93([^\']*?)\'94', r'"\1"', json_content)  # Replace smart quotes
    json_content = re.sub(r'\'92', "'", json_content)  # Replace apostrophes
    json_content = re.sub(r'\'96', "–", json_content)  # Replace em dashes
    json_content = re.sub(r'oai_citation:\d+\'87[^)]*\)', '', json_content)  # Remove citations
    
    # Fix spacing and formatting
    json_content = re.sub(r'\s+', ' ', json_content)
    json_content = json_content.strip()
    
    return json_content

def main():
    # Extract content
    content = extract_json_from_rtf('legal_reporters_complete.json')
    
    if content:
        print("Extracted content sample:")
        print(content[:500])
        print("...")
        
        # Save raw extracted content
        with open('legal_reporters_raw.txt', 'w') as f:
            f.write(content)
        
        print("Raw content saved to legal_reporters_raw.txt")
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
            print(f"Successfully parsed JSON with {len(data)} entries")
            
            # Save clean JSON
            with open('legal_reporters_clean.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print("Clean JSON saved to legal_reporters_clean.json")
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print("Manual cleanup needed")

if __name__ == "__main__":
    main()