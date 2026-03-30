import os
import glob

def compile_manuscript():
    """Compiles all markdown sections into a single manuscript."""
    # Find all .md files in the current directory that start with a number
    # This ensures abstract, introduction, etc. are grabbed in order.
    section_files = sorted(glob.glob("*.md"))
    
    # Filter out the compiled manuscript if it already exists to avoid duplication
    section_files = [f for f in section_files if f != "compiled_manuscript.md"]
    
    print("Found sections to compile:")
    for f in section_files:
        print(f"  - {f}")
        
    compiled_content = ""
    for file in section_files:
        with open(file, 'r', encoding='utf-8') as f:
            compiled_content += f.read() + "\n\n---\n\n"
            
    output_file = "compiled_manuscript.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(compiled_content)
        
    print(f"\n✅ Successfully compiled {len(section_files)} sections into {output_file}!")

if __name__ == "__main__":
    compile_manuscript()
