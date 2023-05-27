from stegano import lsb
import os

msg = "Testowe ukrywanie wiadomosci w obrazku baloniki"

img_in = input("Podaj ścieżkę do pliku: ")
while os.path.isfile(img_in) == False or img_in[-4:] != ".png": img_in = input("Podaj ścieżkę do pliku: ")
option = input("1 -> odszyfruj wiadomość; 0 -> schowaj w obrazku: ") 
while option != "0" and option != "1": option = input("1 -> odszyfruj wiadomość; 0 -> schowaj w obrazku: ") 


if option == "0":
    img_out = img_in[0:-4] + "_hide" + img_in[-4:]
    lsb.hide(img_in, message = msg).save(img_out)
    print("Utworzono plik z ukrytą wiadomością:", img_out)
elif option == "1":
    view_msg = lsb.reveal(img_in)
    print("Ukryta wiadomość:", view_msg)

#C:\Users\hp\Studia\ATG\balloons.png
#C:\Users\hp\Studia\ATG\balloons_hide.png