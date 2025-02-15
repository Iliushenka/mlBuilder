class TokensLexer:
    # Типы значений
    CODE: str = "CODE"
    NUMBER: str = "NUMBER"
    STRING: str = "STRING"
    VARIABLE: str = "VARIABLE"

    PARENT: str = "PARENT"  # in ( [?] )

    # Операции
    PLUS: str = "PLUS"  # +
    MINUS: str = "MINUS"  # -
    MULTIPLY: str = "MULTIPLY"  # *
    DIVISION: str = "DIVISION"  # /

    POWER: str = "POWER" # ^

    # Скобки
    OPEN_BRACE = "OPEN_BRACE"  # <
    CLOSE_BRACE = "CLOSE_BRACE"  # >

    OPEN_PARENT = "OPEN_PARENT"  # (
    CLOSE_PARENT = "CLOSE_PARENT"  # )

    OPEN_BRACKET = "OPEN_BRACKET"  # {
    CLOSE_BRACKET = "CLOSE_BRACKET"  # }

    # Дополнительные символы
    DOT: str = "DOT"  # .
    COMMA: str = "COMMA"  # ,
    SEMICOLON: str = "SEMICOLON"  # ;
    COLON: str = "COLON"  # :
    ASSIGN: str = "ASSIGN"  # =

    # Конец файла
    EOF: str = "EOF"
