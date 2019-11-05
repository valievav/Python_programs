"""
Helps processing parameters output from GUI form.
"""

def one_elem_str_param_from_list(param_list: list)->str or None:
    """
    Converts list to one element string parameter.\n
    If passed list with more than 1 value - used only 1st element.\n
    """
    if len(param_list) == 1:
        str_value = "".join(param_list)
        return str_value
    elif len(param_list) > 1:
        first_value = param_list[0]
        print(f"List length is {len(param_list)}, expected 1. Going to use first element only - {first_value}")
        return first_value
    else:
        return None


def main():
    values_list = ["Voyager"]

    str_value = one_elem_str_param_from_list(values_list)
    print(str_value, type(str_value))


if __name__ == "__main__":
    main()

