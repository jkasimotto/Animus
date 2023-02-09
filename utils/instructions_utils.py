
def compare_answers(list1, list2, return_correct=True):
    result = []
    for i, tuple1 in enumerate(list1):
        if return_correct and tuple1 == list2[i]:
            result.append(i)
        if not return_correct and tuple1 != list2[i]:
            result.append(i)
    return result

def nested_list_to_nested_numbered_str(list_of_lists):
    """
    Only does one level of nesting.
    """
    result = []
    for i, list_of_xs in enumerate(list_of_lists):
        for j, x in enumerate(list_of_xs):
            result.append(f"{i + 1}.{j + 1} {x}")
    return "\n".join(result)

def nested_numbered_str_to_nested_list(formatted_answer_str: str):
    lines = formatted_answer_str.strip().split("\n")
    lines = [line for line in lines if line.strip() != ""]
    result = []
    current_list = []
    current_level = 0
    for line in lines:
        level, answer = line.strip().split(" ", 1)
        level = int(level.split(".")[0])
        if level > current_level:
            result.append(current_list)
            current_list = [answer]
            current_level = level
        elif level == current_level:
            current_list.append(answer)
    result.append(current_list)
    result = [l for l in result if len(l) > 0]
    return result