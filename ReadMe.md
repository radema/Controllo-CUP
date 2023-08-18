# Controllo CUP

Questa repository contiene il codice Python che esegue un controllo sui codici CUP. Il codice prende tre argomenti:

* Il percorso del file .zip che contiene i dati di OpenCoesione.
* Il nome della scheda CUP nel file Estrazione CUP da PAdigitale2026, che contiene l'elenco dei codici CUP da controllare.
* Il nome della cartella CUP da controllare.
Il codice prima legge i dati dai due file. Quindi esegue una serie di controlli sui codici CUP, tra cui:

* Se il codice CUP è già presente in OpenCoesione.
* Se il codice CUP è presente nel feedback dal DIPE.
* Se il codice CUP è associato al modello corretto.
Il codice quindi classifica i codici CUP secondo una scala di priorità. Le possibili classificazioni sono:

* "CUP già presente in OPEN COESIONE" (CUP già presente in OpenCoesione)
* "CUP NON PRESENTE NEL FEEDBACK DIPE" (CUP non presente nel feedback dal DIPE)
* "CUP PRESENTE IN PIU' CANDIDATURE" (CUP presente in più candidature)
* "TEMPLATE MANCANTE" (Template mancante)
* "POSSIBILE TEMPLATE ERRATO" (Possibile template errato)
* "NESSUN PROBLEMA RISCONTRATO AL MOMENTO" (Nessun problema trovato al momento)
Infine, il codice crea due file di output:

* KPI_aggregati.csv, che contiene il numero di codici CUP per ogni classificazione.
* CUP_ANALYSIS.xlsx, che contiene tutti i dati per tutti i codici CUP, inclusa la classificazione.

## Installazione

Per installare il progetto, eseguire il seguente comando nella cartella di lavoro:

'''
pip install -r requirements.txt
'''

## Uso

Per eseguire il progetto, eseguire il seguente comando nella cartella di lavoro:

'''
python src/main.py data/progetti_esteso_OC.zip CUP Estrazione_CUP.xlsx
'''
