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

### 2.4 Aritmética Vetorial "Armada" e a Refatoração DRY (`VectorMath`)

Para que o Método de Horner funcione com vetores de caracteres, precisamos de duas operações fundamentais sobre vetores: **adição** e **multiplicação**. Estas operações foram isoladas na classe `VectorMath` (implementando o princípio DRY - *Don't Repeat Yourself*), o que permite que elas sejam utilizadas tanto pela conversão da parte inteira (Dia 2) quanto fracionária (Dia 3).

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

#### 2.4.2 Multiplicação Vetorial Completa (Produtos Parciais)

A multiplicação de dois vetores multi-dígito segue o método clássico de **produtos parciais** que aprendemos na escola:

1. Para cada dígito $d_i$ do segundo operando (da direita para a esquerda, com índice $i$):
   - Calcula-se o **produto parcial**: $\text{vec\_a} \times d_i$ (usando `_vector_mul_digit`).
   - Desloca-se o produto parcial $i$ posições para a esquerda (adicionando $i$ zeros à direita), simulando a multiplicação por $B^i$.
2. Todos os produtos parciais são **somados** usando a função de adição vetorial.

### 2.5 A Função `_small_int_to_vector`: Fronteira Controlada

A função `_small_int_to_vector(val)` é a **única fronteira** onde um inteiro Python é convertido para a representação vetorial. Ela é usada exclusivamente para converter:
- O valor da base de origem ou destino (ex: `16` se estamos convertendo **da/para** Base 16).
- O peso de um dígito individual (ex: `10` para o dígito `'A'`).

Esses valores são sempre **pequenos** (no máximo 35 para dígitos, e no máximo 36 para bases), e a conversão ocorre apenas na **inicialização** do processo. Uma vez convertidos para vetores, toda a matemática subsequente opera exclusivamente sobre caracteres, usando as tabelas da ALU.

Esse padrão é análogo à fronteira entre hardware e software: o compilador converte constantes numéricas em representações binárias uma vez, e o circuito então opera autonomamente.

---

### 2.6 Dez Possíveis Perguntas do Professor — Dia 02

**Pergunta 1: O que é o Método de Horner e por que ele é mais eficiente que a avaliação polinomial direta?**
> O Método de Horner reescreve o polinômio $d_{n-1} B^{n-1} + \cdots + d_0$ na forma aninhada $((d_{n-1} \cdot B + d_{n-2}) \cdot B + \cdots) \cdot B + d_0$. A forma direta exige calcular todas as potências de $B$ separadamente ($B^2, B^3, \ldots$), gerando $\sim 2n$ multiplicações. O Método de Horner elimina completamente o cálculo de potências, reduzindo para apenas $n-1$ multiplicações e $n-1$ adições. Além de ser mais rápido, evita o armazenamento de potências intermediárias que cresceriam exponencialmente como vetores gigantescos.

**Pergunta 2: Como vocês garantem que a conversão é realmente direta e não usa a Base 10 como pivô escondido?**
> Toda a aritmética do Método de Horner é executada usando as tabelas da ALU da **base de destino**. A base de origem é convertida para um vetor na base de destino via `_small_int_to_vector`, e cada dígito de entrada também é convertido para vetor na base de destino. A partir daí, todas as multiplicações e somas acontecem exclusivamente com consultas às tabelas `add_table` e `mul_table` da base de destino. A Base 10 não aparece em nenhuma operação intermediária — ela sequer possui tabelas carregadas no contexto da conversão (exceto, é claro, se ela própria for a base de destino).

**Pergunta 3: Por que a ALU usa tabelas pré-computadas em vez de calcular as operações em tempo real?**
> Por três razões: (1) **Aderência ao projeto**: calcular em tempo real significaria usar `+` e `*` do Python sobre inteiros nativos durante a conversão, que acionariam a ALU binária do hardware — violando a restrição de "simulação puramente abstrata". (2) **Analogia com hardware real**: processadores reais usam circuitos combinacionais pré-configurados na fabricação que produzem resultados instantâneos para pares de entrada fixos, exatamente como nossas tabelas. (3) **Desempenho**: a consulta a um dicionário hash é $O(1)$, garantindo que cada operação dígito-a-dígito seja instantânea.

**Pergunta 4: A geração das tabelas aritméticas usa operações nativas do Python como `+`, `*`, `//` e `%`. Isso não viola a restrição do projeto?**
> Não, porque a restrição proíbe usar `int` e `float` para representar a **magnitude completa do número sendo processado**. Os valores usados na geração das tabelas são parâmetros de fabricação — sempre menores que $B^2$ (no máximo $35 \times 35 = 1225$) e representam pesos de dígitos individuais, não dados do problema. A analogia é a fabricação de um chip: o engenheiro de hardware usa ferramentas externas (CAD, simuladores) para projetar os circuitos. Uma vez construída, a ALU opera autonomamente por buscas no dicionário hash.

**Pergunta 5: Explique passo a passo como funciona a adição vetorial com carry. O que acontece quando a soma de dois dígitos excede a base?**
> A adição vetorial (na classe `VectorMath`) percorre os dois vetores da direita para a esquerda (do menos significativo para o mais significativo), de modo idêntico a "armar a conta" no papel. Para cada par de dígitos, consultamos a tabela de adição, que retorna uma tupla $(carry, resultado)$. Se a soma excede a base (por exemplo, $4 + 3 = 7$ na Base 5), o carry será $\lfloor 7/5 \rfloor = 1$ e o resultado será $7 \mod 5 = 2$. Esse carry é então somado na próxima posição à esquerda. Se após processar todos os dígitos ainda restar carry, ele é inserido como um novo dígito à esquerda do resultado.

**Pergunta 6: Como funciona a multiplicação de dois vetores multi-dígito? Descreva o conceito de "produtos parciais".**
> A multiplicação vetorial (na classe `VectorMath`) usa o mesmo método que aprendemos na escola primária. Percorremos o segundo operando da direita para a esquerda. Para cada dígito $d_i$ (na posição $i$), multiplicamos todo o primeiro vetor por esse dígito único, gerando um **produto parcial**. Esse produto parcial é então deslocado $i$ posições para a esquerda (adicionamos $i$ zeros à direita), o que equivale a multiplicar por $B^i$, respeitando o peso posicional. Finalmente, todos os produtos parciais são somados. O resultado é a multiplicação completa, executada inteiramente com consultas às tabelas da base.

**Pergunta 7: O que é a função `_small_int_to_vector` e por que ela é necessária?**
> É a função que converte pequenos inteiros nativos (como o valor da base de origem ou o peso de um dígito individual) em vetores de caracteres na base alvo. Ela é necessária porque as operações (Horner ou Multiplicações Sucessivas) precisam que a base e cada dígito estejam representados como vetores para poder operar sobre eles com as tabelas da ALU. Esses inteiros são sempre pequenos (no máximo 36), e a conversão ocorre apenas na inicialização do processo (como configuração). É a **única fronteira controlada** entre o mundo dos inteiros Python e o mundo dos vetores simbólicos.

**Pergunta 8: Se eu quiser converter o número $\text{FF}_{16}$ para a Base 3, como o algoritmo procederia? Detalhe as operações.**
> Passo 0: O `IntegerConverter` instancia a ALU carregada com tabelas da Base 3 (destino). A base de origem (16) vira o vetor `['1', '2', '1']` na Base 3 (pois $16_{10} = 121_3$). Passo 1: O primeiro dígito `'F'` (peso 15) vira vetor `['1', '2', '0']` na Base 3 (pois $15_{10} = 120_3$). Horner: resultado $= ['0'] \times ['1','2','1'] + ['1','2','0'] = ['1','2','0']$. Passo 2: O segundo dígito `'F'` (peso 15) novamente. Horner: resultado $= ['1','2','0'] \times ['1','2','1'] + ['1','2','0']$. Todas as multiplicações e somas são feitas pelo `VectorMath` consultando as tabelas da Base 3. O resultado final será $100110_3$ (equivalente a $255_{10}$). A Base 16 só serviu para dar a string inicial; a Base 10 não serviu para nada.

**Pergunta 9: Qual a complexidade computacional da conversão pelo Método de Horner? Ela é aceitável para o projeto?**
> A conversão de Horner para um número com $k$ dígitos na base de origem, produzindo resultados com até $n$ dígitos na base de destino, tem complexidade $O(k \cdot n^2)$ no pior caso. Isso ocorre porque a cada iteração de Horner, realizamos uma multiplicação vetorial ($O(n \cdot m)$ onde $m$ é o tamanho do vetor da base) seguida de uma adição ($O(n)$), e o vetor resultado cresce a cada passo. Para o escopo acadêmico do projeto, que lida com números de tamanho moderado, essa complexidade é perfeitamente aceitável. O foco está na integridade aritmética e eliminação de pivôs.

**Pergunta 10: Por que vocês optaram por executar a aritmética de Horner na base de destino e não na base de origem?**
> Optamos por executar na base de destino porque, dessa forma, o vetor resultante do método de Horner **já nasce na base correta**, dispensando qualquer pós-processamento. Se executássemos na base de origem, obteríamos a magnitude do número correta, porém ela estaria codificada num vetor longo da base de origem (e nós precisaríamos de uma etapa adicional para dividir sucessivamente esse vetor na base destino, o que seria redundante). Além disso, essa estratégia se alinha à simetria espelhada da nossa arquitetura: Horner é executado na Destino (para Inteiros) e Multiplicações Sucessivas são executadas na Origem (para Frações).

---

## Dia 03: Conversão Direta — Parte Fracionária e Integração a $\mathbb{R}$

### 3.1 A Simetria Invertida: Multiplicações Sucessivas na Base de Origem

Para converter a parte **fracionária** entre duas bases arbitrárias de forma puramente abstrata, não podemos utilizar o Método de Horner convencional. A matemática de pesos negativos exige o método das **Multiplicações Sucessivas**.

No Dia 2, para a parte inteira, a ALU era configurada na **Base de Destino**, processando a matemática de "baixo para cima". 
No Dia 3, ocorre uma simetria espelhada brilhante da teoria dos números: para a parte fracionária, a ALU precisa ser instanciada estritamente na **Base de Origem**.

**Por que na Base de Origem?**
Seja a fração $0.3_{10}$ (Base 10) que deve ser convertida para Base 2.
1. Multiplicamos a fração pela base de destino ($2_{10}$): $0.3_{10} \times 2_{10} = 0.6_{10}$.
2. A operação matemática ($3 \times 2 = 6$) ocorreu obedecendo às tabuadas da Base 10.
3. O "transbordo" (a parte que passa para a esquerda da vírgula) é retirado e torna-se o próximo dígito na Base 2. No caso, $0$.
4. O processo se repete com o resto ($0.6_{10}$).

Ao longo deste ciclo, todo o trabalho algébrico é realizado com **vetores da base de origem** utilizando exatamente a mesma classe de apoio `VectorMath` implementada para a parte inteira (Princípio DRY).

### 3.2 O Processamento Integrado de Inteiros e Frações (Reais)

Para atender à restrição máxima do Dia 3 — *"O conversor deve processar perfeitamente a parte inteira e fracionária de forma integrada"* —, foi criado o módulo `DirectConverter`.

A separação entre Horner (para inteiros) e Multiplicações (para frações) não é uma limitação de engenharia de software, mas sim uma exigência da álgebra vetorial abstrata. Se tentássemos computar pesos fracionários negativos em um mesmo loop com Horner, seríamos forçados a fazer sucessivas divisões vetoriais por potências, causando possíveis perdas de precisão antes mesmo da resposta final estar formatada.

A classe `DirectConverter` age como uma **orquestradora**:
1. Recebe o número real bruto (ex: `"-1A3.F"`).
2. Transforma-o em um `FloatVector` e localiza o ponteiro da vírgula.
3. Repassa os vetores de dígitos à esquerda da vírgula para o `IntegerConverter`.
4. Repassa os vetores de dígitos à direita da vírgula para o `FractionalConverter`.
5. **Reagrega** tudo em um único e novo `FloatVector` pertencente à base de destino e formata a resposta.

Essa abordagem preserva o encapsulamento, fornece uma API única para uso externo e obedece matematicamente a todos os requisitos.

### 3.3 Dízimas Periódicas Nativas (O Problema do IEEE 754)

No sistema computacional padrão, variáveis `float` armazenam dados sob a norma IEEE 754. Quando um número não tem representação finita numa base, ele se torna uma **dízima**. 
Exemplo clássico: $0.1_{10}$ (1/10 finito na Base 10) é infinito na Base 2: $0.0001100110011..._{2}$

O hardware lida com isso cortando o número (truncamento). Quando se faz a conversão reversa, o pedaço amputado faz falta, e um erro de arredondamento aparece (o infame *`0.1 + 0.2 = 0.30000000000000004`* do JavaScript/Python).

No projeto U1, o `FractionalConverter` não trabalha com precisão limitada. Ele trabalha com vetores de caracteres exatos da fração. Para evitar um loop infinito em dízimas reais (e diferenciar truncamento de repetição autêntica), adotou-se o rastreamento via **Dicionário de Estados (Hash Map Histórico)**.

**Como funciona a detecção de Dízimas:**
1. Antes de cada multiplicação sucessiva, a fração atual (ex: `['1', '5']`) tem seus zeros à direita "limpos" (normalização).
2. Essa fração é convertida em string e adicionada a um dicionário `history`, associada à posição onde estamos (`len(result_digits)`).
3. Se o algoritmo, no futuro, chegar numa fração exata de resto `['0']`, a conversão para; ela é finita.
4. Se o algoritmo chegar numa fração que **já consta nas chaves do `history`**, ele detectou um *Déjà Vu*. Ele interrompe o laço instantaneamente, retorna os dígitos computados e informa ao orquestrador o índice exato onde a dízima se inicia (ciclo).
5. O `DirectConverter` imprime visualmente a notação de dízima: `0.0(0011)`. 

---

### 3.4 Dez Possíveis Perguntas do Professor — Dia 03

**Pergunta 1: Como o conversor trata o fato da conversão fracionária precisar da base de origem para funcionar, em oposição à parte inteira que rodou na de destino?**
> A arquitetura vetorial lidou com isso instanciando uma segunda ALU (Unidade Lógica e Aritmética). No `FractionalConverter`, nós declaramos `self.tables = ArithmeticTables(source_base, mapper)`. Com a ALU focada na Origem, a classe `VectorMath` realiza a soma e a multiplicação sem que o algoritmo principal tenha de se preocupar. É o mesmo motor operatório da parte inteira, mas operando com o dicionário Hash da base de origem (Simetria Invertida). 

**Pergunta 2: A restrição fala sobre não usar coerção decimal fracionária (multiplicar e dividir por 10). Como vocês se livraram disso?**
> Um "atalho" infeliz em conversores fracionários seria assumir a fração $0.35$ como o inteiro $35$, submetê-la ao conversor inteiro do Dia 2, e depois dividir no destino por $100$. Isso exige coerção decimal base 10 implícita. Nosso `FractionalConverter` isola os caracteres (ex: `['3', '5']`) num sub-vetor. Usamos o `VectorMath` para efetivamente fazer `['3', '5'] * DestBaseVector` usando a ALU original. Dessa forma, as variáveis nunca formam uma magnitude numérica inteira artificial, eliminando coerção nativa de potências da Base 10.

**Pergunta 3: Qual é o risco de não se isolar inteiros e fracionários e tentar rodar tudo de uma vez com Horner em Bases diferentes de 10?**
> A aritmética posicional, fundamentalmente, exige comportamentos opostos para Expoentes Positivos (divergentes) e Expoentes Negativos (convergentes). Horner exige o armazenamento de divisões para a direita. Ao rodar divisões em vetores abstratos em bases genéricas, cairíamos num vórtice infinito logo no primeiro algarismo não múltiplo da base. Separando-os pela posição da vírgula, efetuamos Multiplicação no fracionário. Orquestrando tudo no final com a classe `DirectConverter`, temos estabilidade de 100% e evitamos divisão.

**Pergunta 4: O que significa o rastreamento via "Dicionário de Estados"? Como o projeto detecta uma dízima periódica?**
> Quando estamos multiplicando o resto da fração, nós sempre guardamos a "assinatura" do resto num Hash Map do Python, apontando para em qual índice do loop ele apareceu. Se o resto $X$ der as caras de novo, a matemática provará que os próximos passos serão exatamente os mesmos. O algoritmo aciona o "break", pega o índice apontado no Dicionário, e nós "envelopamos" com parênteses os dígitos a partir do índice salvo. Exemplo: um $0.3333..._{10}$ originário de um $0.1_3$ é detectado assim que a sobra "1" aparece pela segunda vez. Retorna-se `0.(3)`.

**Pergunta 5: A detecção de dízima tem um alto custo de memória já que salva cada resto histórico?**
> Não. O objeto `history` armazena apenas um dicionário de strings curtas, de acordo com as casas fracionárias, em complexidade de tempo de busca $O(1)$. Além disso, inserimos um `max_precision=20` preventivo; caso o usuário faça um cálculo irracional infinito (ou uma dízima muito exótica), após 20 iterações o algoritmo aceitará a aproximação e encerrará o loop. Isso mantém a pegada de memória ($O(K)$) no Dicionário negligenciável perante a infraestrutura.

**Pergunta 6: Na saída visual final, o que o `DirectConverter` faz ao receber `0` na parte inteira e um loop do `FractionalConverter`?**
> A parte inteira devolverá ao vetor apenas a string `['0']`. O fracionário devolverá uma lista contendo, por exemplo, o vetor `['0', '0', '1', '1']` e o índice $1$ marcando o ciclo. O `DirectConverter.format_output` injetará o caractere de vírgula/ponto da notação exata no índice indicado, e isolará a string entre os parênteses referentes ao ciclo: `0.0(011)`. A formatação visual trata a notação universal, não mascarando o hardware.

**Pergunta 7: O algoritmo de Multiplicações Sucessivas extrai "o que transbordou" para a parte inteira (o overflow). Como o script converte esse overflow da origem para a base de destino final?**
> Quando o vetor fracionário é multiplicado pela Base Destino (usando o sistema operando na Base Origem), a multiplicação aumenta a string; por exemplo, `['3', '5']` de duas posições pode virar `['1', '3', '0']` com três. Isolamos os $N$ números excedentes à esquerda (`['1']`), convertemos esse sub-vetor minúsculo via função controlada (porque sabemos que o overflow é, no máximo, restrito ao limite de `36` — não uma magnitude global) e buscamos a chave correta dele na classe `CharMapper`. O símbolo vira a próxima casa do vetor fracionário final.

**Pergunta 8: Por que a refatoração extraindo as matemáticas num módulo `VectorMath` foi necessária hoje, no Dia 3?**
> Devido ao princípio DRY de Engenharia de Software (Don't Repeat Yourself). Os métodos `_vector_add` e `_vector_mul` criados no Dia 2 possuíam uma complexidade considerável de varredura (da direita para esquerda carregando carry de soma com a ALU). Como percebemos que o `FractionalConverter` utilizaria exatamente a mesma estrutura (só que acionando a ALU da Base de Origem ao invés da Destino), seria péssima prática copiar e colar o código de vetor. O encapsulamento limpo permitiu que instanciássemos o `VectorMath(ALU_Orig)` ou `VectorMath(ALU_Dest)` conforme o desejo algébrico.

**Pergunta 9: Ao "normalizar" o estado removendo zeros à direita (função `_normalize_frac_state`), qual perigo estávamos evadindo no histórico?**
> Se no passo 1 a sobra foi a representação `['5', '0']`, ela tem o mesmo valor matemático absoluto fracionário que `['5']`. Se não expurgássemos o zero fantasma à direita, o Dicionário de História Python trataria `"50"` e `"5"` como duas chaves (Hashes) completamente diferentes. Isso arruinaria o laço da dízima periódica, transformando um ciclo simples num falso loop finito ou numa interrupção baseada em `max_precision`. A normalização garante que frações aritmeticamente idênticas emitam sempre a mesma assinatura no dicionário.

**Pergunta 10: Ao dizer que as partes se unem de "Forma Integrada", a que vocês se referem no contexto de Produto Final?**
> O usuário (ou outro módulo Python, ou uma CLI no Dia 6) jamais precisa tocar no construtor de Horner ou no loop de Histórico e de Multiplicações Sucessivas. Para o sistema, o comando `DirectConverter().convert_real("1.33", 10, 2)` é o único ponto de contato existente (Padrão Façade). A lógica de desmembramento entre inteiros e frações, separação das ALUs (Origem/Destino) e formatação de Parênteses Finais fica estritamente na caixa-preta. Do ponto de vista de requisito funcional, o programa lida perfeitamente com um conjunto de vetores $x \in \mathbb{R}$ em chamada unificada.

---

## Dia 04: Operações Elementares Diretas — Adição e Subtração

### 4.1 A Extensão da ALU: O Controle de Borrow (Empréstimo)

Até o Dia 3, a nossa Unidade Lógica e Aritmética Simulada (ALU) no arquivo `arithmetic_tables.py` calculava prévia e estaticamente o carry de Adição e de Multiplicação. No Dia 4, adicionamos as tabelas de consulta ($O(1)$) para **Subtração**, com o crucial controle de **Borrow** (o "pede-emprestado").

A lógica matemática de pré-computação da tabela de subtração é:
- Para cada par de dígitos válidos $(a, b)$ na Base $B$:
  - Se $a \ge b$, o resultado é $a - b$ e o **borrow** gerado para a casa anterior é $0$.
  - Se $a < b$, nós não geramos um dígito negativo (o que seria uma violação no registrador abstrato). Nós pegamos $B$ emprestado da próxima casa à esquerda. Logo, o resultado é $(a + B) - b$ e o **borrow** gerado para a casa anterior é $1$.

### 4.2 Alinhamento em Ponto Flutuante

Para que os operandos vetoriais (`FloatVector`) operem sem colapso, implementamos no módulo `DirectOperations` o método `align_vectors`. 
A regra básica de operações elementares, aplicável a todas as bases de 2 a 36, é **Vírgula embaixo de vírgula**.
- Os zeros à **esquerda da parte inteira** (zero-padding) não alteram o valor numérico.
- Os zeros à **direita da parte fracionária** (zero-padding) não alteram o valor numérico.
Assim, $12.5 + 1.25$ se converte no vetor alinhado $12.50 + 01.25$. A posição da vírgula `comma_position` em ambos os operandos passa a ser idêntica, permitindo que o algoritmo itere dígito a dígito de forma estritamente mecânica e linear, varrendo do último caractere fracionário até o primeiro caractere inteiro.

### 4.3 A Adição e Subtração Universais sem Intervenção Decimal

As operações (denominadas `_unsigned_add` e `_unsigned_sub`) não convertem os blocos de algarismos em valores decimais. Se o sistema está processando Hexadecimal e encontra a coluna `A` e `1`, ele envia o par de caracteres `('A', '1')` à tabela hash, que imediatamente retorna o caractere `'B'`. Não existe matemática de tempo de execução, preservando assim a pureza da **Aritmética Direta na Base**, como exigido pelo edital do projeto.

No caso da **Subtração Vetorial**, o algoritmo exige que a parcela de cima seja, no mínimo, do mesmo tamanho da de baixo ($A \ge B$). 
Para cada casa de índice $i$:
1. Subtraímos o dígito de baixo pelo de cima, guardando o empréstimo originário $b_1$.
2. Imediatamente subtraímos a casa resultante pelo **borrow que havia sido transportado** da iteração passada, guardando um potencial empréstimo residual $b_2$.
3. O novo borrow que será mandado para a esquerda é a soma de $b_1 + b_2$. (Nossa teoria assegurou matematicamente que $b_1$ e $b_2$ nunca podem ser igual a 1 simultaneamente).

### 4.4 Roteamento de Sinais: Replicando Regras Aritméticas

No mundo real (e computacional), a adição entre dois números negativos é na verdade uma subtração de suas magnitudes, com conservação de sinais.
O orquestrador público exposto pelo módulo `DirectOperations`:
1. Identifica se a chamada à API é de `add()` (Soma) ou `sub()` (Subtração).
2. Converte todas as subtrações em adições de sinais invertidos: $A - B \rightarrow A + (-B)$.
3. Efetua a checagem absoluta (módulo) usando o método `is_greater_or_equal_abs`.
4. Roteia a execução:
   - Se os sinais forem iguais: aciona a soma simples (`_unsigned_add`) e mantém o sinal comum.
   - Se os sinais diferem: aciona a subtração armada (`_unsigned_sub`), colocando no topo a maior magnitude, e herdando o sinal do vetor absoluto superior.

Esse controle de fluxo é a **chave** que permite processar Reais negativos perfeitamente.

---

### 4.5 Dez Possíveis Perguntas do Professor — Dia 04

**Pergunta 1: Como o seu algoritmo lida com a soma de $10.1_2$ e $1.1_2$ se eles têm tamanhos diferentes?**
> Através do algoritmo de alinhamento em ponto flutuante na classe `DirectOperations`. Como a nossa estrutura `FloatVector` isola conceitualmente a parte inteira da fracionária pela `comma_position`, nós injetamos zeros à esquerda da parte inteira do número menor e zeros à direita da parte fracionária, se necessário. O alinhamento formaria $10.1$ e $01.1$.

**Pergunta 2: Se eu inserir os caracteres Hexadecimais `'A'` e `'B'` na subtração sem envolver as bibliotecas `int` do Python, como o computador saberá que `'B'` (11) menos `'A'` (10) resulta em 1?**
> Pela arquitetura de **Look-Up Table** (Tabela de Consulta Hash) desenvolvida no Dia 2 e expandida no Dia 4. No momento da instância do código para Hexadecimal, geramos uma matriz estática que aponta a chave hash `('B', 'A')` diretamente à tupla de retorno `(borrow='0', resultado='1')`. Nós nunca fazemos o CPU calcular $11 - 10$ no meio da soma; nós acessamos a memória em $O(1)$.

**Pergunta 3: O que vocês fazem se o usuário pede para calcular $3 - 8$ (ou seja, quando $A < B$)? A subtração vetorial de vocês permite gerar dígitos negativos?**
> Não. O registrador abstrato foi programado para jamais emitir um caractere `-` isolado no meio do vetor. O método `_unsigned_sub` obriga que a magnitude de $A \ge B$. O orquestrador superior lida com a solicitação calculando $|8| - |3|$, que gera a saída `5`, e depois anexa cirurgicamente o sinal de quem tinha a maior magnitude absoluta, resultando em `-5`.

**Pergunta 4: O algoritmo permite base decimal (10) como ponte para o carry ou o borrow na subtração armada?**
> Absolutamente não. Essa é a restrição mais importante do Dia 4. O nosso borrow funciona inteiramente a partir das tabelas nativas de cada base. Se estivermos na Base 2, um empréstimo (borrow) vale exatamente $2$. Nós nunca transformamos as strings do vetor para `int` em Python para fazer uma matemática decimal oculta.

**Pergunta 5: Mostre-me onde está o risco matemático caso um borrow tente pedir empréstimo no mesmo momento em que a subtração inicial também precisa de um.**
> Isso é matematicamente impossível. Se subtrairmos a coluna de cima pela coluna de baixo ($b_1$) e isso gerar borrow, é porque $A < B$. Isso significa que o resultado temporário já incorporou o bônus da base e se tornou largo o suficiente de forma que subtrair um único $-1$ adicional de borrow na cascata ($b_2$) não necessitará pedir outro à esquerda. Logo, $b_1$ e $b_2$ nunca podem estourar somados.

**Pergunta 6: Na subtração armada, qual é o critério de parada da propagação de zeros? (Ex: o falso $04.5 - 04.5 = 00.0$)**
> A função `_unsigned_sub` e a função de roteamento geral executam a sanitização através de blocos `while`. Na parte inteira, todos os zeros excedentes à esquerda são descartados através de cortes (pops) na lista, até atingirmos um limite que pare perto da vírgula (evitando apagar o `.0` no final absoluto). A regra `is_greater_or_equal_abs` é quem nos previne que um vetor acabe com $000$ fantasmas poluindo a visualização limpa de string.

**Pergunta 7: Em um empréstimo (borrow) muito estendido (ex: $1000_{16} - 1_{16}$), como a sua string reage à travessia por múltiplos zeros?**
> De maneira mecânica e natural. A cada zero processado, $0_{16} - 0_{16} - \text{borrow\_anterior} (1)$ dispara a tabela que sabe que $0 - 1 = \text{resultado } F$, e exige borrow de 1 para o colega seguinte à esquerda. O algoritmo é um loop rígido que não "enxerga" o final: ele só para quando a varredura atinge o índice $0$ da string alinhada, o que consome perfeitamente o $1 - 1 = 0$ na extrema esquerda.

**Pergunta 8: No momento em que você injeta os zeros de alinhamento (`zero-padding`), você não perde o verdadeiro `comma_position` das Strings originais?**
> Nós preservamos perfeitamente e garantimos que a saída também ganhe a formatação original. Como nós anexamos $N$ zeros para preencher a lacuna máxima (`max_int - len(int_a)`), a nova posição de vírgula passa a ser exatamente o tamanho desse novo bloco inteiro máximo. Ambos os FloatVectors virtuais (A e B) terão uma `comma_position` unânime para o loop iterar de forma sincronizada.

**Pergunta 9: O que acontece caso as matrizes de adição e de subtração lidem com dois `FloatVectors` em bases divergentes (Ex: somar um número Binário com um Octal)?**
> O módulo possui validação rígida de fronteira na primeira linha da operação `add(A, B)`. Se a propriedade `base` do operando $A$ for incompatível com a do operando $B$, nós levantamos um `ValueError`. Operações vetoriais armadas diretas são axiomáticas da mesma base. Para somá-los, o usuário deve primeiro engatilhar a API do `DirectConverter` (Dia 2 e 3) para equiparar as bases.

**Pergunta 10: Ao dizer que resolvemos $A - B$ invertendo o sinal de $B$ e chamando a Adição, que Padrão de Engenharia de Software foi respeitado?**
> Reuso de Código de Alto Nível (DRY) e Abstração Algébrica. Na matemática, a subtração genuína não passa de uma adição perante um inverso aditivo. Nossa API não precisa se desdobrar criando duas lógicas para controle de sinais (uma de soma, uma de subtração). Encapsulando tudo perante uma porta de entrada global, se o dev pedir "Diminua 5 de 10", nós clonamos a variável do 5, transformamos em -5, e entregamos para o módulo de soma lidar com $10 + (-5)$. O roteador cuida do resto de forma muito elegante.
