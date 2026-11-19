# TagStore: design doc per la distribuzione come app desktop

Versione 0.1. Riassume le scelte fatte per trasformare TagStore in un'app che l'utente installa con un doppio clic, senza Python né GitHub. La finestra e la posizione della configurazione sono decise. La firma del codice resta aperta.

## 1. Obiettivo

Oggi TagStore si usa lanciando `python -m tagstore.web --root <cartella>` dopo aver installato Python e le dipendenze. L'obiettivo è che un utente non tecnico possa:

- scaricare un solo file di installazione;
- installarlo come qualsiasi programma Windows;
- aprire TagStore da un'icona, scegliere la cartella delle immagini e usarlo.

L'app funziona interamente in locale. Nessun dato lascia il computer dell'utente.

## 2. Stato attuale

- **Backend**: pacchetto Python `tagstore` con `model.py` (logica e database), `errors.py` e `web.py` (server FastAPI). Non c'è una CLI: `cli.py` non fa parte del repo.
- **Frontend**: pagina singola in `tagstore/static/` (`index.html`, `app.js`, `style.css`), senza framework né build step. Parla col backend via `/api/...`.
- **Dipendenze**: `fastapi`, `uvicorn`, `send2trash` e `pywebview`. Il build esclude `rich`.
- **Dati**: `.tagstore.json`, `synonyms.txt` e `banned.txt` stanno nella cartella delle immagini. Il launcher salva l'ultima cartella in `%APPDATA%\TagStore\config.json` e il log in `%APPDATA%\TagStore\tagstore.log`.
- **Azioni sul sistema**: l'app rinomina ed elimina file, mostra un file in Esplora risorse (`explorer /select`) e lo apre nell'editor predefinito (`os.startfile`).
- **Server**: `python -m tagstore.web` si lega a `127.0.0.1` sulla porta 8000. L'app installata sceglie una porta libera sullo stesso indirizzo.

## 3. Decisioni prese

1. **Non si fa una webapp HTML pura.** Un browser non può scansionare cartelle, rinominare o eliminare file e aprirli nell'editor di sistema. La File System Access API esiste solo su Chromium, richiede di riconcedere i permessi a ogni sessione e obbligherebbe a riscrivere tutto `model.py` in JavaScript.
2. **Non si fa un'app nativa tipo Krita, né Electron/Tauri.** Richiederebbero di riscrivere il backend senza benefici concreti.
3. **Si mantiene l'architettura attuale** (server locale FastAPI + interfaccia web) e la si impacchetta.
4. **Packaging con PyInstaller in modalità `--onedir`.** Produce una cartella con `TagStore.exe`, Python e le librerie già dentro. Si evita `--onefile`: parte più lento e genera più falsi positivi degli antivirus.
5. **Distribuzione con un installer (setup file) creato con Inno Setup**, a sua volta costruito sopra la cartella prodotta da PyInstaller.
6. **Piattaforma iniziale: Windows.** macOS e Linux richiederebbero una build su ciascun sistema e sono fuori scope per ora.
7. **Ogni utente esegue l'app sul proprio PC.** Il server resta su `127.0.0.1`. Non è previsto un uso in rete locale.
8. **Finestra nativa (variante B).** `pywebview` con Edge WebView2. Chiudere la finestra chiude il processo. Se la finestra non si apre, l'app mostra un messaggio con il percorso del log e termina. Non resta un processo in attesa senza finestra.
9. **Configurazione del launcher in `%APPDATA%\TagStore`.** `config.json` contiene `last_root`. `tagstore.log` è il log. La cartella immagini scelta al primo avvio viene riaperta dopo.
10. **`synonyms.txt` e `banned.txt` restano nella cartella delle immagini**, accanto a `.tagstore.json`. Spostarli in `%APPDATA%` è lavoro successivo.

## 4. Decisioni aperte

- **Firma del codice.** Un certificato elimina l'avviso SmartScreen ma ha un costo. Resta fuori da questa versione.

## 5. Architettura finale

```
TagStore.exe (launcher, senza console)
 ├─ legge la cartella immagini (ultima usata o scelta all'avvio)
 ├─ sceglie una porta libera su 127.0.0.1
 ├─ avvia uvicorn con l'app FastAPI in un thread
 └─ apre la finestra pywebview. Se non si apre, mostra un messaggio e termina
```

Il frontend e il backend restano quelli attuali. Il launcher è l'unico componente nuovo.

## 6. Esperienza dell'utente

1. Scarica `TagStore-Setup-<versione>.exe`.
2. Lo esegue. Se non è firmato, Windows mostra l'avviso SmartScreen: *Maggiori informazioni → Esegui comunque*.
3. L'installer procede con l'installazione per singolo utente, senza richiedere i permessi di amministratore, e crea il collegamento nel menu Start (e, a scelta, sul Desktop).
4. Al primo avvio compare un selettore di cartella: l'utente indica dove stanno le immagini.
5. Si apre l'interfaccia di TagStore e l'utente avvia la scansione dal pulsante già presente.
6. Agli avvii successivi l'app riapre l'ultima cartella.
7. Per chiudere basta chiudere la finestra.
8. Per disinstallare si usa *Impostazioni → App*. I file `.tagstore.json` nelle cartelle delle immagini restano, così i tag non si perdono.

## 7. Modifiche al codice

- **`run_tagstore.py` (nuovo, nella radice del repo)**: punto d'ingresso per PyInstaller. Gestisce selezione della cartella, scelta della porta, avvio del server e della finestra. Sta fuori dal pacchetto per non rompere gli import relativi (`from .model import ...`).
- **Percorso della cartella `static/`**: in `web.py` va risolto con un helper che usa `sys._MEIPASS` quando l'app gira dentro PyInstaller e il percorso normale altrimenti.
- **Logging di uvicorn**: con `--noconsole` `sys.stdout` e `sys.stderr` sono `None` e la configurazione di log predefinita di uvicorn va in errore. Si passa `log_config=None` oppure si reindirizza il log su un file in `%APPDATA%\TagStore\`.
- **Porta**: invece di 8000 fissa, si cerca una porta libera, così l'avvio non fallisce se è occupata.
- **Cartella immagini**: selettore iniziale (`tkinter.filedialog` o il dialogo di `pywebview`), con l'ultima scelta salvata in `%APPDATA%\TagStore\config.json`. L'opzione `--root` resta valida per l'uso da sviluppatore. Cambiare cartella nella versione 1 significa riavviare l'app.
- **Azioni su Windows**: `explorer /select` e `os.startfile` funzionano così come sono. Il ramo non Windows resta com'è finché macOS e Linux sono fuori scope.

## 8. Preparazione del repo

Struttura prevista:

```
tagstore/              pacchetto esistente (con static/)
run_tagstore.py        launcher (nuovo)
requirements.txt       fastapi, uvicorn, send2trash, pywebview
requirements-dev.txt   -r requirements.txt, pyinstaller
packaging/
  tagstore.spec        configurazione PyInstaller
  installer.iss        script Inno Setup
  build.ps1            build + installer in un comando
.gitignore             build/, dist/, .venv/, .tagstore.json
```

Passi, in ordine:

1. Clonare il repo e creare un branch `packaging`.
2. Creare un ambiente virtuale e installare `requirements-dev.txt`.
3. Verificare che l'app parta ancora con `python -m tagstore.web --root <cartella di prova>`.
4. Applicare le modifiche del punto 7 e provare `python run_tagstore.py`.
5. Costruire con PyInstaller (`--onedir`, `--noconsole`, `--name TagStore`, `--add-data` per `tagstore/static`, `--collect-submodules uvicorn` per gli import nascosti, UPX disattivato). Quando funziona, salvare le opzioni nel file `.spec`.
6. Lanciare `dist\TagStore\TagStore.exe` e correggere i problemi tipici: file statici mancanti, import non trovati, errori di log.
7. Scrivere `installer.iss` con installazione per singolo utente (`PrivilegesRequired=lowest`), collegamenti, disinstallatore, versione e icona.
8. Compilare l'installer con Inno Setup e ottenere `TagStore-Setup-<versione>.exe`.
9. Provare l'installer su un Windows pulito (una macchina virtuale o Windows Sandbox), senza Python installato.
10. Pubblicare il setup, per esempio come *Release* su GitHub.

## 9. Rischi

- **Antivirus e SmartScreen**: gli eseguibili creati con PyInstaller possono essere segnalati. Si mitiga con `--onedir`, senza UPX, e segnalando i falsi positivi ai produttori. La firma del codice lo risolve del tutto.
- **WebView2 assente su sistemi vecchi**: Windows 10 e 11 aggiornati lo includono. Se manca, l'app mostra un messaggio e termina.
- **Dimensione**: ci si aspetta qualche decina di MB. Va tenuta d'occhio escludendo `rich` e i moduli inutilizzati.
- **Cartelle con molte immagini**: la scansione ha già avanzamento e annullamento. Va verificata su una cartella grande dentro l'app impacchettata.

## 10. Piano di lavoro

1. **Milestone 1**: launcher funzionante da sorgente (porta libera, selettore cartella, apertura finestra).
2. **Milestone 2**: `TagStore.exe` costruito con PyInstaller e funzionante sulla propria macchina.
3. **Milestone 3**: installer Inno Setup, provato su Windows pulito.
4. **Milestone 4**: pubblicazione della prima release e raccolta di feedback.
5. **Dopo**: build automatica con GitHub Actions su un runner Windows, firma del codice, cambio cartella dall'interfaccia, spostamento dei file di configurazione in `%APPDATA%`.

## 11. Fuori scope

Versioni per macOS e Linux, uso in rete locale con più utenti, aggiornamenti automatici, riscrittura del backend in un altro linguaggio.
