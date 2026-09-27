from base_vector import FloatVector, CharMapper
from arithmetic_tables import ArithmeticTables
from vector_math import VectorMath

class DirectOperations:
    """
    Controlador de alto nível para operações de ponto flutuante com sinais.
    Delega a aritmética matemática bruta para o VectorMath (Princípio DRY).
    """
    def __init__(self, base: int, mapper: CharMapper = None):
        self.base = base
        self.mapper = mapper or CharMapper()
        self.tables = ArithmeticTables(base, self.mapper)
        self.math = VectorMath(self.tables)

    def _align_vectors(self, vec_a: FloatVector, vec_b: FloatVector) -> tuple[list[str], list[str], int]:
        int_a = vec_a.digits[:vec_a.comma_position]
        int_b = vec_b.digits[:vec_b.comma_position]
        max_int = max(len(int_a), len(int_b))
        
        int_a_aligned = ['0'] * (max_int - len(int_a)) + int_a
        int_b_aligned = ['0'] * (max_int - len(int_b)) + int_b
        
        frac_a = vec_a.digits[vec_a.comma_position:]
        frac_b = vec_b.digits[vec_b.comma_position:]
        max_frac = max(len(frac_a), len(frac_b))
        
        frac_a_aligned = frac_a + ['0'] * (max_frac - len(frac_a))
        frac_b_aligned = frac_b + ['0'] * (max_frac - len(frac_b))
        
        aligned_a = int_a_aligned + frac_a_aligned
        aligned_b = int_b_aligned + frac_b_aligned
        
        return aligned_a, aligned_b, max_frac

    def _format_result(self, res_dig: list[str], frac_len: int, sign: str) -> FloatVector:
        comma = len(res_dig) - frac_len
        
        # Insere zeros à esquerda se a vírgula ficou negativa ou na ponta (ex: .10)
        while comma <= 0:
            res_dig.insert(0, '0')
            comma += 1
            
        # Remove zeros excedentes à esquerda da parte inteira (preservando o 0 antes da vírgula)
        while comma > 1 and res_dig[0] == '0':
            res_dig.pop(0)
            comma -= 1
            
        # Remove zeros redundantes na parte fracionária
        while len(res_dig) > comma and res_dig[-1] == '0':
            res_dig.pop()
            
        res = FloatVector(self.base)
        res.digits = res_dig
        res.comma_position = comma
        res.sign = '+' if all(d == '0' for d in res_dig) else sign
        return res

    def add(self, vec_a: FloatVector, vec_b: FloatVector) -> FloatVector:
        if vec_a.base != vec_b.base: raise ValueError("Operandos devem estar na mesma base.")
        a_dig, b_dig, frac_len = self._align_vectors(vec_a, vec_b)
        
        if vec_a.sign == vec_b.sign:
            res_dig = self.math.add(a_dig, b_dig)
            sign = vec_a.sign
        else:
            if self.math.is_greater_or_equal(a_dig, b_dig):
                res_dig = self.math.sub(a_dig, b_dig)
                sign = vec_a.sign
            else:
                res_dig = self.math.sub(b_dig, a_dig)
                sign = vec_b.sign
                
        return self._format_result(res_dig, frac_len, sign)

    def sub(self, vec_a: FloatVector, vec_b: FloatVector) -> FloatVector:
        neg_b = FloatVector(self.base, '-' if vec_b.sign == '+' else '+')
        neg_b.digits = vec_b.digits.copy()
        neg_b.comma_position = vec_b.comma_position
        return self.add(vec_a, neg_b)

    def mul(self, vec_a: FloatVector, vec_b: FloatVector) -> FloatVector:
        if vec_a.base != vec_b.base: raise ValueError("Operandos devem estar na mesma base.")
        
        res_dig = self.math.mul(vec_a.digits, vec_b.digits)
        frac_len = (len(vec_a.digits) - vec_a.comma_position) + (len(vec_b.digits) - vec_b.comma_position)
        sign = '+' if vec_a.sign == vec_b.sign else '-'
        
        return self._format_result(res_dig, frac_len, sign)

    def div(self, vec_a: FloatVector, vec_b: FloatVector, max_precision=10) -> FloatVector:
        if vec_a.base != vec_b.base: raise ValueError("Operandos devem estar na mesma base.")
        if all(d == '0' for d in vec_b.digits): raise ZeroDivisionError("Divisão por zero.")

        # Desloca as vírgulas até o divisor ser estritamente inteiro
        frac_b_len = len(vec_b.digits) - vec_b.comma_position
        a_dig = vec_a.digits.copy()
        a_comma = vec_a.comma_position + frac_b_len
        while a_comma > len(a_dig):
            a_dig.append('0')
            
        b_dig = vec_b.digits.copy()
        
        res_dig = []
        partial_div = []
        idx_a = 0
        comma_placed = False
        res_comma = 0
        
        # Executa a divisão vetorial longa (Chave da Divisão)
        while idx_a < len(a_dig) or (len(partial_div) > 0 and not (len(partial_div)==1 and partial_div[0]=='0') and len(res_dig) - res_comma < max_precision):
            if idx_a == a_comma:
                res_comma = len(res_dig)
                comma_placed = True
                
            if idx_a < len(a_dig):
                partial_div.append(a_dig[idx_a])
            else:
                if not comma_placed:
                    res_comma = len(res_dig)
                    comma_placed = True
                partial_div.append('0')
                
            # Limpa zeros no início do dividendo parcial para otimizar
            while len(partial_div) > 1 and partial_div[0] == '0': partial_div.pop(0)
            
            best_q = '0'
            best_prod = ['0']
            for val_q in range(1, self.base):
                q_char = self.mapper.get_char(val_q)
                prod = self.math.mul_digit(b_dig, q_char)
                if self.math.is_greater_or_equal(partial_div, prod):
                    best_q = q_char
                    best_prod = prod
                else:
                    break
                    
            res_dig.append(best_q)
            partial_div = self.math.sub(partial_div, best_prod)
            idx_a += 1
            
        if not comma_placed:
            res_comma = len(res_dig)
            
        sign = '+' if vec_a.sign == vec_b.sign else '-'
        frac_len = len(res_dig) - res_comma
        
        return self._format_result(res_dig, frac_len, sign)
