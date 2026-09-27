from base_vector import FloatVector, CharMapper
from integer_converter import IntegerConverter
from fractional_converter import FractionalConverter

class DirectConverter:
    """
    Integra a conversão da parte inteira e fracionária, fornecendo
    suporte completo a números reais (x ∈ R).
    """
    def __init__(self, mapper: CharMapper = None):
        self.mapper = mapper or CharMapper()

    def convert_real(self, number_str: str, source_base: int, dest_base: int, max_precision: int = 20) -> tuple[FloatVector, int]:
        """
        Converte um número real em string da source_base para a dest_base.
        Retorna o novo FloatVector e o índice onde começa a dízima (-1 se exata).
        """
        # 1. Parse na base de origem
        source_vec = FloatVector(source_base)
        source_vec.from_string(number_str)

        # 2. Converte a Parte Inteira (Horner na Base Destino)
        int_conv = IntegerConverter(dest_base, self.mapper)
        
        # Isola a parte inteira usando o nosso ponteiro de vírgula (radix point)
        int_digits_src = source_vec.digits[:source_vec.comma_position]
        if not int_digits_src:
            int_digits_src = ['0']
            
        int_digits_dest = int_conv.convert(int_digits_src, source_base)

        # 3. Converte a Parte Fracionária (Multiplicações na Base Origem)
        frac_conv = FractionalConverter(source_base, self.mapper)
        
        frac_digits_src = source_vec.digits[source_vec.comma_position:]
        frac_digits_dest, cycle_start = frac_conv.convert(frac_digits_src, dest_base, max_precision)

        # 4. Monta o Vetor Final (Base Destino) e ajusta a posição da vírgula
        dest_vec = FloatVector(dest_base, source_vec.sign)
        dest_vec.digits = int_digits_dest + frac_digits_dest
        dest_vec.comma_position = len(int_digits_dest)

        return dest_vec, cycle_start

    def format_output(self, vec: FloatVector, cycle_start: int) -> str:
        """Gera a string visual, envolvendo a dízima periódica nativa com parênteses."""
        int_part = "".join(vec.digits[:vec.comma_position])
        if not int_part:
            int_part = "0"
            
        frac_part = "".join(vec.digits[vec.comma_position:])
        
        if cycle_start != -1:
            # Temos uma dízima! Envolve o período que se repete com parênteses.
            non_repeating = frac_part[:cycle_start]
            repeating = frac_part[cycle_start:]
            frac_part = f"{non_repeating}({repeating})"
            
        sinal_str = "-" if vec.sign == '-' else ""
        frac_str_formatada = f".{frac_part}" if frac_part else ""
            
        return f"{sinal_str}{int_part}{frac_str_formatada} (Base {vec.base})"
