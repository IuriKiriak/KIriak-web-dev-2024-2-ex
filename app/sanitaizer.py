import markdown
import bleach

def sanitaizer_text(user_input):
    allowed_tags = [
        'p', 'br', 'em', 'strong', 'a', 'img', 'code', 'pre',
        'blockquote', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
    ]

    allowed_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title'],
        'code': ['class'],
        'pre': ['class']
    }

    html_content = markdown.markdown(user_input)
    sanitized_content = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attributes)

    return sanitized_content