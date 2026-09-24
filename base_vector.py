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
    Estrutura vetorial customizada que simula um registrador contínuo.
    Armazena o número como um único vetor de dígitos isolados e 
    utiliza um ponteiro para a posição da vírgula (radix point).
    """
    def __init__(self, base: int, sign: str = '+'):
        if base < 2 or base > 36:
            raise ValueError("A base deve estar entre 2 e 36.")
        
        self.base = base
        self.sign = sign
        
        # O Registrador: Um único vetor contínuo de caracteres
        # Ex: Para 12.5 -> digits = ['1', '2', '5']
        self.digits = [] 
        
        # Posição da vírgula (índice no vetor onde termina a parte inteira)
        # Ex: Para 12.5 -> comma_position = 2 (a vírgula está após o 2º dígito)
        self.comma_position = 0 
        
        self.mapper = CharMapper()

    def from_string(self, number_str: str):
        """Popula a estrutura em um vetor contínuo, anotando a posição da vírgula."""
        number_str = number_str.strip().upper()
        if not number_str:
            raise ValueError("String vazia fornecida.")

        if number_str[0] in ['+', '-']:
            self.sign = number_str[0]
            number_str = number_str[1:]
        else:
            self.sign = '+'

        parts = number_str.split('.')
        if len(parts) > 2:
            raise ValueError("O número possui mais de um separador decimal.")

        int_str = parts[0] if parts[0] else "0"
        frac_str = parts[1] if len(parts) == 2 else ""

        self.digits = []
        
        # Preenche o vetor contínuo com todos os dígitos juntos
        for char in int_str + frac_str:
            val = self.mapper.get_value(char)
            if val >= self.base:
                raise ValueError(f"Dígito '{char}' é inválido para a base {self.base}.")
            self.digits.append(char)
            
        # A posição da vírgula é exatamente o tamanho do bloco inteiro na string original
        self.comma_position = len(int_str)

    def __str__(self):
        """Reconstrução visual fatiando o vetor único pela posição da vírgula."""
        int_part = "".join(self.digits[:self.comma_position])
        if not int_part:
            int_part = "0"
            
        frac_part = "".join(self.digits[self.comma_position:])
        
        sinal_str = "-" if self.sign == '-' else ""
        frac_str_formatada = f".{frac_part}" if frac_part else ""
            
        return f"{sinal_str}{int_part}{frac_str_formatada} (Base {self.base})"
