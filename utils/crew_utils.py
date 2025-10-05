

def sanitize_column_name(col):
    """Convert Excel columns to SQLite-safe names"""
    col = str(col).strip()
    col = col.replace(' ', '_')
    col = col.replace('-', '_')
    col = col.replace('%', 'pct')
    col = col.replace('(', '').replace(')', '')
    col = col.replace('/', '_')
    col = col.replace('.', '_')
    if col and col[0].isdigit():
        col = '_' + col
    return col.lower()