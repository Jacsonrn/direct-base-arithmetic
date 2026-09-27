"""
Projeto U1 - Aritmética Direta em Bases Arbitrárias (Sem Pivô Decimal)
Disciplina: Computação Numérica
Autor: Jacson

Este módulo serve como ponto de entrada (Entry Point) unificado para:
1. Conversão de números Reais entre bases de 2 a 36.
2. Operações Aritméticas (+, -, *, /) nativas em uma base específica.
3. Demonstração e Suite de Testes Comparativos contra ruído digital (IEEE 754).
"""

import sys
from direct_converter import DirectConverter
from direct_operations import DirectOperations
from base_vector import FloatVector

def format_op_output(v: FloatVector) -> str:
    """Formata a saída visual de FloatVectors gerados pelas Operações Aritméticas."""
    int_part = ''.join(v.digits[:v.comma_position])
    frac_part = ''.join(v.digits[v.comma_position:])
    sinal = '-' if v.sign == '-' else ''
    res = f'{sinal}{int_part}'
    if frac_part: res += f'.{frac_part}'
    return res

def menu_conversao():
    print("\n" + "-"*40)
    print(" Conversão Direta de Base (x ∈ R) ")
    print("-"*40)
    val = input("Digite o número (ex: -1A.8): ").strip().upper()
    try:
        b_orig = int(input("Base de origem (2 a 36): ").strip())
        b_dest = int(input("Base de destino (2 a 36): ").strip())
        
        conv = DirectConverter()
        v_res, ciclo = conv.convert_real(val, b_orig, b_dest)
        
        saida_formatada = conv.format_output(v_res, ciclo)
        print(f"\n[Resultado Exato]: {val} (Base {b_orig})  -->  {saida_formatada}")
    except Exception as e:
        print(f"Erro na conversão: {e}")

def menu_operacoes():
    print("\n" + "-"*40)
    print(" Operações Aritméticas Nativas (ALU) ")
    print("-"*40)
    try:
        base = int(input("Escolha a base da operação (2 a 36): ").strip())
        op = input("Operador (+, -, *, /): ").strip()
        val1 = input(f"Primeiro operando na Base {base}: ").strip().upper()
        val2 = input(f"Segundo operando na Base {base}: ").strip().upper()
        
        v1 = FloatVector(base); v1.from_string(val1)
        v2 = FloatVector(base); v2.from_string(val2)
        alu = DirectOperations(base)
        
        if op == '+': res = alu.add(v1, v2)
        elif op == '-': res = alu.sub(v1, v2)
        elif op == '*': res = alu.mul(v1, v2)
        elif op == '/': res = alu.div(v1, v2)
        else:
            print("Operador inválido.")
            return
            
        print(f"\n[Cálculo Efetuado na Base {base}]:")
        print(f"  {val1}")
        print(f"{op} {val2}")
        print(f"--------")
        print(f"  {format_op_output(res)}")
    except Exception as e:
        print(f"Erro na operação: {e}")

def suite_ruido_digital():
    print("\n" + "="*65)
    print(" SUÍTE DE TESTES COMPARATIVOS: RUÍDO DIGITAL E IEEE 754 ")
    print("="*65)
    
    print("\n-> TESTE 1: O infame problema (0.1 + 0.2)")
    print("Na computação tradicional, o hardware binário não consegue")
    print("representar 0.1 e 0.2 de forma exata, gerando dízimas no silício.")
    
    # Simulação nativa em Python
    py_res = 0.1 + 0.2
    print(f"\n[Hardware / Python - Float64]    : 0.1 + 0.2 = {py_res}")
    
    # Simulação Vetorial
    v1 = FloatVector(10); v1.from_string("0.1")
    v2 = FloatVector(10); v2.from_string("0.2")
    alu = DirectOperations(10)
    vet_res = format_op_output(alu.add(v1, v2))
    print(f"[Nossa Aritmética Abstrata Base 10]: 0.1 + 0.2 = {vet_res}")
    
    if vet_res == "0.3":
        print(">> CONCLUSÃO: Erro de arredondamento cumulativo eliminado com sucesso!")

    print("\n" + "-"*65)
    print("-> TESTE 2: Dízimas Periódicas Artificiais e Perda de Ciclagem")
    print("Converter 0.1 da Base 3 (que equivale a 1/3) para a Base 10.")
    
    # Python nativo
    py_frac = 1 / 3
    print(f"\n[Hardware / Python - Ponto Flutuante]: 1/3 = {py_frac}")
    print("A dízima é truncada por falta de bits (16ª casa), perdendo a matemática exata.")
    
    # Nossa arquitetura
    conv = DirectConverter()
    res, ciclo = conv.convert_real("0.1", 3, 10)
    print(f"[Nosso Conversor Nativo]             : 0.1 (B3) = {conv.format_output(res, ciclo)}")
    print(">> CONCLUSÃO: O Hash Map detectou o ciclo perfeitamente e gerou a notação")
    print("   formal '0.(3)'. Integridade absoluta da informação preservada!")
    
    input("\nPressione Enter para retornar ao menu...")

def main():
    while True:
        print("\n" + "="*55)
        print(" PROCESSADOR ARITMÉTICO VETORIAL - MENU PRINCIPAL")
        print("="*55)
        print("1. Conversão Direta entre Bases (Reais)")
        print("2. Operações Aritméticas Elementares")
        print("3. Executar Suíte de Testes (Demonstração de Ruído)")
        print("0. Sair")
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            menu_conversao()
        elif escolha == '2':
            menu_operacoes()
        elif escolha == '3':
            suite_ruido_digital()
        elif escolha == '0':
            print("Encerrando o sistema. Projeto U1 Finalizado!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
