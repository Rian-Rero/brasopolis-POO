import os


class UserManager:
    def __init__(self, filepath="users.txt"):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                pass

    def login_or_register(self):
        while True:
            choice = input("Você quer [1] Logar ou [2] Registrar? ")
            if choice == "1":
                return self.login()
            elif choice == "2":
                return self.register()
            else:
                print("Escolha inválida. Tente novamente.")

    def login(self):
        name = input("Digite seu nome de usuário: ")
        with open(self.filepath, "r") as f:
            for line in f:
                user_data = line.strip().split(",")
                if user_data[0] == name:
                    print("Login bem-sucedido!")
                    return {"name": name}
        print("Usuário não encontrado. Tente novamente ou registre-se.")
        return self.login_or_register()

    def register(self):
        name = input("Digite seu nome de usuário: ")
        with open(self.filepath, "a") as f:
            f.write(f"{name}\n")
        print("Registro bem-sucedido!")
        return {"name": name}
