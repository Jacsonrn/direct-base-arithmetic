class CharMapper:
    """
    Classe responsável pelo mapeamento dinâmico de caracteres numéricos e alfabéticos
    para seus respectivos pesos (valores inteiros) e vice-versa.
    Suporta bases de 2 até 36 (alfabeto 0-9 e A-Z).
    """
    def __init__(self):
        # Dicionários de mapeamento bidirecional
        self.char_to_val = {}
        self.val_to_char = {}
        self._initialize_mapping()

    def _initialize_mapping(self):
        # Mapeia numerais (0-9)
        for i in range(10):
            self.char_to_val[str(i)] = i
            self.val_to_char[i] = str(i)
        
        # Mapeia letras (A-Z) para valores de 10 a 35
        for i in range(26):
            char = chr(ord('A') + i)
            val = 10 + i
            self.char_to_val[char] = val
            self.val_to_char[val] = char

    def get_value(self, char: str) -> int:
        char = char.upper()
        if char not in self.char_to_val:
            raise ValueError(f"Caractere inválido ou não suportado: '{char}'")
        return self.char_to_val[char]

    def get_char(self, value: int) -> str:
        if value not in self.val_to_char:
            raise ValueError(f"Valor sem representação de caractere mapeada: {value}")
        return self.val_to_char[value]


class FloatVector:
    """
    Estrutura vetorial customizada que simula um registrador para armazenar 
    números reais em uma base arbitrária B >= 2.
    NÃO utiliza int ou float para representar a grandeza completa do número.
    """
    def __init__(self, base: int, sign: str = '+'):
        if base < 2 or base > 36:
            raise ValueError("A base deve estar entre 2 e 36.")
        
        self.base = base
        self.sign = sign  # '+' ou '-'
        
        # Vetores de dígitos (strings de tamanho 1) simulando posições de memória
        self.integer_part = []     # Ex: ['1', 'A', '3']
        self.fractional_part = []  # Ex: ['F', '2']
        
        self.mapper = CharMapper()

    def from_string(self, number_str: str):
        """
        Popula a estrutura vetorial interpretando uma string do número.
        Isola as partes e valida estritamente contra a base selecionada.
        """
        number_str = number_str.strip().upper()
        if not number_str:
            raise ValueError("String vazia fornecida.")

        # Tratamento de sinal
        if number_str[0] in ['+', '-']:
            self.sign = number_str[0]
            number_str = number_str[1:]
        else:
            self.sign = '+'

        # Separação decimal
        parts = number_str.split('.')
        if len(parts) > 2:
            raise ValueError("O número possui mais de um separador decimal (vírgula/ponto).")

        # Processamento do vetor inteiro
        int_str = parts[0] if parts[0] else "0"
        self.integer_part = []
        for char in int_str:
            val = self.mapper.get_value(char)
            if val >= self.base:
                raise ValueError(f"Dígito '{char}' é inválido ou excede a base {self.base}.")
            self.integer_part.append(char)

        # Processamento do vetor fracionário
        self.fractional_part = []
        if len(parts) == 2:
            frac_str = parts[1]
            for char in frac_str:
                val = self.mapper.get_value(char)
                if val >= self.base:
                    raise ValueError(f"Dígito '{char}' é inválido ou excede a base {self.base}.")
                self.fractional_part.append(char)

    def __str__(self):
        """Reconstrução visual do vetor para fins de log/debug."""
        int_str = "".join(self.integer_part) if self.integer_part else "0"
        frac_str = "".join(self.fractional_part)
        
        sinal_str = "-" if self.sign == '-' else ""
        frac_str_formatada = f".{frac_str}" if frac_str else ""
            
        return f"{sinal_str}{int_str}{frac_str_formatada} (Base {self.base})"
