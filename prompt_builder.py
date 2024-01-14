# Custom GPT-4 functions for the GPT-4 API
import ipdb
import constants
import tiktoken

from openai import OpenAI

client = OpenAI()

def tokens(text: str, model: str) -> int:
    """Returns the length of the text, measured in tokens"""

    enc = tiktoken.encoding_for_model(model)

    return len(enc.encode(text))

def compressor_prompt(text: str, max_tokens = None) -> str:
    """Returns a prompt for compressing text."""

    if max_tokens is None:
        return f"""Compress the following text in a way such that you (GPT-4) can reconstruct the semantic information as close as possible to the original while using as little tokens as possible. This is for yourself, you do not need to make it human readable. Aggressively compress it in any way you see fit.  Abuse of language mixing, abbreviations, symbols (unicode and emoji), or any other encodings or internal representations is all permissible, as long as it, if pasted in a new inference cycle, will yield results that are near-identical in meaning to the original text:\n\n## Text to compress:\n\n{text}"""
    
    else:
        return f"""Compress the following text in a way such that you (GPT-4) can reconstruct the semantic information as close as possible to the original while using less than {max_tokens} tokens. This is for yourself, you do not need to make it human readable. Aggressively compress it in any way you see fit.  Abuse of language mixing, abbreviations, symbols (unicode and emoji), or any other encodings or internal representations is all permissible, as long as it, if pasted in a new inference cycle, will yield results that are near-identical in meaning to the original text:\n\n## Text to compress:\n\n{text}"""

def compress(text:str, max_tokens: None, model: str = "gpt-4") -> str:
    """Returns a compressed version of the text."""

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": compressor_prompt(text, max_tokens)}
            ])
    
    return completion.choices[0].message.content

def grader_prompt(
        essay: str,
        assignment_prompt_blueprint: str,
        assignment: str,
        assignment_option_1: str,
        assignment_option_2: str,
        extra: str = None) -> str:
    """Returns a prompt for grading an assignment."""
    
    return assignment_prompt_blueprint.format_map({
        "assignment": assignment,
        "assignment_option_1": assignment_option_1,
        "assignment_option_2": assignment_option_2,
        "student_paper": essay,
        "extra": extra
    })

def grade_assignment_1_prompt(essay: str, max_tokens: int = 8000, model: str = "gpt-4") -> str:
    """Returns a prompt for grading assignment 1."""

    prompt = grader_prompt(
    essay=essay,
    assignment_prompt_blueprint=constants.assignment1_prompt_blueprint,
    assignment=constants.assignment1_instructions_compressed,
    assignment_option_1=constants.assignment1_option1_excerpt_compressed,
    assignment_option_2=constants.assignment1_option2_excerpt_compressed)

    # If the essay is too long, compress it
    prompt_tokens = tokens(prompt, model)
    if prompt_tokens > max_tokens:
        essay_tokens = tokens(essay, model)
        essay_tokens_to_keep = int(essay_tokens - (prompt_tokens - max_tokens))
        essay = compress(essay, essay_tokens_to_keep, model)

        prompt = grader_prompt(
            essay=essay,
            assignment_prompt_blueprint=constants.assignment1_prompt_blueprint_compressed,
            assignment=constants.assignment1_instructions_compressed,
            assignment_option_1=constants.assignment1_option1_excerpt_compressed,
            assignment_option_2=constants.assignment1_option2_excerpt_compressed)

    return prompt

def grade_assignment_2_prompt(essay: str, max_tokens: int = 8000, model: str = "gpt-4") -> str:
    """Returns a prompt for grading assignment 2."""

    prompt = grader_prompt(
    essay=essay,
    assignment_prompt_blueprint=constants.assignment2_prompt_blueprint,
    assignment=constants.assignment2_instructions_compressed,
    assignment_option_1=constants.assignment2_option1_excerpt_compressed,
    assignment_option_2=constants.assignment2_option2_excerpt_compressed,
    extra=constants.assignment1_instructions_compressed)

    # If the essay is too long, compress it
    prompt_tokens = tokens(prompt, model)
    if prompt_tokens > max_tokens:
        essay_tokens = tokens(essay, model)
        essay_tokens_to_keep = int(essay_tokens - (prompt_tokens - max_tokens))
        essay = compress(essay, essay_tokens_to_keep, model)

        prompt = grader_prompt(
            essay=essay,
            assignment_prompt_blueprint=constants.assignment2_prompt_blueprint_compressed,
            assignment=constants.assignment2_instructions_compressed,
            assignment_option_1=constants.assignment2_option1_excerpt_compressed,
            assignment_option_2=constants.assignment2_option2_excerpt_compressed,
            extra=constants.assignment1_instructions_compressed)
        
    return prompt
