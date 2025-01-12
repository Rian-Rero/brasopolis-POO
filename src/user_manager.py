import os
from typing import Dict, Optional

class UserManager:
    def __init__(self, filepath: str = "src/DataBase/users.txt") -> None:
        self.filepath: str = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                pass

    def login_or_register(self) -> Dict[str, str]:
        while True:
            choice: str = input("Você quer [1] Logar ou [2] Registrar? ")
            if choice == "1":
                return self.login()
            elif choice == "2":
                return self.register()
            else:
                print("Escolha inválida. Tente novamente.")

    def login(self) -> Dict[str, str]:
        name: str = input("Digite seu nome de usuário: ")
        with open(self.filepath, "r") as f:
            for line in f:
                user_data: list[str] = line.strip().split(",")
                if user_data[0] == name:
                    print("Login bem-sucedido!")
                    return {"name": name}
        print("Usuário não encontrado. Tente novamente ou registre-se.")
        return self.login_or_register()

    def register(self) -> Dict[str, str]:
        name: str = input("Digite seu nome de usuário: ")
        with open(self.filepath, "a") as f:
            f.write(f"{name}\n")
        print("Registro bem-sucedido!")
        return {"name": name}