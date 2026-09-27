from base_vector import CharMapper
from arithmetic_tables import ArithmeticTables
from vector_math import VectorMath

class IntegerConverter:
    """
    Realiza a conversão direta da parte inteira de um número entre duas bases 
    utilizando a Aritmética Polinomial (Método de Horner).
    Toda a matemática é executada nativamente na base de destino.
    """
    def __init__(self, dest_base: int, mapper: CharMapper):
        self.dest_base = dest_base
        self.mapper = mapper
        # A nossa ALU carregada com a tabuada da base de destino
        self.tables = ArithmeticTables(dest_base, mapper)
        self.math = VectorMath(self.tables)

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
        base_from_vec = self._small_int_to_vector(source_base)

        for digit in source_digits:
            digit_val = self.mapper.get_value(digit)
            digit_vec = self._small_int_to_vector(digit_val)
            
            # Horner: Result = (Result * source_base) + digit
            temp_mul = self.math.mul(result, base_from_vec)
            result = self.math.add(temp_mul, digit_vec)
            
        return result

    def _small_int_to_vector(self, val: int) -> list[str]:
        """Converte pequenos inteiros (como os parâmetros da base) para vetor."""
        if val == 0: return ['0']
        res = []
        while val > 0:
            res.insert(0, self.mapper.get_char(val % self.dest_base))
            val //= self.dest_base
        return res
