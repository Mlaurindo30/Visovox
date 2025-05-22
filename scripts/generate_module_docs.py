import os
import ast
import re
from pathlib import Path

MODULES_DIR = Path("src/visiovox/modules/")
DOCS_DIR = Path("docs/modules/")

HEADER = """# Documentação do Módulo `{module}`\n\n"""

TEMPLATE = """
## 1. Sumário do Módulo
{sumario}

## 2. Análise Pré-Código
- **Responsabilidades Principais:**
  - <Extraído de docstrings ou manual>
- **Arquivos:**
{arquivos}
- **Classes:**
{classes}

## 3. Estrutura de Arquivos, Classes e Métodos
{tabela}

## 4. Notas e Recomendações
- **Extensibilidade:** <Manual ou extraído>
- **Integração:** <Manual ou extraído>
- **Testabilidade:** <Manual ou extraído>
- **Input/Output:** <Manual ou extraído>

## 5. Exemplo de Uso
{exemplo_uso}

## 6. Pontos de Atenção e Próximos Passos
- <Manual ou extraído>
"""

def extract_example_from_docstring(doc):
    if not doc:
        return None
    # Busca bloco de código python
    code_blocks = re.findall(r"```python(.*?)```", doc, re.DOTALL)
    if code_blocks:
        return f"```python\n{code_blocks[0].strip()}\n```"
    # Busca seção 'Exemplo de Uso' (linha + bloco)
    match = re.search(r"Exemplo de Uso[:\n]+(.*?)(?:\n\s*\n|$)", doc, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_classes_and_docstrings(py_path):
    """Extrai classes, docstrings, métodos e exemplos de um arquivo Python."""
    with open(py_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    classes = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            methods = []
            for n in node.body:
                if isinstance(n, ast.FunctionDef):
                    mdoc = ast.get_docstring(n) or ""
                    methods.append({
                        'name': n.name,
                        'doc': mdoc.splitlines()[0] if mdoc else ''
                    })
            example = extract_example_from_docstring(doc)
            classes.append({
                'name': node.name,
                'doc': doc,
                'methods': methods,
                'example': example
            })
    return classes

def generate_module_doc(module_name):
    module_path = MODULES_DIR / module_name
    arquivos = []
    classes = []
    tabela = "| Arquivo | Classe(s) | Métodos Principais | Descrição |\n|--------|-----------|--------------------|-----------|\n"
    sumario = []
    exemplo_uso = None
    for py_file in module_path.glob("*.py"):
        class_list = extract_classes_and_docstrings(py_file)
        arquivos.append(f"  - `{py_file.name}`")
        for c in class_list:
            method_list = ", ".join([f"{m['name']}" for m in c['methods']])
            method_desc = "; ".join([f"{m['name']}: {m['doc']}" for m in c['methods'] if m['doc']])
            classes.append(f"  - {c['name']}: {c['doc'].splitlines()[0] if c['doc'] else ''}")
            tabela += f"| {py_file.name} | {c['name']} | {method_list or '-'} | {c['doc'].splitlines()[0] if c['doc'] else '-'} |\n"
            # Para sumário e exemplo de uso
            if c['doc']:
                sumario.append(f"- **{c['name']}**: {c['doc'].splitlines()[0]}")
            if not exemplo_uso and c['example']:
                exemplo_uso = c['example']
    sumario_str = "\n".join(sumario) if sumario else "<Resumo automático ou manual do módulo>"
    exemplo_uso = exemplo_uso or "```python\n# Exemplo gerado manualmente ou por padrão\n```"
    doc = HEADER.format(module=module_name)
    doc += TEMPLATE.format(
        sumario=sumario_str,
        arquivos="\n".join(arquivos),
        classes="\n".join(classes),
        tabela=tabela,
        exemplo_uso=exemplo_uso
    )
    out_path = DOCS_DIR / f"{module_name}.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f"Gerado: {out_path}")

def main():
    for module_dir in MODULES_DIR.iterdir():
        if module_dir.is_dir() and not module_dir.name.startswith('__'):
            generate_module_doc(module_dir.name)

if __name__ == "__main__":
    main() 