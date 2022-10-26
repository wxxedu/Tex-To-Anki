import re

def list_mapper(mapper, lst):
    return list(map(mapper, lst))

def remove_comments(latex: str) -> str:
    r"""
    Removes the comments from the latex. 

    Parameters
    ----------
    latex : str

    Returns
    -------
    str 
        The latex with the comments removed. 
    """
    return re.sub(r"%.+", "", latex)


def replace_to_mathjax(latex: str) -> str:
    r"""
    Replaces $...$ with \(...\) and $$...$$ with \[...\]. 
    Wraps the align and align* environments with \[...\].
    Replaces the equation environment with \[...\]. 
    
    Parameters
    ----------
    latex : str 

    Returns
    -------
    str 
        The latex with the replacements made. 
    """
    
    def senv(env_name: str):
        def inner(latex: str) -> str:
            return r"\begin{" + env_name + "}" + latex + r"\end{" + env_name + "}"
        return inner
    
    def mtp(maker): 
        def inner(latex: str) -> tuple:
            return (latex, maker(latex))
        return inner 

    block_equations = []

    envs = ["align", "align\\*", "equation", "equation\\*", "gather", "gather\\*"]

    for env in envs:
        block_equations += list_mapper(mtp(senv(env)), get_environments(latex, env))

    # $$...$$ 
    beqmapper = lambda x: (x, r"$$" + x + r"$$")

    block_equations += list_mapper(beqmapper, re.findall(r"\$\$(.*?)\$\$", latex, re.DOTALL))

    # replaces the block equations with a placeholder
    for i, block_equation in enumerate(block_equations):
        latex = latex.replace(block_equation[1], "¡¡¡block_equation_" + str(i)
                              + "!!!")

    # replaces $...$ with \(...\)
    latex = re.sub(r"\$(.+?)\$", r"\\\(\1\\\)", latex)
    
    # replace back the block equations, with environments removed 
    for i, block_equation in enumerate(block_equations):
        latex = latex.replace("¡¡¡block_equation_" + str(i) + "!!!", 
                              r"\[" + block_equation[0] + r"\]")

    return latex


def remove_leading_whitespace(latex: str) -> str:
    r"""
    Removes the leading whitespace from each line in the latex. 

    Parameters
    ----------
    latex : str

    Returns
    -------
    str 
        The latex with the leading whitespace removed. 
    """
    return re.sub(r"^\s+", "", latex, flags=re.MULTILINE)


def get_environments(latex: str, env_name: str) -> list:
    r"""
    Parses the latex and extracts the contents of all the environment with the
    given env_name. 

    Note that the \begin{env_name} and \end{env_name} are not included.

    Parameters
    ----------
    latex : str
    env_name : str 

    Returns
    -------
    list 
        The contents of the environment with the given env_name. 
    """
    reg_str = r"\\begin{" + env_name + r"}(.*?)\\end{" + env_name + r"}"
    env_regex = re.compile(reg_str, re.DOTALL)
    return list(map(mapping_sequence, env_regex.findall(latex))) 


def mapping_sequence(latex: str) -> str: 
    """
    Maps the sequence of the latex to the sequence of the mathjax. 

    Parameters
    ----------
    latex : str 

    Returns
    -------
    str 
        The sequence of the mathjax. 
    """
    latex = remove_leading_whitespace(latex)
    latex = replace_to_mathjax(latex)
    latex = remove_comments(latex)
    return latex

if __name__ == "__main__":
    test_latex = r"""
    \begin{test}
        This is the inner contents.
        This is the second line.
        \begin{align}
            f(x) &= x^2 \\
        \end{align}
    \end{test}
    """
    envs = get_environments(test_latex, "test")

    for env in envs:
        print(env)
