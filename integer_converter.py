from base_vector import CharMapper
from arithmetic_tables import ArithmeticTables

class IntegerConverter:
    """
    Realiza a conversão direta da parte inteira de um número entre duas bases 
    utilizando a Aritmética Polinomial (Método de Horner).
    Toda a matemática é executada nativamente na base de destino.
    """
    def __init__(self, dest_base: int, mapper: CharMapper):
        self.dest_base = dest_base
        self.mapper = mapper
        # A nossa ALU carregada com a tabuada da base de destino!
        self.tables = ArithmeticTables(dest_base, mapper)

    def convert(self, source_digits: list[str], source_base: int) -> list[str]:
        """
        Converte um vetor de dígitos inteiros da source_base para a dest_base.
        Ex: converte ['1', 'A'] da Base 16 para a Base 2.
        """
        if not source_digits or source_digits == ['0']:
            return ['0']

        # O resultado acumulado (começa em zero na base destino)
        result = ['0']
        
        # Converte a base de origem para um vetor na base destino
        # Ex: se a source_base for 16, e a dest_base for 2, isso gera ['1', '0', '0', '0', '0']
        base_from_vec = self._small_int_to_vector(source_base)

        for digit in source_digits:
            # 1. Converte o dígito atual para um vetor na base destino
            digit_val = self.mapper.get_value(digit)
            digit_vec = self._small_int_to_vector(digit_val)
            
            # 2. Horner: Result = (Result * source_base) + digit
            # Perceba que as contas usam as NOSSAS funções matemáticas de vetores!
            temp_mul = self._vector_mul(result, base_from_vec)
            result = self._vector_add(temp_mul, digit_vec)
            
        return result

    def _small_int_to_vector(self, val: int) -> list[str]:
        """Converte pequenos inteiros (como os parâmetros da base) para vetor."""
        if val == 0: return ['0']
        res = []
        while val > 0:
            res.insert(0, self.mapper.get_char(val % self.dest_base))
            val //= self.dest_base
        return res

    # ---------------------------------------------------------
    # OPERAÇÕES MATEMÁTICAS "ARMADAS" (Soma e Multiplicação de Vetores)
    # ---------------------------------------------------------
    def _vector_add(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        """Soma armada da direita para a esquerda usando as tabelas da ALU."""
        max_len = max(len(vec_a), len(vec_b))
        # Alinha com zeros à esquerda
        a = ['0'] * (max_len - len(vec_a)) + vec_a
        b = ['0'] * (max_len - len(vec_b)) + vec_b
        
        result = []
        carry = '0'
        
        for i in range(max_len - 1, -1, -1):
            # Soma os dois dígitos e depois soma o "vai-um"
            c1, sum1 = self.tables.lookup_add(a[i], b[i])
            c2, final_sum = self.tables.lookup_add(sum1, carry)
            
            # O novo carry
            _, final_carry = self.tables.lookup_add(c1, c2)
            
            result.insert(0, final_sum)
            carry = final_carry
            
        if carry != '0':
            result.insert(0, carry)
            
        # Limpa os zeros à esquerda do resultado
        while len(result) > 1 and result[0] == '0':
            result.pop(0)
            
        return result

    def _vector_mul_digit(self, vec: list[str], digit: str) -> list[str]:
        """Multiplica um vetor por um ÚNICO dígito."""
        if digit == '0': return ['0']
        result = []
        carry = '0'
        for i in range(len(vec) - 1, -1, -1):
            c1, prod = self.tables.lookup_mul(vec[i], digit)
            c2, final_sum = self.tables.lookup_add(prod, carry)
            _, final_carry = self.tables.lookup_add(c1, c2)
            result.insert(0, final_sum)
            carry = final_carry
            
        if carry != '0':
            result.insert(0, carry)
        return result

    def _vector_mul(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        """Multiplicação armada completa entre dois vetores."""
        result = ['0']
        for i, digit in enumerate(reversed(vec_b)):
            # Multiplica e adiciona os zeros à direita (deslocamento posicional)
            temp = self._vector_mul_digit(vec_a, digit)
            if temp != ['0']:
                temp.extend(['0'] * i)
            result = self._vector_add(result, temp)
        return result
