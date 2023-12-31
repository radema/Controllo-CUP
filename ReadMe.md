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

**Nota bene:** i file di input vanno inseriti nella cartella `data` e non nelle sottocartelle. 

## Installazione

Per installare il progetto, eseguire i seguenti comandi nella cartella di lavoro:

```
git clone https://github.com/radema/Controllo-CUP.git

make activate-env

conda activate controllo_cup
```

## Uso

Per eseguire il progetto, eseguire il seguente comando nella cartella di lavoro:

```
python src/main.py data/progetti_esteso_OC.zip CUP Estrazione_CUP.xlsx
```

## Utilizzo tramite [Google Colab](https://colab.research.google.com/?hl=it)

### Prerequisiti

* account per accedere a Google Colab

* accesso alla repository GitHub

### Istruzioni

1. Accedere a [Google Colab](https://colab.research.google.com/?hl=it) tramite il proprio account

2. In fase di accesso, optare per l'opzione `github'

3. cercare per `radema` nella barra di ricerca e selezionare la repository `Controllo-Cup`

4. Aprire il foglio `controllo_cup.ipynb`

5. Eseguire le prime due celle

6. Seguire le istruzioni del notebook
