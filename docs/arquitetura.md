# Arquitetura do Sistema: Processador Aritmético Vetorial

Este diagrama Mermaid ilustra o *pipeline* de dados e a hierarquia de classes do projeto `direct-base-arithmetic`. A arquitetura foi construída sob os princípios **SOLID** (com foco no Princípio da Responsabilidade Única - SRP), garantindo um desacoplamento total entre o controle de fluxo (Facades) e a computação matemática bruta (Baixo Nível).

```mermaid
graph TD
    %% Classes de Estilo (Cores)
    classDef startNode fill:#f59e0b,stroke:#fff,stroke-width:2px,color:#fff;
    classDef facadeNode fill:#0284c7,stroke:#fff,stroke-width:2px,color:#fff;
    classDef lowlevelNode fill:#059669,stroke:#fff,stroke-width:2px,color:#fff;
    classDef hardwareNode fill:#8b5cf6,stroke:#fff,stroke-width:2px,color:#fff;
    classDef dataNode fill:#374151,stroke:#fff,stroke-width:2px,color:#fff;
    classDef decision fill:#6366f1,stroke:#fff,stroke-width:2px,color:#fff;
    classDef endNode fill:#10b981,stroke:#fff,stroke-width:2px,color:#fff;

    Start((Entrada de Dados <br> CLI: main.py)):::startNode --> Parser["Parser de String <br> base_vector.py: from_string()"]:::dataNode
    
    %% Estrutura de Dados
    Parser -->|Valida Dígitos| FV["Registrador Virtual <br> base_vector.py: class FloatVector <br> (sign, digits, comma_position)"]:::dataNode

    FV --> OpType{"Qual a intenção?"}:::decision
    
    %% RAMO ESQUERDO: Conversão de Base (Dias 2 e 3)
    OpType -->|Conversão Numérica| DConv["Orquestrador de Conversão <br> direct_converter.py: convert_real()"]:::facadeNode
    DConv --> Split{"Separar Pela Vírgula"}:::decision
    
    Split -->|Inteiros| IntConv["integer_converter.py <br> convert()"]:::facadeNode
    Split -->|Frações| FracConv["fractional_converter.py <br> convert()"]:::facadeNode
    
    IntConv -->|Método de Horner| VM_Dest["vector_math.py <br> mul(), add() <br> [Instanciado com ALU Destino]"]:::lowlevelNode
    FracConv -->|"Mult. Sucessivas <br> Dicionário Hash"| VM_Orig["vector_math.py <br> mul(), sub() <br> [Instanciado com ALU Origem]"]:::lowlevelNode
    
    VM_Dest --> Merge["Reagrupamento (Merge) <br> direct_converter.py: convert_real()"]:::facadeNode
    VM_Orig -->|"Detecta Ciclos (Ex: 1/3)"| Merge
    
    Merge --> Format["Formatação Final <br> direct_converter.py: format_output()"]:::facadeNode
    Format --> OutConv(("String Renderizada <br> Ex: 0.(3)")):::endNode
    
    %% RAMO DIREITO: Operações Elementares (Dias 4 e 5)
    OpType -->|"Operação (+, -, *, /)"| DOps["Orquestrador Aritmético <br> direct_operations.py: add(), sub()..."]:::facadeNode
    DOps --> Align["Alinhamento Zero-Padding <br> direct_operations.py: _align_vectors()"]:::facadeNode
    Align --> Sign["Roteamento Lógico de Sinais <br> direct_operations.py: add() / sub()"]:::facadeNode
    Sign --> VM_ALU["vector_math.py <br> add(), sub(), mul_digit() <br> [Instanciado com ALU da Base Atual]"]:::lowlevelNode
    
    VM_ALU --> DOps_Fmt["Reajuste da Vírgula <br> direct_operations.py: _format_result()"]:::facadeNode
    DOps_Fmt --> OutOps(("Novo Objeto <br> FloatVector")):::endNode

    %% O CORAÇÃO DE BAIXO NÍVEL (Hardware Simulado)
    VM_Dest ===> ALU
    VM_Orig ===> ALU
    VM_ALU ===>|"add, sub, mul"| ALU["ALU Simulada <br> arithmetic_tables.py <br> lookup_add(), lookup_sub(), lookup_mul()"]:::hardwareNode
    
    ALU -.->|"Bidirecional"| Mapper["Dicionário ASCII (0 a 35) <br> base_vector.py: CharMapper <br> get_value() / get_char()"]:::hardwareNode
```

### Legenda da Arquitetura:
*   **<span style="color:#f59e0b;">Laranja (Entrada):</span>** O Ponto de Entrada da aplicação (`main.py`).
*   **<span style="color:#374151;">Cinza (Data Structures):</span>** Nossas estruturas de armazenamento contínuo e *Parsers* (Ex: `FloatVector`).
*   **<span style="color:#0284c7;">Azul (Facades de Alto Nível):</span>** Classes orquestradoras. Elas lidam com a regra de negócio (Ponto Flutuante, preenchimento de zeros, sinais negativos) e protegem o usuário da matemática bruta.
*   **<span style="color:#6366f1;">Roxo (Decisões):</span>** Desvios de lógica algorítmica.
*   **<span style="color:#059669;">Verde Escuro (Baixo Nível):</span>** A classe `VectorMath` (`vector_math.py`), nosso "Coprocessador Matemático". Opera exclusivamente com matrizes puras, ignorando sinais e vírgulas.
*   **<span style="color:#8b5cf6;">Violeta (Hardware Simulado):</span>** As *Look-up Tables* em `arithmetic_tables.py`. Geram as matrizes $O(1)$ equivalentes aos circuitos combinacionais físicos de uma Unidade Lógica e Aritmética (ALU).
*   **<span style="color:#10b981;">Verde Claro (Saída):</span>** O produto finalizado e validado após o processamento.
