from base_vector import CharMapper

class ArithmeticTables:
    """
    Gera tabelas estáticas (dicionários) de adição e multiplicação para uma base específica.
    Simula a Unidade Lógica e Aritmética (ALU) nativa de um processador operando
    exclusivamente com símbolos da base fornecida.
    """
    def __init__(self, base: int, mapper: CharMapper):
        if base < 2 or base > 36:
            raise ValueError("A base deve estar entre 2 e 36.")
            
        self.base = base
        self.mapper = mapper
        
        # Dicionários onde a chave é uma tupla de caracteres, ex: ('5', '4')
        # O valor será uma tupla com (carry_char, result_char)
        self.add_table = {}
        self.mul_table = {}
        
        self._generate_tables()
        
    def _generate_tables(self):
        # Pega todos os símbolos válidos para esta base (ex: Base 3 -> ['0', '1', '2'])
        valid_chars = [self.mapper.get_char(i) for i in range(self.base)]
        
        for a in valid_chars:
            for b in valid_chars:
                val_a = self.mapper.get_value(a)
                val_b = self.mapper.get_value(b)
                
                # Pré-computa a ADIÇÃO
                sum_val = val_a + val_b
                carry_add = sum_val // self.base  # Divisão inteira: o "vai-um"
                rem_add = sum_val % self.base     # Resto: o dígito que fica
                self.add_table[(a, b)] = (self.mapper.get_char(carry_add), self.mapper.get_char(rem_add))
                
                # Pré-computa a MULTIPLICAÇÃO
                mul_val = val_a * val_b
                carry_mul = mul_val // self.base
                rem_mul = mul_val % self.base
                self.mul_table[(a, b)] = (self.mapper.get_char(carry_mul), self.mapper.get_char(rem_mul))

    def lookup_add(self, char_a: str, char_b: str) -> tuple[str, str]:
        """Retorna o (carry, resultado) da soma de dois dígitos."""
        char_a = char_a.upper()
        char_b = char_b.upper()
        return self.add_table[(char_a, char_b)]

    def lookup_mul(self, char_a: str, char_b: str) -> tuple[str, str]:
        """Retorna o (carry, resultado) da multiplicação de dois dígitos."""
        char_a = char_a.upper()
        char_b = char_b.upper()
        return self.mul_table[(char_a, char_b)]
