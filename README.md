# 🐍 Desafio DIO Luizalabs: Sistema Bancário Modularizado (Back-end com Python)

Este projeto consiste em um sistema bancário simplificado, operado via console (terminal). O código foi refatorado para adotar o **paradigma funcional** e as boas práticas de **modularização**, atendendo aos requisitos da Versão 1 (criação e vinculação de clientes e contas) do desafio.

## ✨ Funcionalidades Implementadas (V1)

O sistema oferece as seguintes opções de operação:

| Opção | Descrição | Regras de Argumentos |
| :---: | :--- | :--- |
| **`d`** | Depositar valor na conta (requer usuário cadastrado). | Apenas **Posicional** (`/`) |
| **`s`** | Sacar valor (sujeito a limites e saldo). | Apenas **Nomeado** (`*`) |
| **`e`** | Exibir o extrato de movimentações e saldo. | **Misto** (Posicional e Nomeado) |
| **`nu`** | **Novo Usuário**: Cadastra um novo cliente (pessoa física). | - |
| **`nc`** | **Nova Conta**: Cria uma conta corrente e a **vincula** a um usuário existente. | - |
| **`lc`** | Listar todas as contas correntes cadastradas. | - |
| **`q`** | Sair do sistema. | - |

---

## 🔒 Regras de Negócio e Modularização

### 1. Requisitos de Transação
* **Limite de Saque (Valor):** Máximo de **R$ 500,00** por operação.
* **Limite de Saque (Frequência):** Máximo de **3 saques** diários.
* **Depósito/Saque:** O valor deve ser sempre positivo.
* **Validação Inicial:** Não permite Depósito (`d`) ou Saque (`s`) se **nenhum usuário** (`nu`) tiver sido cadastrado.

### 2. Requisitos da Versão 2
* **Usuário (`nu`):** Deve ser único, validado pelo **CPF** (somente números). Armazena nome, data de nascimento, CPF e endereço.
* **Conta Corrente (`nc`):**
    * Agência fixa: **`0001`**.
    * Número da conta é **sequencial**, iniciando em `1`.
    * A conta é **vinculada a um objeto/dicionário de Usuário** existente (buscado via CPF).

### 3. Implementação Funcional
As operações de transação seguem estritamente as regras de passagem de argumentos definidas no desafio:

| Função | Assinatura | Tipo de Argumento |
| :--- | :--- | :--- |
| `depositar` | `(saldo, valor, extrato, /)` | **Posicional** (`positional only`) |
| `sacar` | `(*, saldo, valor, extrato, ...)` | **Nomeado** (`keyword only`) |
| `exibir_extrato` | `(saldo, /, *, extrato)` | **Misto** (Posicional e Nomeado) |

---

## ▶️ Como Rodar o Projeto

### Pré-requisitos
Certifique-se de ter o **Python 3** instalado em sua máquina.

### Execução

1.  **Clone o repositório** e navegue até a pasta do projeto:
    ```bash
    git clone [https://github.com/Wallacet28/desafio_dio-banco.git](https://github.com/Wallacet28/desafio_dio-banco.git)
    cd desafio_dio-banco
    ```
2.  **Execute o script:**
    ```bash
    python banco.py
    ```

### 💡 Dicas de Uso
Para testar o sistema completo, a ordem recomendada de operações é: `nu` -> `nc` -> `lc` -> `d`/`s`/`e`.

---

## 🧑‍💻 Autor

Desenvolvido por **Wallace Tadeu** como parte do desafio da trilha **Back-end com Python** da DIO em parceria com a Luizalabs.

**[Link para o Repositório no GitHub](https://github.com/Wallacet28/desafio_dio-banco)**
