import re
from pathlib import Path

def generate_toc(markdown_text: str) -> str:
    """
    Sinh danh sách mục lục có đánh số và liên kết anchor tự động (chuẩn Markdown).
    """
    headers = re.findall(r'^(#{1,6})\s+(.*)', markdown_text, re.MULTILINE)
    toc_lines = []
    counters = [0] * 6  # hỗ trợ tới H6

    for hashes, title in headers:
        level = len(hashes)
        # Bỏ qua tiêu đề "Mục lục"
        if title.strip().lower().startswith("mục lục"):
            continue

        counters[level - 1] += 1
        for i in range(level, 6):
            counters[i] = 0

        numbering = ".".join(str(c) for c in counters[:level] if c > 0)
        anchor = re.sub(r'[^\w\s-]', '', title).strip().lower()
        anchor = re.sub(r'\s+', '-', anchor)

        # 4 dấu cách mỗi cấp (chuẩn Markdown nested list)
        indent = "    " * (level - 1)
        toc_lines.append(f"{indent}- {numbering}. [{title}](#{anchor})")

    # thêm dòng trống sau mỗi mục để đảm bảo xuống dòng đúng
    return "\n".join(toc_lines) + "\n"


def update_toc(file_path: str):
    """
    Tự động cập nhật hoặc chèn mục lục vào file Markdown.
    """
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    toc_content = generate_toc(content)
    toc_block = f"<!-- TOC START -->\n{toc_content}<!-- TOC END -->"

    if "<!-- TOC START -->" in content and "<!-- TOC END -->" in content:
        new_content = re.sub(
            r'<!-- TOC START -->.*?<!-- TOC END -->',
            toc_block,
            content,
            flags=re.DOTALL,
        )
    else:
        new_content = f"# Mục lục\n\n{toc_block}\n\n---\n\n{content}"

    path.write_text(new_content, encoding="utf-8")
    print(f"✅ Đã cập nhật mục lục trong: {file_path}")


if __name__ == "__main__":
    update_toc("README.md")
