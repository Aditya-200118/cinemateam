from django import template
from math import ceil
register = template.Library()

@register.filter
def get_range(value):
    return range(value)

@register.filter
def seat_position(row, col):
    return (row) * 10 + col


@register.filter
def last_row_seat_count(seat_count):
    return seat_count % 10 or 10

@register.filter
def num_rows(seat_count):
    return ceil(seat_count / 10)
# your_app/templatetags/custom_filters.py

# In your app's templatetags directory, create a file called `custom_filters.py` if you haven't already
# @register.filter
# def merge_and_convert(row, col):
#     """Concatenate row and column into a string and convert to int."""
#     return str(int(row) * 10 + int(col))  # Adjust according to your seat numbering logic

# In your app's templatetags directory, add to your custom_filters.py

# @register.filter
# def reverse_seat_position(seat_number):
#     """Convert absolute seat number back to row and column."""
#     col = seat_number % 10
#     row = (seat_number // 10) + 1
#     return row, col

# @register.filter
# def merge_and_convert(row_col):
#     """Concatenate row and column from a string 'row,col' and convert to int."""
#     if row_col is None:
#         return None
#     try:
#         row, col = map(int, row_col.split(','))
#         return row * 10 + col  # Adjust according to your seat numbering logic
#     except (ValueError, TypeError):
#         return None  # Handle conversion errors gracefully


# from django import template

# register = template.Library()

@register.filter
def merge_and_convert(row, col):
    """Concatenate row and column into an integer."""
    return int(row) * 10 + int(col)  # Adjust according to your seat numbering logic
