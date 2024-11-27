# movie/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter(name='youtube_embed_url')
def youtube_embed_url(value):
    if "youtube.com/watch" in value:
        video_id = value.split("v=")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return value
