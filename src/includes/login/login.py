import customtkinter
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "usuarios.csv")

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("dark-blue") 

rootlogin = customtkinter.CTk()
rootlogin.geometry('600x400')
rootlogin.title('Brasópilis')
rootlogin.resizable(False, False)

num_jogadores = 0
jogadores_atual = 0

# Funções
def iniciar():
    global num_jogadores
    try:
        num_jogadores = int(num_jogadores_entry.get())
        if num_jogadores > 0:
            intro.pack_forget()
            num_jogadores_label.pack_forget()
            num_jogadores_entry.pack_forget()
            iniciar_button.pack_forget()
            show_login_ui()
        else:
            print("O número de jogadores deve ser maior que zero.")
    except ValueError:
        print("Por favor, insira um número válido.")

def show_login_ui():
    intro.configure(text=f'Jogador {jogadores_atual + 1}/{num_jogadores}, faça login ou registre-se:')
    intro.pack(padx=10, pady=10)
    user_label.pack(padx=10, pady=10)
    passw_label.pack(padx=10, pady=10)
    login_button.pack(padx=10, pady=10)
    regist_button.pack(padx=10, pady=10)

def acess():
    global jogadores_atual
    username = user_label.get()
    password = passw_label.get()
    try:
        with open(csv_path, "r") as file:
            usuarios = file.readlines()
            for usuario in usuarios:
                stored_username, stored_password = usuario.strip().split(",")
                if username == stored_username and password == stored_password:
                    print(f'Login feito com sucesso para {username}!')
                    jogadores_atual += 1
                    clear_entries()
                    if jogadores_atual < num_jogadores:
                        show_login_ui()
                    else:
                        print("Todos os jogadores fizeram login com sucesso!")
                        rootlogin.destroy()
                    return
        print('Usuário ou senha incorretos!')
    except FileNotFoundError:
        print('Nenhum usuário registrado ainda.')

def registro():
    global jogadores_atual
    username = user_label.get()
    password = passw_label.get()
    if username and password:
        with open(csv_path, "a") as file:
            file.write(f"{username},{password}\n")
        print(f'Registro feito com sucesso para {username}!')
        jogadores_atual += 1
        clear_entries()
        if jogadores_atual < num_jogadores:
            show_login_ui()
        else:
            print("Todos os jogadores fizeram login ou registro com sucesso!")
            rootlogin.destroy()
    else:
        print('Por favor, preencha os campos de usuário e senha.')

def clear_entries():
    user_label.delete(0, 'end')
    passw_label.delete(0, 'end')


intro = customtkinter.CTkLabel(rootlogin, text='Informe o número de jogadores:')
intro.pack(padx=10, pady=10)

num_jogadores_label = customtkinter.CTkLabel(rootlogin, text='Número de jogadores:')
num_jogadores_label.pack(padx=10, pady=10)

num_jogadores_entry = customtkinter.CTkEntry(rootlogin, placeholder_text='Digite o número de jogadores')
num_jogadores_entry.pack(padx=10, pady=10)

iniciar_button = customtkinter.CTkButton(rootlogin, text='Iniciar', command=iniciar)
iniciar_button.pack(padx=10, pady=10)

user_label = customtkinter.CTkEntry(rootlogin, placeholder_text='Digite o seu usuário')
passw_label = customtkinter.CTkEntry(rootlogin, placeholder_text='Digite a sua senha', show="*")

login_button = customtkinter.CTkButton(rootlogin, text='Acessar', command=acess)
regist_button = customtkinter.CTkButton(rootlogin, text='Registrar', command=registro)

rootlogin.mainloop()
