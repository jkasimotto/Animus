from textwrap import dedent
import time


def format_multiline_string(prompt):
    # Dedent the prompt
    prompt = dedent(prompt)
    # Strip leading and trailing newlines
    prompt = prompt.strip("\n")
    return prompt


def bulletpoint_str_to_list(output_str):
    lines = output_str.strip().split("\n")
    result = [line.strip()[2:] for line in lines]
    return result


def list_to_bulletpoint_str(input_list):
    return "\n".join([f"- {item}" for item in input_list])


def list_to_numbered_str(input_list):
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(input_list)])


def numbered_str_to_list(output_str):
    lines = output_str.strip().split("\n")
    result = [line.strip()[line.find(" ") + 1:] for line in lines]
    return result

def numbered_bools_str_to_list(output_str):
    """
    Converts a string of the form:
    1. True
    2. False
    To a list of booleans.
    """
    str_bools = numbered_str_to_list(output_str)
    bools = [str_bool.strip().lower() == "true" for str_bool in str_bools]
    return bools

def comma_str_to_list(comma_str):
    return [item.strip() for item in comma_str.split(",")]
