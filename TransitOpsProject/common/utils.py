# common/utils.py
# Common utilities

def format_weight(weight):
    if weight is not None:
        return f"{weight:,.2f} kg"
    return "0 kg"
