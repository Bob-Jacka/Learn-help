from typing import Final


class Syntax_rules:
    """
    Syntax rules for suits
    """
    # suit file consts:
    global_import_directive: Final[str] = '.Import_global'
    local_import_directive: Final[str] = '.Import_local'
    function_directive: Final[str] = '$Func'
    comment_symbol: Final[str] = '#'

    # all file config:
    variable_prefix: Final[str] = 'Var'
    path_prefix: Final[str] = 'Path'