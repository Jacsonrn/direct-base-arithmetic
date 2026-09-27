from arithmetic_tables import ArithmeticTables

class VectorMath:
    """
    Agrupa operações matemáticas armadas de vetores de dígitos (inteiros absolutos sem sinal),
    utilizando a Unidade Lógica e Aritmética (ALU) carregada.
    """
    def __init__(self, tables: ArithmeticTables):
        self.tables = tables

    def add(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        max_len = max(len(vec_a), len(vec_b))
        a = ['0'] * (max_len - len(vec_a)) + vec_a
        b = ['0'] * (max_len - len(vec_b)) + vec_b
        
        result = []
        carry = '0'
        for i in range(max_len - 1, -1, -1):
            c1, sum1 = self.tables.lookup_add(a[i], b[i])
            c2, final_sum = self.tables.lookup_add(sum1, carry)
            _, final_carry = self.tables.lookup_add(c1, c2)
            result.insert(0, final_sum)
            carry = final_carry
            
        if carry != '0':
            result.insert(0, carry)
            
        while len(result) > 1 and result[0] == '0':
            result.pop(0)
            
        return result

    def sub(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        """Subtração armada (vec_a - vec_b). Premissa: vec_a >= vec_b."""
        max_len = max(len(vec_a), len(vec_b))
        a = ['0'] * (max_len - len(vec_a)) + vec_a
        b = ['0'] * (max_len - len(vec_b)) + vec_b
        
        result = []
        borrow = '0'
        for i in range(max_len - 1, -1, -1):
            b1, sub1 = self.tables.lookup_sub(a[i], b[i])
            b2, final_sub = self.tables.lookup_sub(sub1, borrow)
            _, final_borrow = self.tables.lookup_add(b1, b2)
            result.insert(0, final_sub)
            borrow = final_borrow
            
        while len(result) > 1 and result[0] == '0':
            result.pop(0)
            
        return result

    def mul_digit(self, vec: list[str], digit: str) -> list[str]:
        if digit == '0': return ['0']
        if digit == '1': return vec.copy()
        
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

    def mul(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        result = ['0']
        for i, digit in enumerate(reversed(vec_b)):
            if digit == '0': continue
            temp = self.mul_digit(vec_a, digit)
            temp.extend(['0'] * i)
            result = self.add(result, temp)
        return result

    def is_greater_or_equal(self, vec_a: list[str], vec_b: list[str]) -> bool:
        """Compara o valor absoluto de dois inteiros vetoriais."""
        a = vec_a.copy()
        b = vec_b.copy()
        while len(a) > 1 and a[0] == '0': a.pop(0)
        while len(b) > 1 and b[0] == '0': b.pop(0)
        
        if len(a) > len(b): return True
        if len(a) < len(b): return False
        
        for x, y in zip(a, b):
            val_x = self.tables.mapper.get_value(x)
            val_y = self.tables.mapper.get_value(y)
            if val_x > val_y: return True
            if val_x < val_y: return False
        return True
