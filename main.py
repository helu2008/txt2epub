from ebooklib import epub
import re

def read_text(filename):
    for enc in ['utf-8', 'gb18030', 'gbk', 'big5']:
        try:
            with open(filename, 'r', encoding=enc) as f:
                return f.read()
        except:
            pass
    raise ValueError("encoding error")

def convert(filename):
    text = read_text(filename)
    parts = re.split(r'(第[一二三四五六七八九十百千0-9]+[章].*?)\n', text)
    chapters = []
    if len(parts) >= 3:
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            body = parts[i+1].strip().replace('\n', '<br/>')
            chapters.append((title, body))
    else:
        chapters.append(("Content", text.strip().replace('\n', '<br/>')))
    book = epub.EpubBook()
    title = filename.replace(".txt", "")
    book.set_title(title)
    book.set_language("zh")
    book.add_author("Unknown")
    spine = ['nav']
    toc = []
    for i, (t, c) in enumerate(chapters):
        ch = epub.EpubHtml(title=t, file_name=f'chap_{i}.xhtml', lang='zh')
        ch.content = f'<h1>{t}</h1><p>{c}</p>'
        book.add_item(ch)
        spine.append(ch)
        toc.append(ch)
    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(title + '.epub', book, {})

