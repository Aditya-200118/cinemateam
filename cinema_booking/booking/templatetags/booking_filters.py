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

@register.filter
def index_add_one(value):
    try:
        if isinstance(value, list):
            return [str(int(v) + 1) for v in value]
        return str(int(value) + 1)
    except (TypeError, ValueError):
        return value

@register.filter
def merge_and_convert(row, col):
    return int(row) * 10 + int(col)
