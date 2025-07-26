import openai
import os

def read_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_doc_from_chatgpt(code, api_key):
    openai.api_key = api_key

    prompt = (
        "You are a technical documentation generator. "
        "Given the following Python code, create a clean and structured technical documentation. "
        "Include: Module description, classes with docstrings and methods, standalone functions, and purpose of the code.\n\n"
        f"```python\n{code}\n```"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior software documenter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Error: {e}"

def save_output(doc, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"✅ Documentation saved to {output_path}")

if __name__ == "__main__":
    file_path = input("📄 Enter Python file path: ").strip()
    api_key = input("🔐 Enter your OpenAI API Key: ").strip()
    output_path = input("📁 Output file name (default: doc.md): ").strip() or "doc.md"

    if os.path.exists(file_path):
        code = read_code(file_path)
        documentation = generate_doc_from_chatgpt(code, api_key)
        save_output(documentation, output_path)
    else:
        print("❌ Invalid file path.")
