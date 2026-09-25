# Fundamentação Teórica — Projeto U1: Aritmética Direta em Bases Arbitrárias

---

## Dia 01: Arquitetura da Estrutura Vetorial e Mapeamento de Caracteres

### 1.1 Sistemas de Numeração Posicional

Todo sistema de numeração que utilizamos no cotidiano é **posicional**. Isso significa que o **valor** de cada algarismo depende de duas coisas: o seu **peso intrínseco** (qual símbolo ele é) e a sua **posição** dentro do número.

A fórmula geral que rege qualquer sistema posicional é:

$$
N = \sum_{i=-f}^{n-1} d_i \cdot B^i
$$

Onde:
- $N$ é o valor numérico representado.
- $d_i$ é o dígito na posição $i$.
- $B$ é a **base** (ou **radix**) do sistema numérico ($B \ge 2$).
- $n$ é a quantidade de dígitos na parte inteira.
- $f$ é a quantidade de dígitos na parte fracionária.

**Exemplo prático (Base 10):** O número $372.5_{10}$ é decomposto como:

$$
3 \cdot 10^2 + 7 \cdot 10^1 + 2 \cdot 10^0 + 5 \cdot 10^{-1} = 300 + 70 + 2 + 0.5 = 372.5
$$

**Exemplo prático (Base 16 — Hexadecimal):** O número $\text{1A3.F}_{16}$ é decomposto como:

$$
1 \cdot 16^2 + 10 \cdot 16^1 + 3 \cdot 16^0 + 15 \cdot 16^{-1} = 256 + 160 + 3 + 0.9375 = 419.9375_{10}
$$

Esse princípio é **universal**: funciona identicamente para qualquer base, desde que os símbolos (dígitos) respeitem o intervalo $[0, B-1]$.

### 1.2 O Alfabeto Simbólico e a Necessidade do Mapeamento Dinâmico

Na Base 10, usamos os símbolos `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}` — dez símbolos para dez valores possíveis por posição. Porém, quando a base excede 10, os algarismos arábicos não são suficientes. A convenção universalmente adotada em computação é estender o alfabeto com letras latinas maiúsculas:

| Símbolo | Valor | Símbolo | Valor | Símbolo | Valor |
|---------|-------|---------|-------|---------|-------|
| 0       | 0     | A       | 10    | K       | 20    |
| 1       | 1     | B       | 11    | L       | 21    |
| 2       | 2     | C       | 12    | M       | 22    |
| ...     | ...   | ...     | ...   | ...     | ...   |
| 9       | 9     | J       | 19    | Z       | 35    |

Isso nos dá suporte para bases de **2 até 36** ($10$ dígitos $+ 26$ letras $= 36$ símbolos).

#### 1.2.1 A Tabela ASCII e a Geração Programática

Em vez de codificar manualmente 36 mapeamentos em cadeias `if/elif`, o projeto utiliza a **tabela ASCII** (_American Standard Code for Information Interchange_). A tabela ASCII é um padrão de codificação que atribui um número inteiro único a cada caractere:

- `'A'` $\rightarrow$ código ASCII $65$
- `'B'` $\rightarrow$ código ASCII $66$
- `'Z'` $\rightarrow$ código ASCII $90$

As funções nativas `ord()` e `chr()` do Python permitem transitar entre caractere e código:
- `ord('A')` retorna `65`
- `chr(65)` retorna `'A'`

Assim, o laço `chr(ord('A') + i)` percorre o alfabeto inteiro de forma dinâmica. Essa abordagem é **escalável** e **livre de erros manuais**, simulando exatamente como um processador real interpreta caracteres a partir de suas posições na tabela de codificação.

#### 1.2.2 Dicionários Hash (Hash Maps) e Complexidade O(1)

Os mapeamentos são armazenados em **dicionários** (`dict` do Python), uma estrutura de dados que implementa internamente uma **tabela hash**. A tabela hash transforma a chave (ex: `'A'`) em um índice numérico através de uma **função de dispersão** (_hash function_), permitindo acesso em tempo constante $O(1)$ — ou seja, o tempo de busca não cresce mesmo que o dicionário contenha milhões de entradas.

O mapeamento é **bidirecional**:
- `char_to_val`: dado um caractere, retorna o peso numérico. Ex: `'A'` → `10`.
- `val_to_char`: dado um peso, retorna o caractere. Ex: `10` → `'A'`.

Essa bidirecionalidade é essencial porque durante a **conversão** precisamos traduzir nos dois sentidos: ler dígitos da entrada (caractere → valor) e escrever dígitos na saída (valor → caractere).

### 1.3 Estrutura Vetorial: Simulação de Registrador de Hardware

#### 1.3.1 Por Que Não Usar `int` e `float`?

As variáveis primitivas `int` e `float` da linguagem Python (e de qualquer linguagem de programação) delegam a representação numérica ao **hardware da CPU**, que opera nativamente em **base 2 (binário)**. Quando escrevemos `x = 255` em Python:
1. O interpretador converte a string `"255"` para um inteiro binário internamente.
2. O processador armazena esse valor como uma cadeia de bits: `11111111₂`.
3. Qualquer operação aritmética (soma, multiplicação) é executada pela **ALU** (_Arithmetic Logic Unit_) do processador em circuitos binários.

Isso significa que, se usássemos `int` para armazenar um número na Base 7 e fizéssemos operações nele, estaríamos **secretamente usando a Base 2 como intermediário** — violando frontalmente a restrição do projeto que exige **eliminação absoluta de bases intermediárias**.

Além disso, o tipo `float` do Python segue o padrão **IEEE 754** de ponto flutuante de 64 bits, que armazena o número com precisão limitada a aproximadamente 15-17 dígitos decimais significativos. Frações que são exatas em certas bases (como $0.1_{10}$) se tornam **dízimas infinitas na Base 2**, forçando o hardware a truncar, o que injeta **erros de arredondamento cumulativos** — o exato problema que este projeto se propõe a eliminar.

#### 1.3.2 O Modelo do Registrador Contínuo

Em processadores reais, um **registrador** é uma pequena unidade de armazenamento ultrarrápida dentro da CPU. Ele armazena os dados como uma **sequência contínua e linear de bits**, sem nenhuma separação física interna. Não há "gaveta para parte inteira" e "gaveta para parte fracionária" — há apenas uma fita contínua e um **metadado** auxiliar que indica onde a vírgula (ponto radix) está posicionada.

O projeto simula esse comportamento com a seguinte arquitetura:

```
Estrutura FloatVector:
┌──────────┬─────────────────────────────────┬──────────────────┐
│  sign    │  digits (vetor contínuo)        │ comma_position   │
│  '+'/'-' │  ['1', '2', '3', '4', '5']     │  3               │
└──────────┴─────────────────────────────────┴──────────────────┘
                                              ↑
                                    "A vírgula está após
                                     o 3º dígito"
                                    Leitura: 123.45
```

- **`sign`**: Armazena o sinal como um caractere (`'+'` ou `'-'`), sem uso de booleano numérico.
- **`digits`**: Uma lista Python onde cada elemento é uma string de tamanho 1, representando um **único dígito** do número. Os dígitos inteiros e fracionários coexistem **no mesmo vetor**, sem separação.
- **`comma_position`**: Um inteiro que funciona como **ponteiro** indicando quantos dígitos pertencem à parte inteira. Os dígitos a partir desta posição são a parte fracionária.

#### 1.3.3 Ponto Radix (Radix Point) e Vírgula Flutuante

O termo técnico para a "vírgula" ou "ponto decimal" em um sistema de numeração genérico é **ponto radix** (_radix point_). Em português, usamos "vírgula" por convenção, mas o conceito é independente da base.

O ponto radix divide conceitualmente o número em duas regiões:
- **À esquerda**: dígitos com pesos posicionais $B^0, B^1, B^2, \ldots$ (potências crescentes, valor inteiro).
- **À direita**: dígitos com pesos posicionais $B^{-1}, B^{-2}, B^{-3}, \ldots$ (potências negativas, valor fracionário).

Ao armazenar o ponto radix como uma **variável de posição** (`comma_position`) em vez de inserir fisicamente um caractere `'.'` no vetor, estamos replicando fielmente a técnica de **ponto flutuante** (_floating point_), onde a vírgula pode "flutuar" (mudar de posição) conforme as operações são realizadas — exatamente como nos registradores de hardware.

#### 1.3.4 Validação de Entrada e Barreira de Segurança

O método `from_string()` implementa uma **barreira de validação** que impede a inserção de dígitos inválidos para a base selecionada. Se um `FloatVector` é instanciado com `base=2` (binário), qualquer tentativa de inserir o caractere `'5'` resultará em uma exceção `ValueError`.

Essa validação opera da seguinte forma:
1. Isola o sinal (se presente).
2. Divide a string pelo separador `'.'`.
3. Para cada caractere, consulta o `CharMapper` para obter o peso numérico.
4. Compara o peso contra a base: se `peso >= base`, o dígito é inválido.

Esse padrão é análogo aos **circuitos de proteção** em hardware, que detectam estados ilegais e impedem a propagação de dados corrompidos pelo restante do sistema.

### 1.4 Princípios de Engenharia de Software Aplicados

#### 1.4.1 Separação de Responsabilidades (Single Responsibility Principle)

O Dia 1 produziu duas classes distintas:
- **`CharMapper`**: Responsabilidade única de traduzir entre símbolos e pesos.
- **`FloatVector`**: Responsabilidade única de armazenar e estruturar o número.

Esse padrão segue o **Princípio da Responsabilidade Única** (SRP, do SOLID), que afirma que cada módulo ou classe deve ter **uma, e apenas uma, razão para mudar**. Se amanhã decidirmos estender o alfabeto para suportar bases maiores que 36, apenas o `CharMapper` precisará ser modificado — o `FloatVector` permanecerá intacto.

#### 1.4.2 Encapsulamento e Abstração

O método `_initialize_mapping()` é prefixado com underscore (`_`), indicando que é um método **privado** por convenção. Isso sinaliza que o mundo externo não deve chamá-lo diretamente, apenas o construtor `__init__` o faz. Essa prática protege a integridade interna do objeto e expõe apenas as operações seguras (`get_value`, `get_char`) ao restante do sistema.

---

### 1.5 Dez Possíveis Perguntas do Professor — Dia 01

**Pergunta 1: Por que vocês não utilizaram variáveis `int` ou `float` para armazenar o número completo?**
> Porque os tipos primitivos `int` e `float` do Python delegam a representação ao hardware, que opera nativamente em Base 2 (binário). Usar `int` significaria converter secretamente o número para Base 2 na CPU, violando a restrição do projeto que proíbe bases intermediárias. Além disso, o tipo `float` segue o padrão IEEE 754 com precisão limitada a ~15 dígitos, o que introduziria erros de arredondamento cumulativos — exatamente o problema que o projeto visa eliminar. Por isso, representamos o número como um vetor de caracteres isolados onde cada elemento é um único dígito simbólico.

**Pergunta 2: O que é o Ponto Radix e por que vocês armazenam a posição da vírgula como um inteiro separado em vez de colocar um caractere `'.'` dentro do vetor?**
> O ponto radix (ou radix point) é o separador que divide a parte inteira da parte fracionária em qualquer sistema de numeração posicional. Armazenamos a posição como um inteiro separado (`comma_position`) por duas razões: (1) isso simula fielmente o comportamento real de registradores de hardware, que guardam apenas bits/dígitos em uma fita contínua e usam um metadado auxiliar para indicar onde a vírgula "flutua"; (2) isso facilita enormemente as operações aritméticas futuras, pois podemos deslocar a vírgula (incrementar/decrementar `comma_position`) sem precisar reorganizar fisicamente os elementos do vetor.

**Pergunta 3: Qual a complexidade computacional de buscar um caractere no `CharMapper`? Por que não usaram uma cadeia `if/elif`?**
> A busca no `CharMapper` opera em tempo constante $O(1)$ porque utilizamos dicionários hash do Python. Uma cadeia `if/elif` teria complexidade $O(n)$ no pior caso (teria que percorrer todas as 36 comparações até achar a última letra `'Z'`). Além disso, dicionários são mais limpos, mais escaláveis e menos propensos a erros manuais de digitação. A escolha também replica o conceito de **lookup tables** (tabelas de consulta) usado em hardware real.

**Pergunta 4: Como vocês garantem que um dígito inválido não entre no sistema? Por exemplo, se alguém tentar inserir `'G'` num número de Base 16?**
> O método `from_string()` implementa uma barreira de validação. Para cada caractere da string de entrada, ele consulta o `CharMapper` para obter o peso numérico do dígito e, em seguida, verifica se esse peso é menor que a base. Na Base 16, os dígitos válidos vão de 0 a F (pesos 0 a 15). O caractere `'G'` possui peso 16, que é $\ge 16$ (a base), portanto o sistema levanta uma exceção `ValueError` imediatamente, impedindo que dados corrompidos se propaguem.

**Pergunta 5: O que é a tabela ASCII e como vocês a utilizam para gerar o mapeamento de caracteres?**
> A tabela ASCII (American Standard Code for Information Interchange) é um padrão que atribui um código numérico inteiro a cada caractere. A letra `'A'` tem código 65, `'B'` tem 66, e assim por diante até `'Z'` com código 90. No projeto, usamos as funções `ord()` (que retorna o código ASCII de um caractere) e `chr()` (que retorna o caractere dado um código) para percorrer o alfabeto dinamicamente com o laço `chr(ord('A') + i)`. Isso elimina a necessidade de digitar manualmente 26 mapeamentos e torna o código à prova de erros humanos.

**Pergunta 6: Qual a diferença conceitual entre a sua estrutura `FloatVector` e o formato IEEE 754 usado pelo hardware?**
> O IEEE 754 é um formato binário fixo que armazena o número em três campos de bits (sinal, expoente e mantissa) com tamanho predeterminado (32 ou 64 bits). Sua limitação fundamental é a precisão finita: frações que não são exatas em Base 2 sofrem truncamento. O nosso `FloatVector`, em contraste, é uma estrutura de tamanho arbitrário (a lista pode crescer indefinidamente), opera em qualquer base de 2 a 36, e armazena cada dígito de forma simbólica sem perda. Não há truncamento de hardware porque não há limite de bits — o vetor simplesmente cresce conforme necessário.

**Pergunta 7: Por que vocês separaram o `CharMapper` em uma classe própria em vez de incorporar o mapeamento diretamente dentro do `FloatVector`?**
> Aplicamos o Princípio da Responsabilidade Única (SRP). O `FloatVector` tem a responsabilidade de armazenar e estruturar o número; o `CharMapper` tem a responsabilidade de traduzir entre símbolos e valores. Se amanhã precisarmos estender o alfabeto (por exemplo, para suportar bases maiores que 36 usando caracteres Unicode), precisaremos modificar apenas o `CharMapper`, sem tocar na classe de armazenamento. Além disso, o `CharMapper` é reutilizado por outras classes do projeto (como as tabelas aritméticas), evitando duplicação de código.

**Pergunta 8: Vocês falam em "simular um registrador". O que é um registrador de hardware e como o vetor de vocês replica esse conceito?**
> Um registrador é uma pequena unidade de armazenamento ultrarrápida dentro da CPU, composta por flip-flops que guardam bits individuais em série. Ele armazena dados como uma sequência linear contínua — não há separação física entre "parte inteira" e "parte fracionária". Nosso `FloatVector` replica isso: o atributo `digits` é uma lista linear onde todos os dígitos coexistem sequencialmente, e a posição da vírgula é controlada por um metadado separado (`comma_position`), assim como o expoente controla a posição do ponto no hardware. A diferença é que nosso registrador simulado opera com símbolos de qualquer base, não apenas bits.

**Pergunta 9: O que significa o mapeamento ser "bidirecional" e por que isso é necessário?**
> Bidirecional significa que podemos traduzir nos dois sentidos: de caractere para valor (`char_to_val`: `'A'` → `10`) e de valor para caractere (`val_to_char`: `10` → `'A'`). Isso é necessário porque as operações do projeto exigem ambas as direções: quando lemos um número de entrada, precisamos converter seus dígitos-caractere em pesos numéricos para processamento; quando escrevemos o resultado, precisamos converter pesos numéricos de volta em caracteres para exibição. Sem bidirecionalidade, teríamos que implementar uma busca reversa ineficiente percorrendo todo o dicionário.

**Pergunta 10: Qual o limite máximo de base suportado pelo sistema e por quê?**
> O limite é a Base 36, que corresponde aos 10 algarismos arábicos (0-9) mais as 26 letras do alfabeto latino (A-Z), totalizando 36 símbolos distintos. Essa é uma convenção amplamente adotada em computação (utilizada, por exemplo, pela função `int()` do próprio Python e pela ferramenta `base64`). Para suportar bases maiores, seria necessário estender o alfabeto com outros conjuntos de caracteres (como letras minúsculas, caracteres Unicode ou símbolos especiais), o que adicionaria complexidade ao mapeamento sem benefício prático para o escopo acadêmico deste projeto.

---

## Dia 02: Algoritmo de Conversão Direta — Parte Inteira

### 2.1 O Problema da Conversão com Pivô Decimal

A abordagem **convencional** de conversão entre bases utiliza a Base 10 como intermediário:

$$
\text{Base A} \xrightarrow{\text{converter para decimal}} \text{Base 10} \xrightarrow{\text{converter para base B}} \text{Base B}
$$

Essa técnica funciona, mas introduz dois problemas fundamentais:

1. **Injeção de ruído digital**: A Base 10 pode não representar exatamente certas frações que seriam exatas na base de destino. O número $0.1_3$ (um terço na Base 3, que equivale a $1/3$) se torna $0.333\ldots_{10}$ — uma dízima infinita. Ao truncar essa dízima para converter para outra base, introduzimos erros artificiais.

2. **Mascaramento da teoria**: O estudante que usa `int("1A3", 16)` em Python está delegando toda a matemática ao interpretador, que internamente converte para Base 2 via hardware. Nenhuma compreensão da aritmética posicional é exercitada.

A **conversão direta** elimina o pivô:

$$
\text{Base A} \xrightarrow{\text{conversão direta}} \text{Base B}
$$

### 2.2 A Unidade Lógica e Aritmética (ALU) Simulada

#### 2.2.1 ALU em Hardware Real

A **ALU** (_Arithmetic Logic Unit_) é o componente do processador responsável por executar operações aritméticas (soma, subtração, multiplicação, divisão) e lógicas (AND, OR, NOT, XOR). Em um processador convencional, a ALU opera exclusivamente em Base 2 (binário), utilizando circuitos de portas lógicas fisicamente construídos no silício do chip.

#### 2.2.2 ALU Simulada por Tabelas de Consulta

Como o nosso projeto exige operações em **qualquer base arbitrária** (e não apenas em binário), precisamos "construir" nossa própria ALU que saiba somar e multiplicar dígitos na base escolhida. A solução adotada é a **pré-computação de tabelas de consulta** (_lookup tables_).

Para uma dada base $B$, existem exatamente $B^2$ combinações possíveis de pares de dígitos. Para cada par $(a, b)$ onde $0 \le a, b < B$, pré-computamos:

**Tabela de Adição:**

$$
a + b = \text{carry} \cdot B + \text{resultado}
$$

Onde:
- $\text{carry} = \lfloor (a + b) / B \rfloor$ (divisão inteira — o "vai-um")
- $\text{resultado} = (a + b) \mod B$ (resto — o dígito que permanece)

**Tabela de Multiplicação:**

$$
a \times b = \text{carry} \cdot B + \text{resultado}
$$

Onde:
- $\text{carry} = \lfloor (a \times b) / B \rfloor$
- $\text{resultado} = (a \times b) \mod B$

#### 2.2.3 Exemplo Concreto: Tabuada da Base 5

Para a **Base 5**, os dígitos válidos são `{0, 1, 2, 3, 4}`. Algumas entradas da tabela de adição:

| $a$ | $b$ | $a + b$ (decimal) | Carry | Resultado | Notação Base 5 |
|-----|-----|--------------------|-------|-----------|----------------|
| 3   | 4   | 7                  | 1     | 2         | $12_5$          |
| 4   | 4   | 8                  | 1     | 3         | $13_5$          |
| 2   | 1   | 3                  | 0     | 3         | $03_5$          |

Quando nosso algoritmo precisar somar `'3' + '4'` na Base 5, ele simplesmente consulta a tabela e obtém `(carry='1', resultado='2')` — sem executar nenhuma operação aritmética em tempo de execução.

#### 2.2.4 Sobre o Uso de Inteiros na Geração das Tabelas

É importante endereçar uma questão legítima: a geração das tabelas utiliza operações aritméticas nativas do Python (`+`, `*`, `//`, `%`) sobre inteiros pequenos. Isso **não viola** as restrições do projeto pelas seguintes razões:

1. A restrição proíbe usar `int` para representar a **magnitude completa do número**. Os valores envolvidos na geração da tabela são sempre menores que $B^2$ (no máximo $35 \times 35 = 1225$ para Base 36) — são parâmetros de configuração, não dados do problema.
2. Essa geração é **análoga à fabricação do chip**: assim como um engenheiro de hardware usa ferramentas externas para projetar e construir os circuitos da ALU, nós usamos Python para "fabricar" nossa ALU simulada. Uma vez construída, toda a aritmética subsequente do projeto opera exclusivamente por consulta a essas tabelas.
3. A tabela é gerada **uma única vez** no construtor e, a partir desse momento, funciona como um circuito combinacional puro que recebe dois dígitos e emite um resultado, sem operações aritméticas intermediárias.

### 2.3 O Método de Horner para Avaliação Polinomial

#### 2.3.1 Fundamentação Matemática

Qualquer número inteiro em uma base $B_{\text{orig}}$ com $n$ dígitos $d_{n-1}, d_{n-2}, \ldots, d_1, d_0$ pode ser expresso como um polinômio:

$$
N = d_{n-1} \cdot B_{\text{orig}}^{n-1} + d_{n-2} \cdot B_{\text{orig}}^{n-2} + \cdots + d_1 \cdot B_{\text{orig}}^{1} + d_0 \cdot B_{\text{orig}}^{0}
$$

O **Método de Horner** (também chamado de **Esquema de Horner** ou _Horner's Rule_) é uma técnica de fatoração que reescreve este polinômio de forma aninhada, eliminando o cálculo explícito de potências:

$$
N = ((\cdots((d_{n-1} \cdot B_{\text{orig}} + d_{n-2}) \cdot B_{\text{orig}} + d_{n-3}) \cdots) \cdot B_{\text{orig}} + d_1) \cdot B_{\text{orig}} + d_0
$$

#### 2.3.2 Vantagens do Método de Horner

1. **Eficiência computacional**: A forma polinomial direta exige $n-1$ multiplicações para calcular as potências de $B$ e mais $n$ multiplicações para ponderar os dígitos, totalizando $\sim 2n$ multiplicações e $n$ adições. O Método de Horner reduz para exatamente $n-1$ multiplicações e $n-1$ adições.

2. **Eliminação de potências**: Não é necessário calcular ou armazenar $B^2, B^3, \ldots, B^{n-1}$, que crescem exponencialmente e exigiriam vetores intermediários cada vez maiores.

3. **Operação sequencial**: O algoritmo processa um dígito por vez, da esquerda para a direita, acumulando o resultado. Isso é ideal para a nossa arquitetura vetorial.

#### 2.3.3 Exemplo Passo a Passo

Converter $\text{2A3}_{16}$ (Base 16) para Base 10 usando Horner:

1. Início: $\text{resultado} = 0$
2. Dígito `'2'` (peso 2): $\text{resultado} = 0 \times 16 + 2 = 2$
3. Dígito `'A'` (peso 10): $\text{resultado} = 2 \times 16 + 10 = 42$
4. Dígito `'3'` (peso 3): $\text{resultado} = 42 \times 16 + 3 = 675$

Resultado final: $\text{2A3}_{16} = 675_{10}$ ✓

#### 2.3.4 O Truque Central: Executar Horner na Base de Destino

A grande inovação do projeto é que **toda a aritmética do Método de Horner é executada na base de destino**, não na base de origem nem em decimal. 

Quando convertemos $\text{2A3}_{16}$ para Base 10:
- O valor $16$ (a base de origem) é representado como `['1', '6']` no vetor da Base 10.
- O dígito `'A'` (peso 10) é representado como `['1', '0']` no vetor da Base 10.
- As multiplicações e somas são realizadas pela ALU da Base 10 (tabelas de consulta na Base 10).

Em nenhum momento a Base 16 realiza operações — ela apenas fornece os dígitos de entrada.

E se quiséssemos converter $\text{2A3}_{16}$ para Base 7?
- O valor $16$ é representado como `['2', '2']` no vetor da Base 7 (pois $16_{10} = 22_7$).
- O dígito `'A'` (peso 10) é representado como `['1', '3']` no vetor da Base 7 (pois $10_{10} = 13_7$).
- As multiplicações e somas são realizadas pela ALU da Base 7.

**A Base 10 não participa em nenhuma etapa** — a conversão é genuinamente direta.

### 2.4 Aritmética Vetorial "Armada"

Para que o Método de Horner funcione com vetores de caracteres, precisamos de duas operações fundamentais sobre vetores: **adição** e **multiplicação**.

#### 2.4.1 Adição Vetorial com Carry ("Vai-Um")

O algoritmo de adição vetorial replica exatamente o procedimento manual de "armar a conta":

1. **Alinhamento**: Os dois vetores são alinhados pela direita, preenchendo com zeros à esquerda o vetor mais curto.
2. **Varredura**: Percorre-se da direita para a esquerda (da posição menos significativa para a mais significativa).
3. **Soma com carry**: Para cada posição $i$:
   - Soma-se $a_i + b_i$ usando a tabela de adição da ALU, obtendo $(c_1, s_1)$.
   - Soma-se $s_1 + \text{carry\_anterior}$, obtendo $(c_2, s_{\text{final}})$.
   - O novo carry é $c_1 + c_2$ (consultado na tabela).
   - O dígito da posição $i$ do resultado é $s_{\text{final}}$.
4. **Carry final**: Se após a última posição ainda restar carry, ele é inserido à esquerda do resultado.

**Exemplo na Base 5:** Somar $34_5 + 23_5$:

```
  Carry:  1
    3 4
  + 2 3
  -----
  1 1 2    →  Resultado: 112₅
```

- Posição 0 (direita): `4 + 3` → consulta tabela → carry=`1`, dígito=`2`
- Posição 1: `3 + 2` → carry=`1`, dígito=`0`, depois soma carry anterior `1` → dígito=`1`
- Carry final: `1` é inserido à esquerda

#### 2.4.2 Multiplicação Vetorial por Dígito Único

Este é o bloco fundamental da multiplicação. Multiplica-se cada dígito do vetor pelo dígito multiplicador, da direita para a esquerda, propagando carry:

1. Para cada posição $i$ (da direita para a esquerda):
   - Multiplica $v_i \times d$ usando a tabela de multiplicação → $(c_1, p)$.
   - Soma o carry anterior: $p + \text{carry}$ → $(c_2, r)$.
   - Novo carry: $c_1 + c_2$.
   - Dígito do resultado na posição $i$: $r$.
2. Carry final é inserido à esquerda.

#### 2.4.3 Multiplicação Vetorial Completa (Produtos Parciais)

A multiplicação de dois vetores multi-dígito segue o método clássico de **produtos parciais** que aprendemos na escola:

1. Para cada dígito $d_i$ do segundo operando (da direita para a esquerda, com índice $i$):
   - Calcula-se o **produto parcial**: $\text{vec\_a} \times d_i$ (usando `_vector_mul_digit`).
   - Desloca-se o produto parcial $i$ posições para a esquerda (adicionando $i$ zeros à direita), simulando a multiplicação por $B^i$.
2. Todos os produtos parciais são **somados** usando `_vector_add`.

**Exemplo na Base 10:** $23 \times 14$:

```
    2 3
  × 1 4
  -----
    9 2    ← Produto parcial: 23 × 4
  2 3 0    ← Produto parcial: 23 × 1, deslocado 1 posição
  -----
  3 2 2    ← Soma dos produtos parciais
```

### 2.5 A Função `_small_int_to_vector`: Fronteira Controlada

A função `_small_int_to_vector(val)` é a **única fronteira** onde um inteiro Python é convertido para a representação vetorial. Ela é usada exclusivamente para converter:
- O valor da base de origem (ex: `16` se estamos convertendo **da** Base 16).
- O peso de um dígito individual (ex: `10` para o dígito `'A'`).

Esses valores são sempre **pequenos** (no máximo 35 para dígitos, e no máximo 36 para bases), e a conversão ocorre apenas na **inicialização** do processo. Uma vez convertidos para vetores, toda a matemática subsequente opera exclusivamente sobre caracteres, usando as tabelas da ALU.

Esse padrão é análogo à fronteira entre hardware e software: o compilador converte constantes numéricas em representações binárias uma vez, e o circuito então opera autonomamente.

### 2.6 Complexidade Computacional

| Operação | Complexidade |
|----------|-------------|
| Consulta à tabela (lookup) | $O(1)$ |
| Adição de vetores de $n$ dígitos | $O(n)$ |
| Multiplicação por dígito único (vetor de $n$ dígitos) | $O(n)$ |
| Multiplicação de vetores ($n$ dígitos $\times$ $m$ dígitos) | $O(n \cdot m)$ |
| Conversão de Horner ($k$ dígitos de origem, resultado com até $n$ dígitos no destino) | $O(k \cdot n^2)$ no pior caso |

A complexidade da conversão de Horner é cúbica no pior caso porque, a cada iteração, os vetores de resultado crescem, tornando as multiplicações e somas progressivamente mais caras. Isso é aceitável para o escopo acadêmico do projeto.

---

### 2.7 Dez Possíveis Perguntas do Professor — Dia 02

**Pergunta 1: O que é o Método de Horner e por que ele é mais eficiente que a avaliação polinomial direta?**
> O Método de Horner reescreve o polinômio $d_{n-1} B^{n-1} + \cdots + d_0$ na forma aninhada $((d_{n-1} \cdot B + d_{n-2}) \cdot B + \cdots) \cdot B + d_0$. A forma direta exige calcular todas as potências de $B$ separadamente ($B^2, B^3, \ldots$), gerando $\sim 2n$ multiplicações. O Método de Horner elimina completamente o cálculo de potências, reduzindo para apenas $n-1$ multiplicações e $n-1$ adições. Além de ser mais rápido, evita o armazenamento de potências intermediárias que cresceriam exponencialmente como vetores gigantescos.

**Pergunta 2: Como vocês garantem que a conversão é realmente direta e não usa a Base 10 como pivô escondido?**
> Toda a aritmética do Método de Horner é executada usando as tabelas da ALU da **base de destino**. A base de origem é convertida para um vetor na base de destino via `_small_int_to_vector`, e cada dígito de entrada também é convertido para vetor na base de destino. A partir daí, todas as multiplicações e somas acontecem exclusivamente com consultas às tabelas `add_table` e `mul_table` da base de destino. A Base 10 não aparece em nenhuma operação intermediária — ela sequer possui tabelas carregadas no contexto da conversão.

**Pergunta 3: Por que a ALU usa tabelas pré-computadas em vez de calcular as operações em tempo real?**
> Por três razões: (1) **Aderência ao projeto**: calcular em tempo real significaria usar `+` e `*` do Python sobre inteiros nativos durante a conversão, que acionariam a ALU binária do hardware — violando a restrição. (2) **Analogia com hardware real**: processadores reais usam circuitos combinacionais pré-configurados na fabricação que produzem resultados instantâneos para pares de entrada fixos, exatamente como nossas tabelas. (3) **Desempenho**: a consulta a um dicionário hash é $O(1)$, garantindo que cada operação dígito-a-dígito é instantânea.

**Pergunta 4: A geração das tabelas aritméticas usa operações nativas do Python como `+`, `*`, `//` e `%`. Isso não viola a restrição do projeto?**
> Não, porque a restrição proíbe usar `int` e `float` para representar a **magnitude completa do número sendo processado**. Os valores usados na geração das tabelas são parâmetros de fabricação — sempre menores que $B^2$ (no máximo $35 \times 35 = 1225$) e representam pesos de dígitos individuais, não dados do problema. A analogia é a fabricação de um chip: o engenheiro de hardware usa ferramentas externas (CAD, simuladores) para projetar e construir os circuitos da ALU. Uma vez construída, a ALU opera autonomamente. Da mesma forma, uma vez geradas as tabelas, toda a aritmética subsequente ocorre por consulta pura.

**Pergunta 5: Explique passo a passo como funciona a adição vetorial com carry. O que acontece quando a soma de dois dígitos excede a base?**
> A adição vetorial percorre os dois vetores da direita para a esquerda (do menos significativo para o mais significativo), idêntico a "armar a conta" no papel. Para cada par de dígitos, consultamos a tabela de adição, que retorna uma tupla $(carry, resultado)$. Se a soma excede a base (por exemplo, $4 + 3 = 7$ na Base 5), o carry será $\lfloor 7/5 \rfloor = 1$ e o resultado será $7 \mod 5 = 2$. Esse carry é então somado na próxima posição à esquerda. Se após processar todos os dígitos ainda restar carry, ele é inserido como um novo dígito à esquerda do resultado. O algoritmo também trata o caso de dois carries simultâneos (um da soma dos dígitos e outro da soma com o carry anterior).

**Pergunta 6: Como funciona a multiplicação de dois vetores multi-dígito? Descreva o conceito de "produtos parciais".**
> A multiplicação vetorial usa o mesmo método que aprendemos na escola primária. Percorremos o segundo operando da direita para a esquerda. Para cada dígito $d_i$ (na posição $i$), multiplicamos todo o primeiro vetor por esse dígito único usando `_vector_mul_digit`, gerando um **produto parcial**. Esse produto parcial é então deslocado $i$ posições para a esquerda (adicionamos $i$ zeros à direita), o que equivale a multiplicar por $B^i$, respeitando o peso posicional. Finalmente, todos os produtos parciais são somados usando `_vector_add`. O resultado é a multiplicação completa, executada inteiramente com consultas às tabelas da base.

**Pergunta 7: O que é a função `_small_int_to_vector` e por que ela é necessária?**
> É a função que converte pequenos inteiros nativos (como o valor da base de origem ou o peso de um dígito individual) em vetores de caracteres na base de destino. Ela é necessária porque o Método de Horner precisa que a base de origem e cada dígito estejam representados como vetores para poder operar sobre eles com as tabelas da ALU. Esses inteiros são sempre pequenos (no máximo 36), e a conversão ocorre apenas na inicialização do processo. É a **única fronteira controlada** entre o mundo dos inteiros Python e o mundo dos vetores simbólicos. Uma vez que os valores são convertidos, toda a aritmética subsequente é puramente vetorial.

**Pergunta 8: Se eu quiser converter o número $\text{FF}_{16}$ para a Base 3, como o algoritmo procederia? Detalhe as operações.**
> Passo 0: A ALU é carregada com tabelas da Base 3. A base de origem (16) vira o vetor `['1', '2', '1']` na Base 3 (pois $16_{10} = 121_3$). Passo 1: dígito `'F'` (peso 15) vira vetor `['1', '2', '0']` na Base 3 (pois $15_{10} = 120_3$). Horner: resultado $= ['0'] \times ['1','2','1'] + ['1','2','0'] = ['1','2','0']$. Passo 2: dígito `'F'` (peso 15) novamente. Horner: resultado $= ['1','2','0'] \times ['1','2','1'] + ['1','2','0']$. Todas as multiplicações e somas são feitas consultando as tabelas da Base 3. O resultado final será $100110_3$ (equivalente a $255_{10}$). Em nenhum momento a Base 10 ou a Base 16 realizaram operações — apenas a Base 3.

**Pergunta 9: Qual a complexidade computacional da conversão pelo Método de Horner? Ela é aceitável para o projeto?**
> A conversão de Horner para um número com $k$ dígitos na base de origem, produzindo resultados com até $n$ dígitos na base de destino, tem complexidade $O(k \cdot n^2)$ no pior caso. Isso ocorre porque a cada iteração de Horner, realizamos uma multiplicação vetorial ($O(n \cdot m)$ onde $m$ é o tamanho do vetor da base) seguida de uma adição ($O(n)$), e o vetor resultado cresce a cada passo. Para o escopo acadêmico do projeto, que lida com números de tamanho moderado, essa complexidade é perfeitamente aceitável. Otimizações como Karatsuba ou FFT reduziriam a complexidade, mas adicionariam complexidade de implementação desnecessária.

**Pergunta 10: Por que vocês optaram por executar a aritmética de Horner na base de destino e não na base de origem? Qual seria a diferença?**
> Optamos por executar na base de destino porque o resultado final **já nasce na base correta**, dispensando qualquer conversão posterior. Se executássemos na base de origem, teríamos o resultado numérico correto, mas ele estaria representado como um vetor na base de origem — e precisaríamos de uma etapa adicional para converter cada dígito do resultado para a base de destino, o que reintroduziria o problema da conversão intermediária. Executar na base de destino garante que o Método de Horner produz o resultado final diretamente, de forma limpa e sem etapas extras. Além disso, essa estratégia é simétrica à técnica usada em conversores de hardware, onde o circuito destino interpreta os sinais de entrada.
