import os
import json
from pathlib import Path

def process_pdfs():
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all PDF files from input directory
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    
    for pdf_file in pdf_files:
        # Create dummy JSON data
        dummy_data = {
            "filename": pdf_file.name,
            "status": "processed",
            "metadata": {
                "page_count": 10,
                "file_size": 1024,
                "creation_date": "2024-03-20"
            }
        }
        
        # Generate output JSON file
        output_file = Path(output_dir) / f"{pdf_file.stem}.json"
        with open(output_file, 'w') as f:
            json.dump(dummy_data, f, indent=2)
        
        print(f"Processed {pdf_file.name} -> {output_file.name}")

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs() 
    print("completed processing pdfs")