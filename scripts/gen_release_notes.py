from datetime import datetime

def generate_release_notes(version, changes, bugfixes, breaking, contributors, links=None):
    date_str = datetime.now().strftime("%Y-%m-%d")
    notes = f"""# VisioVox Fusion — Release v{version}
_Data de Release: {date_str}_

## ✨ Novidades
{''.join(f"- {c}\n" for c in changes)}

## 🐞 Correções
{''.join(f"- {b}\n" for b in bugfixes)}

## 🚨 Mudanças Incompatíveis (Breaking Changes)
{''.join(f"- {br}\n" for br in breaking)}

## 👨‍💻 Contribuidores
{', '.join(contributors)}

## 🔗 Links Importantes
{links or '—'}

---
"""
    return notes

# Exemplo de uso:
if __name__ == "__main__":
    print(generate_release_notes(
        "1.3.0",
        ["Novo endpoint `/scene_analysis/analyze` com status incremental.",
         "Plug Real dos módulos YOLOFaceDetector, FanLandmarkExtractor, SAM2Segmenter.",
         "Exemplo real de overlay/mask disponível para frontend."],
        ["Corrigido bug em upload de vídeo com params inválidos."],
        ["Campo `embedding` em faces agora é lista de floats, não string."],
        ["@user1", "@user2"],
        "Docs: https://docs.visiovoxfusion.ai | Demo: https://fusion.visiovox.ai"
    ))