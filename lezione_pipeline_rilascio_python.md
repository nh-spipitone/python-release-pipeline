# Lezione: Creare una pipeline di rilascio per un progetto Python

## Durata consigliata

- Giorno 1: 3 ore
- Giorno 2: 3 ore

## Obiettivo della lezione

L'obiettivo di questa lezione è capire come costruire una semplice pipeline di rilascio per un progetto Python.

Alla fine della lezione gli studenti dovrebbero saper:

- creare un piccolo progetto Python strutturato;
- scrivere test automatici con `pytest`;
- capire perché i test sono importanti prima di rilasciare codice;
- creare un file `requirements.txt`;
- usare Git per versionare il progetto;
- collegare il progetto a GitHub;
- creare una pipeline automatica con GitHub Actions;
- verificare se una modifica può essere rilasciata oppure no.

---

# 1. Che cos'è una pipeline di rilascio?

Una pipeline di rilascio è una sequenza automatica di passaggi che viene eseguita prima di pubblicare o distribuire un progetto software.

In modo molto semplice, una pipeline risponde a questa domanda:

> Possiamo fidarci di questo codice prima di rilasciarlo?

Una pipeline reale può contenere molti passaggi, per esempio:

- installazione delle dipendenze;
- esecuzione dei test;
- controllo dello stile del codice;
- analisi di sicurezza;
- build del progetto;
- deploy su un server;
- pubblicazione di una nuova versione.

In questa lezione ci concentreremo su una versione semplice ma molto utile:

```text
Scrivo codice -> eseguo test -> se i test passano posso rilasciare
```

---

# 2. Perché usare i test automatici?

I test automatici servono a controllare che il codice funzioni come previsto.

Senza test, ogni volta che modifichiamo il progetto dobbiamo controllare manualmente se tutto funziona ancora.

Con i test automatici, invece, possiamo far controllare al computer se abbiamo rotto qualcosa.

Esempio:

```python
assert somma(2, 3) == 5
```

Questa riga significa:

> Mi aspetto che la funzione `somma(2, 3)` restituisca `5`.

Se il risultato è diverso, il test fallisce.

---

# 3. Struttura del progetto

Creiamo un progetto Python molto semplice.

La struttura sarà questa:

```text
python-release-pipeline/
│
├── src/
│   └── calculator.py
│
├── tests/
│   └── test_calculator.py
│
├── requirements.txt
└── README.md
```

Significato delle cartelle e dei file:

| Percorso | Descrizione |
|---|---|
| `src/` | Contiene il codice principale del progetto |
| `tests/` | Contiene i test automatici |
| `requirements.txt` | Contiene le dipendenze del progetto |
| `README.md` | Descrive il progetto |

---

# 4. Creazione del progetto

Apriamo il terminale e creiamo la cartella del progetto.

```bash
mkdir python-release-pipeline
cd python-release-pipeline
```

Creiamo le cartelle principali:

```bash
mkdir src tests
```

Creiamo i file:

```bash
touch src/calculator.py
touch tests/test_calculator.py
touch README.md
touch requirements.txt
```

Su Windows, se il comando `touch` non funziona, possiamo creare i file manualmente da Visual Studio Code oppure usare:

```powershell
New-Item src/calculator.py
New-Item tests/test_calculator.py
New-Item README.md
New-Item requirements.txt
```

---

# 5. Creazione dell'ambiente virtuale

Un ambiente virtuale serve a isolare le dipendenze del progetto.

Creiamolo con:

```bash
python -m venv venv
```

Attiviamolo.

Su Windows:

```bash
venv\Scripts\activate
```

Su macOS/Linux:

```bash
source venv/bin/activate
```

Quando l'ambiente virtuale è attivo, nel terminale dovrebbe comparire qualcosa del tipo:

```text
(venv)
```

---

# 6. Installazione di pytest

`pytest` è una libreria Python che permette di scrivere ed eseguire test automatici.

Installiamola:

```bash
pip install pytest
```

Aggiorniamo il file `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Il file `requirements.txt` dovrebbe contenere una riga simile a questa:

```text
pytest==...
```

Il numero della versione può cambiare.

---

# 7. Scrittura del codice principale

Apriamo il file:

```text
src/calculator.py
```

Inseriamo questo codice:

```python
def somma(a, b):
    return a + b


def sottrai(a, b):
    return a - b


def moltiplica(a, b):
    return a * b


def dividi(a, b):
    if b == 0:
        raise ValueError("Non puoi dividere per zero")
    return a / b
```

Abbiamo creato quattro funzioni:

- `somma`;
- `sottrai`;
- `moltiplica`;
- `dividi`.

La funzione `dividi` contiene anche un controllo: se proviamo a dividere per zero, genera un errore.

---

# 8. Scrittura dei test con pytest

Apriamo il file:

```text
tests/test_calculator.py
```

Inseriamo questo codice:

```python
import pytest
from src.calculator import somma, sottrai, moltiplica, dividi


def test_somma():
    assert somma(2, 3) == 5


def test_sottrai():
    assert sottrai(10, 4) == 6


def test_moltiplica():
    assert moltiplica(3, 4) == 12


def test_dividi():
    assert dividi(10, 2) == 5


def test_dividi_per_zero():
    with pytest.raises(ValueError):
        dividi(10, 0)
```

Ogni funzione che inizia con `test_` viene riconosciuta automaticamente da `pytest`.

Esempio:

```python
def test_somma():
    assert somma(2, 3) == 5
```

Questo test controlla che la funzione `somma` funzioni correttamente.

---

# 9. Esecuzione dei test

Dal terminale, nella cartella principale del progetto, eseguiamo:

```bash
pytest
```

Se tutto funziona, dovremmo vedere un risultato simile:

```text
5 passed
```

Questo significa che tutti i test sono stati superati.

---

# 10. Simuliamo un errore

Ora modifichiamo volutamente la funzione `somma` in modo sbagliato.

Nel file `src/calculator.py`, cambiamo:

```python
def somma(a, b):
    return a + b
```

in:

```python
def somma(a, b):
    return a - b
```

Eseguiamo di nuovo:

```bash
pytest
```

Questa volta un test dovrebbe fallire.

Questo è il punto importante:

> Il test ci ha avvisati che abbiamo rotto una funzionalità.

Senza test, potremmo non accorgercene subito.

Correggiamo la funzione:

```python
def somma(a, b):
    return a + b
```

E rieseguiamo:

```bash
pytest
```

Ora i test dovrebbero passare di nuovo.

---

# 11. Primo concetto di pipeline

Anche senza GitHub Actions, possiamo già immaginare una pipeline locale molto semplice:

```text
1. Installa le dipendenze
2. Esegui i test
3. Se i test passano, il codice può essere rilasciato
4. Se i test falliscono, il rilascio viene bloccato
```

Possiamo anche creare uno script locale.

## Script per Windows

Creiamo un file chiamato:

```text
release_check.bat
```

Contenuto:

```bat
@echo off

echo Avvio dei test...
pytest

if %errorlevel% neq 0 (
    echo Test falliti. Release bloccata.
    exit /b 1
)

echo Test superati. Il progetto puo essere rilasciato.
```

Esecuzione:

```bash
release_check.bat
```

## Script per macOS/Linux

Creiamo un file chiamato:

```text
release_check.sh
```

Contenuto:

```bash
#!/bin/bash

echo "Avvio dei test..."
pytest

if [ $? -ne 0 ]; then
    echo "Test falliti. Release bloccata."
    exit 1
fi

echo "Test superati. Il progetto può essere rilasciato."
```

Rendiamolo eseguibile:

```bash
chmod +x release_check.sh
```

Eseguiamolo:

```bash
./release_check.sh
```

---

# 12. Esercizio guidato del Giorno 1

## Obiettivo

Aggiungere una nuova funzione e scrivere i relativi test.

## Parte 1

Nel file `src/calculator.py`, aggiungere questa funzione:

```python
def potenza(a, b):
    return a ** b
```

## Parte 2

Nel file `tests/test_calculator.py`, importare la funzione:

```python
from src.calculator import somma, sottrai, moltiplica, dividi, potenza
```

## Parte 3

Aggiungere il test:

```python
def test_potenza():
    assert potenza(2, 3) == 8
```

## Parte 4

Eseguire:

```bash
pytest
```

## Domanda per la classe

Cosa succede se modifichiamo la funzione `potenza` in modo errato?

Esempio:

```python
def potenza(a, b):
    return a * b
```

I test passano o falliscono?

---

# 13. Introduzione a Git

Git serve a tenere traccia delle modifiche del progetto.

Inizializziamo Git nella cartella del progetto:

```bash
git init
```

Aggiungiamo tutti i file:

```bash
git add .
```

Creiamo il primo commit:

```bash
git commit -m "Primo commit con progetto Python e test"
```

---

# 14. Creazione del repository su GitHub

Andiamo su GitHub e creiamo un nuovo repository, per esempio:

```text
python-release-pipeline
```

Poi colleghiamo il repository locale a quello remoto.

Il comando sarà simile a questo:

```bash
git remote add origin https://github.com/NOME-UTENTE/python-release-pipeline.git
```

Poi inviamo il codice su GitHub:

```bash
git branch -M main
git push -u origin main
```

---

# 15. Che cos'è GitHub Actions?

GitHub Actions è uno strumento di GitHub che permette di eseguire pipeline automatiche.

Per esempio, possiamo dire a GitHub:

> Ogni volta che qualcuno fa push sul branch main, installa Python, installa le dipendenze ed esegui i test.

Questa è una pipeline di Continuous Integration, spesso abbreviata in CI.

CI significa:

```text
Continuous Integration
```

Cioè integrazione continua.

L'idea è semplice:

> Ogni modifica viene controllata automaticamente.

---

# 16. Creazione della pipeline con GitHub Actions

Creiamo questa struttura nel progetto:

```text
.github/
└── workflows/
    └── python-ci.yml
```

Da terminale:

```bash
mkdir -p .github/workflows
```

Su Windows, se `mkdir -p` non funziona, possiamo creare manualmente le cartelle oppure usare:

```powershell
New-Item -ItemType Directory -Force .github/workflows
```

Creiamo il file:

```text
.github/workflows/python-ci.yml
```

Inseriamo questo contenuto:

```yaml
name: Python CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Scarica il codice
        uses: actions/checkout@v4

      - name: Installa Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Installa dipendenze
        run: pip install -r requirements.txt

      - name: Esegui test
        run: pytest
```

---

# 17. Spiegazione del file YAML

Analizziamo il file pezzo per pezzo.

## Nome della pipeline

```yaml
name: Python CI
```

Questo è il nome che vedremo nella sezione Actions di GitHub.

## Quando parte la pipeline

```yaml
on:
  push:
    branches:
      - main
  pull_request:
```

La pipeline parte quando:

- viene fatto un push sul branch `main`;
- viene aperta o aggiornata una pull request.

## Job

```yaml
jobs:
  test:
```

Un job è un gruppo di operazioni da eseguire.

In questo caso abbiamo un job chiamato `test`.

## Sistema operativo

```yaml
runs-on: ubuntu-latest
```

La pipeline verrà eseguita su una macchina virtuale Linux fornita da GitHub.

## Steps

```yaml
steps:
```

Gli steps sono i singoli passaggi della pipeline.

### Scaricare il codice

```yaml
- name: Scarica il codice
  uses: actions/checkout@v4
```

Questo passaggio scarica il codice del repository dentro la macchina virtuale.

### Installare Python

```yaml
- name: Installa Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

Questo passaggio installa Python 3.12.

### Installare le dipendenze

```yaml
- name: Installa dipendenze
  run: pip install -r requirements.txt
```

Questo passaggio installa le librerie indicate nel file `requirements.txt`.

### Eseguire i test

```yaml
- name: Esegui test
  run: pytest
```

Questo passaggio esegue i test automatici.

Se i test falliscono, la pipeline fallisce.

---

# 18. Invio della pipeline su GitHub

Dopo aver creato il file `python-ci.yml`, salviamo tutto e facciamo commit.

```bash
git add .
git commit -m "Aggiunta pipeline CI con GitHub Actions"
git push
```

Ora andiamo su GitHub, nel repository, e apriamo la sezione:

```text
Actions
```

Dovremmo vedere la pipeline in esecuzione.

Se tutto va bene, il risultato sarà verde.

---

# 19. Simuliamo una pipeline fallita

Ora modifichiamo volutamente una funzione in modo sbagliato.

Nel file `src/calculator.py`, cambiamo:

```python
def moltiplica(a, b):
    return a * b
```

in:

```python
def moltiplica(a, b):
    return a + b
```

Eseguiamo localmente:

```bash
pytest
```

I test dovrebbero fallire.

Facciamo comunque commit e push per vedere cosa succede su GitHub:

```bash
git add .
git commit -m "Errore volontario nella moltiplicazione"
git push
```

Su GitHub Actions la pipeline dovrebbe fallire.

Questo significa:

> GitHub ha controllato il codice e ha trovato un problema prima del rilascio.

Correggiamo il codice:

```python
def moltiplica(a, b):
    return a * b
```

Poi:

```bash
git add .
git commit -m "Correzione funzione moltiplica"
git push
```

La pipeline dovrebbe tornare verde.

---

# 20. Aggiungiamo un messaggio di rilascio simbolico

Per rendere più chiaro il concetto di rilascio, possiamo aggiungere uno step finale.

Modifichiamo il file `.github/workflows/python-ci.yml` così:

```yaml
name: Python CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Scarica il codice
        uses: actions/checkout@v4

      - name: Installa Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Installa dipendenze
        run: pip install -r requirements.txt

      - name: Esegui test
        run: pytest

      - name: Release simbolica
        run: echo "Test superati. Il progetto può essere rilasciato."
```

Questo non pubblica davvero il progetto, ma mostra il concetto:

> Il rilascio avviene solo dopo il superamento dei test.

---

# 21. Esercizio guidato del Giorno 2

## Obiettivo

Gli studenti devono modificare il progetto e osservare il comportamento della pipeline.

## Parte 1

Aggiungere una nuova funzione nel file `src/calculator.py`:

```python
def modulo(a, b):
    if b == 0:
        raise ValueError("Non puoi fare modulo per zero")
    return a % b
```

## Parte 2

Aggiornare gli import nel file `tests/test_calculator.py`:

```python
from src.calculator import somma, sottrai, moltiplica, dividi, potenza, modulo
```

## Parte 3

Aggiungere i test:

```python
def test_modulo():
    assert modulo(10, 3) == 1


def test_modulo_per_zero():
    with pytest.raises(ValueError):
        modulo(10, 0)
```

## Parte 4

Eseguire i test in locale:

```bash
pytest
```

## Parte 5

Se i test passano, fare commit e push:

```bash
git add .
git commit -m "Aggiunta funzione modulo con test"
git push
```

## Parte 6

Controllare la sezione Actions su GitHub.

Domande:

- La pipeline è partita?
- La pipeline è verde o rossa?
- Se è rossa, quale step è fallito?
- Che messaggio di errore vediamo?

---

# 22. Domande di riepilogo

1. Che cos'è una pipeline di rilascio?
2. Perché è utile eseguire i test prima di rilasciare il codice?
3. A cosa serve `pytest`?
4. A cosa serve il file `requirements.txt`?
5. A cosa serve Git?
6. A cosa serve GitHub Actions?
7. Cosa succede se un test fallisce nella pipeline?
8. Perché una pipeline può aiutare un team di sviluppo?

---

# 23. Mini verifica pratica

## Consegna

Partendo dal progetto creato in classe, aggiungere una nuova funzione:

```python
def media(numeri):
    if len(numeri) == 0:
        raise ValueError("La lista non può essere vuota")
    return sum(numeri) / len(numeri)
```

Poi creare almeno due test:

1. un test con una lista di numeri valida;
2. un test con una lista vuota.

Esempio:

```python
def test_media():
    assert media([10, 20, 30]) == 20


def test_media_lista_vuota():
    with pytest.raises(ValueError):
        media([])
```

Infine:

```bash
pytest
git add .
git commit -m "Aggiunta funzione media con test"
git push
```

Controllare che la pipeline GitHub Actions sia verde.

---

# 24. Possibile estensione: controllo dello stile con ruff

Se rimane tempo, si può mostrare un secondo controllo automatico: lo stile del codice.

Installiamo `ruff`:

```bash
pip install ruff
pip freeze > requirements.txt
```

Eseguiamo:

```bash
ruff check .
```

Possiamo aggiungerlo alla pipeline:

```yaml
      - name: Controlla stile codice
        run: ruff check .
```

La pipeline diventerebbe:

```yaml
name: Python CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Scarica il codice
        uses: actions/checkout@v4

      - name: Installa Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Installa dipendenze
        run: pip install -r requirements.txt

      - name: Controlla stile codice
        run: ruff check .

      - name: Esegui test
        run: pytest

      - name: Release simbolica
        run: echo "Controlli superati. Il progetto può essere rilasciato."
```

Questa parte è opzionale.

Se la classe è alle prime armi, è meglio concentrarsi bene su `pytest` e GitHub Actions.

---

# 25. Cosa abbiamo imparato

In questa lezione abbiamo visto come creare una pipeline semplice per un progetto Python.

Abbiamo imparato che:

- una pipeline automatizza i controlli prima del rilascio;
- i test automatici aiutano a evitare regressioni;
- `pytest` permette di scrivere test in modo semplice;
- `requirements.txt` permette di reinstallare le dipendenze del progetto;
- Git tiene traccia delle modifiche;
- GitHub Actions permette di eseguire controlli automatici online;
- se i test falliscono, la pipeline si blocca;
- se i test passano, il progetto può essere considerato pronto per il rilascio.

---

# 26. Schema finale della pipeline

```text
Push su GitHub
      |
      v
GitHub Actions si avvia
      |
      v
Scarica il codice
      |
      v
Installa Python
      |
      v
Installa le dipendenze
      |
      v
Esegue i test con pytest
      |
      v
Test passati?
      |
      |--- No ---> Pipeline rossa, rilascio bloccato
      |
      |--- Sì ---> Pipeline verde, rilascio possibile
```

---

# 27. Frase chiave da ricordare

> Una pipeline non serve a scrivere codice al posto nostro, ma serve a controllare automaticamente che il codice sia abbastanza affidabile da essere rilasciato.

