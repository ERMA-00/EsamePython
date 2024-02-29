class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name

    def get_data(self):

        # Verifico che il file di dati abbia estensione csv
        estensione_file = self.name.split('.')[-1]
        if estensione_file != 'csv':
            raise ExamException('L\'estensione {} non può essere accettata'.format(estensione_file))

        # Provo ad aprire il file
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except:
            raise ExamException('Impossibile aprire il file') 
        
        # Se il file si riesce ad aprire
        else:
            # Creo l'array dove andrò a salvare i dati
            data = []

            # Apro il file in formato read
            my_file = open(self.name, 'r')

            # Per ogni riga nel file
            for line in my_file:

                # Pulisco la riga da spazi inutili
                line = line.strip()

                # Se trovo una riga e c'è almeno una virgola
                if line and ',' in line:

                    # Divido gli elementi della riga
                    elements = line.split(',')
                    
                    # Se sulla stessa riga ci sono altri valori, 
                    # tengo solamente i primi due che leggo
                    try:
                        elements = elements[:2]
                    except:
                        pass

                    # Elimina gli spazi vuoti nella data
                    elements[0] = elements[0].replace(' ','')
                    
                    # Controlla che i valori nella data siano tutti numeri
                    tutti_numeri = True
                    for lettera in elements[0]:
                        if lettera == '-':
                            continue
                        elif not lettera.isdigit() or int(lettera) < 0:
                            tutti_numeri = False

                    # Rendo i valori degli interi
                    try:
                        elements[1] = int(elements[1])
                    except:
                        continue

                    # Verifico che l'anno e il mese siano validi
                    mesi_validi = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                    data_valida = True
                    try:
                        anno = elements[0].split('-')[0]
                        mese = elements[0].split('-')[1]
                        if int(anno) <= 0 or mese not in mesi_validi:
                            data_valida = False
                    except:
                        continue

                    # Se tutte le condizioni sono rispettate
                    # appendo gli elementi all'array dei dati
                    if data_valida and tutti_numeri and elements[1] > 0:
                        data.append(elements)
                    
                    # altrimenti proseguo alla riga successiva

            # Quando ho finito di salvare i dati chiudo il file 
            my_file.close()

            # Controllo che la lista non sia vuota 
            if data == []:
                raise ExamException('Il file non contiene nessuno valore')

            # Creo una lista con solo gli anni e i mesi
            anno_mese = []
            for item in data:
                anno_mese_divisi = item[0].split('-')
                anno_mese.append(anno_mese_divisi)
            
            # Controllo che gli anni e i mesi siano ordinati cronologicamente
            if anno_mese != sorted(anno_mese):
                raise ExamException('I dati non sono ordinati cronologicamente')
            
            # Controllo che non ci siano duplicati
            for i,item in enumerate(anno_mese):
                for index in range(i+1, len(anno_mese)):
                    if item == anno_mese[index]:
                        raise ExamException('Ci sono duplicati tra gli elementi del file CSV')

            # Se tutto è ok, restituisco l'array di dati        
            return data
 
def find_min_max(time_series):
    min_value = 0
    max_value = 0
    min = []
    max = []
    dizionario_anni = {}

    for element in time_series: 

        # Salvo i valori nelle rispettive variabili            
        anno = element[0].split("-")[0]
        mese = element[0].split("-")[1]
        dato = element[1]

        # Se non ho l'anno nel dizionario lo aggiungo
        # e imposto il primo valore che trovo a min e max
        if anno not in dizionario_anni:
            min = []
            max = []
            min_value = dato
            max_value = dato
            min.append(mese)
            max.append(mese)
            dizionario_min_max = {'min': min, 'max': max}
            dizionario_anni[anno] = dizionario_min_max
        else:

            # Se ho già l'anno nel dizionario 
            # controllo se il valore è maggiore dei maggiori precedenti
            if dato > max_value:
                max.clear()
                max_value = dato
                max.append(mese)
            # se è uguale lo appendo alla lista dei maggiori
            elif dato == max_value:
                    max.append(mese)
            
            # controllo se il valore è minore dei minori precedenti
            if dato < min_value:
                min.clear()
                min_value = dato
                min.append(mese)
            # se è uguale lo appendo alla lista dei minori
            elif dato == min_value:
                    min.append(mese)
            
            # Dopo aver verificato tutto 
            # aggiungo i nuovi valori al dizionario
            dizionario_min_max = {'min': min, 'max': max}
            dizionario_anni[anno] = dizionario_min_max

    return dizionario_anni