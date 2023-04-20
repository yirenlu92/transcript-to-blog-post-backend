from prompts import initial_prompt_with_points, initial_prompt_without_points, prompt_suffix, prompt_suffix_transcript

def create_default_prompt(points, match):
    # check if points is only empty strings or if points is empty
    if all(not point.strip() for point in points) or len(points) == 0:
        # dont include points in prompt
        total_prompt = initial_prompt_without_points.format(match)
    

    # include points in prompt
    points = "\n".join(points)
    total_prompt = initial_prompt_with_points.format(points, match)
    return total_prompt

def create_user_defined_prompt(points, match, user_prompt):
    # check if points is only empty strings or if points is empty
    if all(not point.strip() for point in points) or len(points) == 0:
        # dont include points in prompt
        total_prompt = user_prompt + match
    

    # include points in prompt
    points = "\n".join(points)
    total_prompt = user_prompt + prompt_suffix.format(points, match)
    return total_prompt