from base_vector import CharMapper
from arithmetic_tables import ArithmeticTables
from vector_math import VectorMath

class FractionalConverter:
    """
    Realiza a conversão direta da parte fracionária entre duas bases
    por multiplicações sucessivas.
    Rastreia o histórico de restos para detectar dízimas periódicas nativas.
    """
    def __init__(self, source_base: int, mapper: CharMapper):
        self.source_base = source_base
        self.mapper = mapper
        # A ALU fracionária é instanciada na BASE DE ORIGEM!
        self.tables = ArithmeticTables(source_base, mapper)
        self.math = VectorMath(self.tables)

    def convert(self, frac_digits: list[str], dest_base: int, max_precision: int = 20) -> tuple[list[str], int]:
        """
        Converte a fração. Retorna (lista_de_digitos, indice_inicio_dizima).
        Se a fração terminar exata, o indice_inicio_dizima será -1.
        """
        if not frac_digits or self._normalize_frac_state(frac_digits) == "0":
            return ([], -1)

        result_digits = []
        
        # Converte a base de destino para um vetor representativo na base de origem
        dest_base_vec = self._small_int_to_vector(dest_base)

        # Caderninho de rastreamento para detectar as dízimas
        history = {}
        current_frac = frac_digits.copy()
        
        while True:
            state_key = self._normalize_frac_state(current_frac)
            
            if state_key == "0":
                # A conta terminou, fração exata!
                return (result_digits, -1)
                
            if state_key in history:
                # DÍZIMA PERIÓDICA DETECTADA!
                # Encontramos uma fração que já calculamos antes, entramos em loop infinito.
                return (result_digits, history[state_key])
                
            if len(result_digits) >= max_precision:
                # Limite de segurança de casas decimais
                return (result_digits, -1)

            # Anota o estado atual e a posição onde ele ocorreu
            history[state_key] = len(result_digits)

            # Multiplica a fração vetorial pela base de destino
            prod = self.math.mul(current_frac, dest_base_vec)
            
            # Separa o que transbordou para a parte inteira e a nova fração
            num_frac_places = len(current_frac)
            if len(prod) < num_frac_places:
                prod = ['0'] * (num_frac_places - len(prod)) + prod
                
            next_frac = prod[-num_frac_places:] if num_frac_places > 0 else []
            overflow_vec = prod[:-num_frac_places] if len(prod) > num_frac_places else ['0']
            
            if not overflow_vec: overflow_vec = ['0']
                
            # O que transbordou é o nosso novo dígito na base de destino
            overflow_val = self._vector_to_small_int(overflow_vec)
            result_digits.append(self.mapper.get_char(overflow_val))
            
            current_frac = next_frac

    def _normalize_frac_state(self, vec: list[str]) -> str:
        """Remove zeros à direita. '50' é o mesmo estado que '5' matematicamente."""
        v = vec.copy()
        while len(v) > 0 and v[-1] == '0':
            v.pop()
        return "".join(v) if v else "0"

    def _small_int_to_vector(self, val: int) -> list[str]:
        if val == 0: return ['0']
        res = []
        while val > 0:
            res.insert(0, self.mapper.get_char(val % self.source_base))
            val //= self.source_base
        return res

    def _vector_to_small_int(self, vec: list[str]) -> int:
        """Lê o vetor de overflow e devolve seu peso nativo."""
        val = 0
        for char in vec:
            val = val * self.source_base + self.mapper.get_value(char)
        return val
