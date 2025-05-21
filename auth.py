import json
import os
from datetime import datetime

ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        usuario_padrao = {
            "admin": {
                "nome": "Administrador",
                "login": "admin",
                "senha": "admin",
                "perfil": "admin",
                "ultimo_login": "",
                "tentativas_falhas": 0,
                "ativo": True
            }
        }
        salvar_usuarios(usuario_padrao)
        return usuario_padrao
    else:
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def autenticar(usuarios):
    for _ in range(3):
        login = input("Login: ")
        senha = input("Senha: ")
        
        usuario = usuarios.get(login)
        if usuario:
            if not usuario["ativo"]:
                print("Conta bloqueada.")
                return None
            if senha == usuario["senha"]:
                usuario["tentativas_falhas"] = 0
                usuario["ultimo_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                salvar_usuarios(usuarios)
                return usuario
            else:
                usuario["tentativas_falhas"] += 1
                print("Senha incorreta.")
                if usuario["tentativas_falhas"] >= 3:
                    usuario["ativo"] = False
                    print("Conta bloqueada por tentativas inválidas.")
                salvar_usuarios(usuarios)
        else:
            print("Usuário não encontrado.")
    return None

def trocar_senha(usuario, usuarios, login_alvo=None):
    if usuario["perfil"] == "admin" and login_alvo:
        if login_alvo in usuarios:
            nova = input(f"Nova senha para {login_alvo}: ")
            usuarios[login_alvo]["senha"] = nova
            print("Senha atualizada.")
        else:
            print("Usuário não encontrado.")
    else:
        nova = input("Digite sua nova senha: ")
        usuarios[usuario["login"]]["senha"] = nova
        print("Senha atualizada com sucesso.")
    salvar_usuarios(usuarios)

def listar_usuarios(usuarios):
    print("\nUsuários:")
    for u in usuarios.values():
        status = "Ativo" if u["ativo"] else "Bloqueado"
        print(f"- {u['nome']} ({u['login']}) [{u['perfil']}] - {status} - Último login: {u['ultimo_login']}")

def bloquear_usuario(usuarios):
    login = input("Digite o login do usuário para (des)bloquear: ")
    if login in usuarios:
        usuarios[login]["ativo"] = not usuarios[login]["ativo"]
        estado = "desbloqueado" if usuarios[login]["ativo"] else "bloqueado"
        print(f"Usuário {estado}.")
        salvar_usuarios(usuarios)
    else:
        print("Usuário não encontrado.")

def cadastrar_usuario(usuarios):
    login = input("Novo login: ")
    if login in usuarios:
        print("Usuário já existe.")
        return
    nome = input("Nome completo: ")
    senha = input("Senha: ")
    perfil = input("Perfil (admin/user): ")
    usuarios[login] = {
        "nome": nome,
        "login": login,
        "senha": senha,
        "perfil": perfil,
        "ultimo_login": "",
        "tentativas_falhas": 0,
        "ativo": True
    }
    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso.")

def menu_admin(usuario, usuarios):
    while True:
        print("\n[Menu Admin]")
        print("1. Listar usuários")
        print("2. Alterar senha de usuário")
        print("3. Bloquear/desbloquear usuário")
        print("4. Cadastrar novo usuário")
        print("5. Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            listar_usuarios(usuarios)
        elif opcao == "2":
            login_alvo = input("Login do usuário: ")
            trocar_senha(usuario, usuarios, login_alvo)
        elif opcao == "3":
            bloquear_usuario(usuarios)
        elif opcao == "4":
            cadastrar_usuario(usuarios)
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

def menu_user(usuario, usuarios):
    while True:
        print("\n[Menu Usuário]")
        print("1. Alterar minha senha")
        print("2. Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            trocar_senha(usuario, usuarios)
        elif opcao == "2":
            break
        else:
            print("Opção inválida.")

def main():
    usuarios = carregar_usuarios()

    # Força troca de senha do admin
    if usuarios["admin"]["senha"] == "admin":
        print("⚠️ Você está usando a senha padrão do admin.")
        while True:
            nova_senha = input("Digite uma nova senha para o admin: ")
            if nova_senha != "admin":
                usuarios["admin"]["senha"] = nova_senha
                salvar_usuarios(usuarios)
                print("Senha do admin alterada com sucesso.")
                break
            else:
                print("A nova senha não pode ser 'admin'.")

    print("=== Sistema de Autenticação ===")
    usuario = autenticar(usuarios)

    if usuario:
        print(f"Bem-vindo, {usuario['nome']}!")
        if usuario['ultimo_login']:
            print(f"Último login: {usuario['ultimo_login']}")
        if usuario["perfil"] == "admin":
            menu_admin(usuario, usuarios)
        else:
            menu_user(usuario, usuarios)
    else:
        print("Acesso negado.")

if __name__ == "__main__":
    main()