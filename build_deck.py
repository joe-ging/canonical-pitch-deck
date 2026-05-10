import os

def build():
    slides_dir = 'slides'
    assets_dir = 'assets'
    template_file = 'template.html'
    output_file = 'index.html'

    print(f"--- Building Deck ---")

    # 1. Read Template
    if not os.path.exists(template_file):
        print(f"Error: {template_file} not found.")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 2. Collect Slides
    slide_files = sorted([f for f in os.listdir(slides_dir) if f.endswith('.html')])
    slides_content = []
    
    for filename in slide_files:
        print(f"  Adding slide: {filename}")
        with open(os.path.join(slides_dir, filename), 'r', encoding='utf-8') as f:
            slides_content.append(f.read())

    all_slides_html = "\n\n".join(slides_content)

    # 3. Assemble
    final_content = template_content.replace('<!-- SLIDES_HOLDER -->', all_slides_html)

    # 4. Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"--- Build Complete: {output_file} ---")

if __name__ == "__main__":
    build()
