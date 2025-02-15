class TokensNode:
    VARIABLE: str = "VARIABLE"
    NUMBER: str = "NUMBER"
    STRING: str = "STRING"
    PARENT: str = "PARENT"

    EVENT: str = "EVENT"
    SET_VARIABLE: str = "SET_VARIABLE"


    ACTION: str = "ACTION"
    VALUE: str = "VALUE"

    APPEND_BLOCK: str = "APPEND_BLOCK"
    CLOSE_LINE: str = "CLOSE_LINE"

    # Начало файла (Beginning of file)
    BOF: str = "BOF"

    # Конец файла (End of file)
    EOF: str = "EOF"
