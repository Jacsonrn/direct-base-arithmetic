from base_vector import FloatVector, CharMapper
from arithmetic_tables import ArithmeticTables

class DirectOperations:
    """
    Realiza adição e subtração de números reais (FloatVector)
    nativamente na base especificada, simulando hardware real.
    """
    def __init__(self, base: int, mapper: CharMapper = None):
        self.base = base
        self.mapper = mapper or CharMapper()
        self.tables = ArithmeticTables(base, self.mapper)

    def align_vectors(self, vec_a: FloatVector, vec_b: FloatVector) -> tuple[list[str], list[str], int]:
        """
        Alinha as vírgulas de dois FloatVectors preenchendo com zeros (zero-padding).
        Retorna (dígitos_a, dígitos_b, nova_posicao_virgula).
        """
        # Parte Inteira (zeros à esquerda)
        int_a = vec_a.digits[:vec_a.comma_position]
        int_b = vec_b.digits[:vec_b.comma_position]
        max_int = max(len(int_a), len(int_b))
        
        int_a_aligned = ['0'] * (max_int - len(int_a)) + int_a
        int_b_aligned = ['0'] * (max_int - len(int_b)) + int_b
        
        # Parte Fracionária (zeros à direita)
        frac_a = vec_a.digits[vec_a.comma_position:]
        frac_b = vec_b.digits[vec_b.comma_position:]
        max_frac = max(len(frac_a), len(frac_b))
        
        frac_a_aligned = frac_a + ['0'] * (max_frac - len(frac_a))
        frac_b_aligned = frac_b + ['0'] * (max_frac - len(frac_b))
        
        aligned_a = int_a_aligned + frac_a_aligned
        aligned_b = int_b_aligned + frac_b_aligned
        
        return aligned_a, aligned_b, max_int

    def is_greater_or_equal_abs(self, a_digits: list[str], b_digits: list[str]) -> bool:
        """
        Verifica se o módulo do vetor A é maior ou igual ao módulo do vetor B.
        Os vetores já devem estar alinhados!
        """
        for a, b in zip(a_digits, b_digits):
            val_a = self.mapper.get_value(a)
            val_b = self.mapper.get_value(b)
            if val_a > val_b: return True
            if val_a < val_b: return False
        return True # São exatamente iguais

    def _unsigned_add(self, a_digits: list[str], b_digits: list[str], comma_pos: int) -> tuple[list[str], int]:
        """Soma vetorial sem sinal armada da direita para a esquerda."""
        result = []
        carry = '0'
        for i in range(len(a_digits) - 1, -1, -1):
            c1, sum1 = self.tables.lookup_add(a_digits[i], b_digits[i])
            c2, final_sum = self.tables.lookup_add(sum1, carry)
            
            # O novo carry nunca transborda o '1' numa soma de dois números
            _, final_carry = self.tables.lookup_add(c1, c2)
            
            result.insert(0, final_sum)
            carry = final_carry
            
        new_comma = comma_pos
        if carry != '0':
            result.insert(0, carry)
            new_comma += 1
            
        return result, new_comma

    def _unsigned_sub(self, a_digits: list[str], b_digits: list[str], comma_pos: int) -> tuple[list[str], int]:
        """
        Subtração vetorial sem sinal: a - b. 
        PREMISSA MATEMÁTICA: garante-se que A >= B previamente.
        """
        result = []
        borrow = '0'
        
        for i in range(len(a_digits) - 1, -1, -1):
            # 1. Subtrai B de A
            b1, sub1 = self.tables.lookup_sub(a_digits[i], b_digits[i])
            # 2. Subtrai o borrow (que veio da casa anterior)
            b2, final_sub = self.tables.lookup_sub(sub1, borrow)
            
            # Acumula o novo borrow. A matemática prova que b1 e b2 nunca são 1 ao mesmo tempo.
            _, final_borrow = self.tables.lookup_add(b1, b2)
            
            result.insert(0, final_sub)
            borrow = final_borrow
            
        # Remove os zeros fantasmas à esquerda da parte inteira
        new_comma = comma_pos
        while new_comma > 1 and result[0] == '0':
            result.pop(0)
            new_comma -= 1
            
        return result, new_comma

    def _clean_fractional_zeros(self, digits: list[str], comma_pos: int) -> list[str]:
        """Remove zeros redundantes no final da fração (ex: 10.50 -> 10.5)."""
        while len(digits) > comma_pos and digits[-1] == '0':
            digits.pop()
        return digits

    def add(self, vec_a: FloatVector, vec_b: FloatVector) -> FloatVector:
        """Operação nativa de Adição: A + B"""
        if vec_a.base != vec_b.base:
            raise ValueError("Operandos devem estar na mesma base.")
            
        a_dig, b_dig, comma = self.align_vectors(vec_a, vec_b)
        res = FloatVector(self.base)
        
        if vec_a.sign == vec_b.sign:
            # Sinais iguais: soma as magnitudes e preserva o sinal
            res_dig, res_comma = self._unsigned_add(a_dig, b_dig, comma)
            res.sign = vec_a.sign
        else:
            # Sinais diferentes: cai numa subtração, preservando o sinal do maior
            if self.is_greater_or_equal_abs(a_dig, b_dig):
                res_dig, res_comma = self._unsigned_sub(a_dig, b_dig, comma)
                res.sign = vec_a.sign
            else:
                res_dig, res_comma = self._unsigned_sub(b_dig, a_dig, comma)
                res.sign = vec_b.sign
                
        res_dig = self._clean_fractional_zeros(res_dig, res_comma)
        res.digits = res_dig
        res.comma_position = res_comma
        
        # Zero absoluto não tem sinal negativo
        if all(d == '0' for d in res.digits):
            res.sign = '+'
            
        return res

    def sub(self, vec_a: FloatVector, vec_b: FloatVector) -> FloatVector:
        """Operação nativa de Subtração: A - B"""
        # A - B é algebricamente equivalente a A + (-B).
        # Criamos um clone do operando B com o sinal invertido e chamamos a Adição.
        neg_b = FloatVector(self.base, '-' if vec_b.sign == '+' else '+')
        neg_b.digits = vec_b.digits.copy()
        neg_b.comma_position = vec_b.comma_position
        
        return self.add(vec_a, neg_b)
