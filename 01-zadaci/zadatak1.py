lista =  ["Stol", "Stolica", "Krevet","Fotelja"] 
dictionary = {}

def funkcija():
    if isinstance(lista, list):
        if all(isinstance(x, str) for x in lista):
            #rezultat = [x for x in lista if len(x)>4]
            dictionary = { lista.index(x) : x[::-1] for x in lista }  
            print(dictionary)
        else:
            print("error -> u listi nisu svi elemnti tipa string")
    else:
        print("error -> element nije lista")

funkcija()