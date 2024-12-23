import customtkinter
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "usuarios.csv")

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("dark-blue") 

#paramentros
rootlogin = customtkinter.CTk()
rootlogin.geometry('600x300')
rootlogin.title('Brasópilis')
rootlogin.resizable(False,False)

#funções
def acess():
    username = user_label.get()
    password = passw_label.get()
    try:
        with open(csv_path, "r") as file:
            usuarios = file.readlines()
            for usuario in usuarios:
                stored_username, stored_password = usuario.strip().split(",")
                if username == stored_username and password == stored_password:
                    print('Login feito com sucesso!')
                    return
        print('Usuário ou senha incorretos!')
    except FileNotFoundError:
        print('Nenhum usuário registrado ainda.')

def registro():
    username = user_label.get()
    password = passw_label.get()
    if username and password:
        # Salva os dados em um arquivo
        with open(csv_path, "a") as file:
            file.write(f"{username},{password}\n")
        print('Registro feito com sucesso!')
    else:
        print('Por favor, preencha os campos de usuário e senha.')

#Label Introdução
intro = customtkinter.CTkLabel(rootlogin,text='Login')
intro.pack(padx=10, pady=10)

# entradas
user_label  = customtkinter.CTkEntry(rootlogin,placeholder_text='Digite o seu usuário')
user_label.pack(padx=10, pady=10)

passw_label = customtkinter.CTkEntry(rootlogin, placeholder_text='Digite a sua senha',show="*")
passw_label.pack(padx=10, pady=10)

checkbox = customtkinter.CTkCheckBox(rootlogin,text='Lembrar Senha')
checkbox.pack(anchor='center')

# Botões
login = customtkinter.CTkButton(rootlogin, text='Acessar', command= acess)
login.pack(padx=10, pady=10)

regist = customtkinter.CTkButton(rootlogin, text='Registrar', command= registro)
regist.pack(padx=10, pady=10)

rootlogin.mainloop()
