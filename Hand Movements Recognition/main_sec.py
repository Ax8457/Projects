import sys
from PyQt5 import QtWidgets
import mainInterface as uitf
import loadingInterface as litf
import tkinter as tk
from tkinter import messagebox

user = ['AxelB', 'LoicA', 'CharlesAymericFG', 'ElHadjiBaraC']
true_user = ['Axel', 'Loïc', 'Charles-Aymeric', 'El-Hadji Bara']

#fonction de vérification des infos saisies au clavier
def pass_verif():
    authentification_data = {
        'AxelB': 'tdhAxelESIEE2023',
        'LoicA': 'azerty',
        'CharlesAymericFB': 'tdhCharlesAymericESIEE2023',
        'ElHadjiBaraC': 'tdhElHadjiBaraESIEE2023',
    }

    user_password = entry_pass_field.get()
    user_id = entry_user_field.get()

    for i in range (len(user)):
        username = user[i]
        true_username = true_user[i]
        if user_id == username :
            password = authentification_data.get(username)
            if user_password == password :
                messagebox.showinfo("Success", "Welcome {}. Press 'ok' to launch the application".format(true_username))
                fenetre.destroy()
                if __name__ == "__main__":
                    app = QtWidgets.QApplication(sys.argv)
                    TheDigitalHand = QtWidgets.QMainWindow()
                    ui = uitf.MainInterface()
                    ui.setupUi(TheDigitalHand)
                    ui.mainLoop()
                    loading = litf.LoadingInterface(TheDigitalHand)
                    loading.show()
                    sys.exit(app.exec_())
            else:
                messagebox.showerror("Error", "password incorrect")
        else:
            messagebox.showerror("Error", "Login incorrect")


#Window
fenetre = tk.Tk()
fenetre.title("Authentication")
fenetre.configure(bg="#333")
fenetre.columnconfigure(0, weight=1)
# Définir la taille de la fenêtre
window_width = 300
window_height = 200
# taille de l'écran
screen_width = fenetre.winfo_screenwidth()
screen_height = fenetre.winfo_screenheight()
# Coordonnées de la fenêtre
x = (screen_width-window_width) // 2
y = (screen_height-window_height) // 2
#afficher la fenêter
fenetre.geometry('{}x{}+{}+{}'.format(window_width,window_height,x,y))
#empêcher le redimensionnement
fenetre.resizable(False, False)

#User
user_field = tk.Label(fenetre, text=" Login ")
user_field.grid(row=0, column=0, padx=6, pady=6)
entry_user_field = tk.Entry(fenetre, show="")
entry_user_field.grid(row=1, column=0, padx=6, pady=6)

#Pass
pass_field = tk.Label(fenetre, text=" Password ")
pass_field.grid(row=2, column=0, padx=6, pady=6)
entry_pass_field = tk.Entry(fenetre, show="*")
entry_pass_field.grid(row=3, column=0, padx=6, pady=6)

#Button
button = tk.Button(fenetre, text="Valider", command=pass_verif)
button.grid(row=4, column=0, padx=6, pady=6)

fenetre.mainloop()







