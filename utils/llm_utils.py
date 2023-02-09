import random
import time

import openai
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from utils.prompt_utils import format_multiline_string


# define a retry decorator
def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff."""
 
    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay
 
        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)
 
            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1
 
                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
 
                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())
 
                # Sleep for the delay
                print(f"Sleeping for {delay} seconds before retry {num_retries}")
                time.sleep(delay)
 
            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e
 
    return wrapper

@retry_with_exponential_backoff
def make_llm_call(prompt_template, input_variables, formatted_inputs, output_fn=None, temperature=0.0, verbose=True):
    result = LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(prompt_template),
            input_variables=input_variables
        ),
        llm=OpenAI(temperature=temperature),
        verbose=verbose,
    ).predict(**formatted_inputs)
    if verbose:
        print("OUTPUT: ", result)
    if output_fn:
        result = output_fn(result)
    if verbose:
        print("OUTPUT AFTER: ", result)
    return result