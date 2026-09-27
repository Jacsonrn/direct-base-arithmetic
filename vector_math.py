from arithmetic_tables import ArithmeticTables

class VectorMath:
    """
    Agrupa operações matemáticas armadas de vetores de dígitos,
    utilizando a Unidade Lógica e Aritmética (ALU) carregada.
    """
    def __init__(self, tables: ArithmeticTables):
        self.tables = tables

    def add(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        """Soma armada da direita para a esquerda usando as tabelas da ALU."""
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

    def mul_digit(self, vec: list[str], digit: str) -> list[str]:
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

    def mul(self, vec_a: list[str], vec_b: list[str]) -> list[str]:
        """Multiplicação armada completa entre dois vetores."""
        result = ['0']
        for i, digit in enumerate(reversed(vec_b)):
            temp = self.mul_digit(vec_a, digit)
            if temp != ['0']:
                temp.extend(['0'] * i)
            result = self.add(result, temp)
        return result
