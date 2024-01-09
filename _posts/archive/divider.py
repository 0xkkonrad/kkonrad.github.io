import re

def sanitize_title(title):
    """
    Sanitizes the title to be used as a filename. Removes special characters.
    """
    sanitized_title = re.sub(r'[^a-zA-Z0-9-]', '', title.replace(' ', '-'))
    return sanitized_title

def extract_date_title(text):
    """
    Extracts the date and title from the blog post text and removes the date from the text.
    """
    title_match = re.search(r'title: (.+)', text)
    date_match = re.search(r'Data: (\d{4}-\d{2}-\d{2})', text)
    
    if title_match and date_match:
        title = title_match.group(1).strip()
        date = date_match.group(1).strip()

        # Remove the date line from the text
        text = text.replace(f"Data: {date}\n", "")

        return date, title, text
    return None, None, text

def process_markdown_file(filename):
    """
    Processes the markdown file and splits it into separate files without the dates in the content.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    posts = content.split("=======================\n")

    for post in posts:
        if post.strip():
            date, title, post_content = extract_date_title(post)
            if date and title:
                sanitized_title = sanitize_title(title)
                new_filename = f'{date}-{sanitized_title}.md'
                with open(new_filename, 'w', encoding='utf-8') as new_file:
                    new_file.write(post_content)
                    print(f'File created: {new_filename}')

# Replace 'your_markdown_file.md' with the path to your markdown file
process_markdown_file('your_markdown_file.md')
