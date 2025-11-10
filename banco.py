import textwrap

# Função auxiliar para exibir o menu de opções
def menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu_text = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    => """
    # textwrap.dedent é usado para formatar o texto do menu de forma limpa, 
    # removendo a indentação inicial.
    return input(textwrap.dedent(menu_text))


## 1. Funções de Operações Bancárias (V1 - Refatoradas)

# Regra: Argumentos apenas por POSIÇÃO (indicado por '/')
def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta. 
    Argumentos: apenas por posição (saldo, valor, extrato).
    Retorna: saldo e extrato atualizados.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


# Regra: Argumentos apenas por NOME (keyword only, indicado por '*')
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque na conta. 
    Argumentos: apenas por nome (keyword only).
    Retorna: saldo, extrato e numero_saques atualizados.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


# Regra: Argumento 'saldo' por POSIÇÃO e 'extrato' por NOME
def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato bancário. 
    Argumentos: saldo por posição, extrato por nome.
    """
    print("\n================ EXTRATO ================")
    # textwrap.dedent garante que a formatação da string seja limpa
    print(textwrap.dedent("Não foram realizadas movimentações." if not extrato else extrato))
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


## 2. Funções de Usuário e Conta (V2)

def filtrar_usuario(cpf, usuarios):
    """
    Busca um usuário na lista pelo CPF (apenas números).
    Retorna o dicionário do usuário se encontrado, ou None.
    """
    # Limpa o CPF de entrada, garantindo que contenha apenas dígitos
    cpf_limpo = ''.join(filter(str.isdigit, cpf)) 
    
    # Filtra a lista de usuários comparando o CPF limpo
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf_limpo]
    
    # Retorna o primeiro usuário encontrado ou None
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):
    """
    Cria um novo usuário (cliente).
    Regras: CPF deve ser único e armazenar apenas números.
    """
    cpf_input = input("Informe o CPF (somente números): ")
    cpf_limpo = ''.join(filter(str.isdigit, cpf_input)) 

    # Validação simples de tamanho do CPF
    if len(cpf_limpo) != 11:
        print("\n@@@ CPF inválido. Certifique-se de digitar 11 dígitos. @@@")
        return

    # Verifica se o usuário já existe (regra de CPF único)
    usuario = filtrar_usuario(cpf_limpo, usuarios)
    if usuario:
        print("\n@@@ Operação falhou! Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    # Formato do endereço requerido
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adiciona o novo usuário como um dicionário na lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf_limpo, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios, contas):
    """
    Cria uma nova conta corrente e vincula a um usuário existente (pelo CPF).
    Regras: Agência fixa "0001". Número da conta sequencial.
    """
    cpf = input("Informe o CPF do usuário para vincular a conta (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios) # Busca o usuário para vincular

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        # Adiciona a nova conta. O valor 'usuario' armazena a referência ao dicionário do usuário.
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        
        # Incrementa e retorna o próximo número de conta sequencial
        return numero_conta + 1 
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    # Retorna o número de conta inalterado se a criação falhar
    return numero_conta 


def listar_contas(contas):
    """
    Lista todas as contas criadas com seus respectivos usuários.
    Esta função só lista contas se a lista 'contas' tiver sido preenchida
    pela função 'criar_conta' (opção 'nc').
    """
    if not contas:
        print("\n@@@ Não há contas cadastradas para listar. Use a opção [nc] para criar uma. @@@")
        return

    print("\n================ CONTAS CADASTRADAS ================")
    for conta in contas:
        # Imprime os detalhes da conta e do usuário vinculado
        print(textwrap.dedent(f"""\
            Agência:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            CPF:\t\t{conta['usuario']['cpf']}
        """))
        print("-" * 40)
    print("====================================================\n")


## 3. Função Principal (main)

def main():
    """Função principal que gerencia o estado do sistema e o loop de interação."""
    
    # Variáveis de estado do sistema V1 (saldo genérico)
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    # Variáveis de estado do sistema V2 (listas)
    AGENCIA = "0001"
    usuarios = []
    contas = []
    numero_conta = 1 # Variável que rastreia o próximo número de conta disponível

    while True:
        opcao = menu()

        if opcao == "d":
            # VALIDAÇÃO: Não permite depósito se não houver usuários/contas
            if not usuarios:
                print("\n@@@ Operação falhou! É necessário cadastrar um usuário (opção 'nu') antes de depositar. @@@")
                continue # Volta ao início do loop
            
            try:
                valor = float(input("Informe o valor do depósito: "))
                # Atualiza as variáveis locais 'saldo' e 'extrato' com o retorno da função
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\n@@@ Entrada inválida. Por favor, digite um valor numérico. @@@")

        elif opcao == "s":
            # Validação similar para Saque
            if not usuarios:
                print("\n@@@ Operação falhou! É necessário cadastrar um usuário (opção 'nu') antes de sacar. @@@")
                continue

            try:
                valor = float(input("Informe o valor do saque: "))
                # Chamada com argumentos nomeados (keyword only)
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except ValueError:
                print("\n@@@ Entrada inválida. Por favor, digite um valor numérico. @@@")

        elif opcao == "e":
            # Chamada com argumentos posicional e nomeado
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            # Cria o usuário e o adiciona na lista 'usuarios'
            criar_usuario(usuarios) 

        elif opcao == "nc":
            # Cria a conta, vincula ao usuário, adiciona à lista 'contas'
            # e atualiza o contador 'numero_conta'
            numero_conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            
        elif opcao == "lc":
            # Lista todas as contas cadastradas
            listar_contas(contas) 

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema bancário. Até logo! 👋")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Garante que a função main() seja executada quando o script for iniciado
if __name__ == "__main__":
    main()