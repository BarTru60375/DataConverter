# Konwerter danych (JSON / YAML / XML)

Projekt koncowy z przedmiotu **Narzedzia w branzy IT (Lab 5 i 6)**.

Program konwertuje dane miedzy formatami **.json**, **.yml/.yaml** oraz **.xml**.
Format rozpoznawany jest na podstawie rozszerzenia pliku.

## Sposob uzycia (wersja konsolowa)

```
converter.exe pathFile1.x pathFile2.y
```

gdzie `x` oraz `y` to jeden z formatow: `json`, `yml`, `yaml`, `xml`.

Przyklad:

```
python converter.py sample.json out.yml
python converter.py out.yml out.xml
python converter.py out.xml out.json
```

Program wczytuje dane z pliku zrodlowego, a nastepnie tworzy nowy plik
docelowy z danymi w wybranym formacie. W razie bledu (brak pliku,
nieobslugiwany format, niepoprawna skladnia) wypisuje czytelny komunikat
i zwraca kod wyjscia rozny od zera.

## Wersja z interfejsem graficznym (PyQt5)

```
python gui.py
```

Wersja GUI wykonuje wczytywanie i zapis pliku **asynchronicznie**
(w osobnym watku `QThread`), dzieki czemu interfejs nie zawiesza sie
podczas konwersji.

## Instalacja zaleznosci

```
./installResources.ps1
```

lub

```
pip install -r requirements.txt
```

## Budowanie pliku .exe

```
pyinstaller --onefile converter.py            # wersja konsolowa
pyinstaller --onefile --noconsole gui.py      # wersja z GUI (bez okna konsoli)
```

Plik wynikowy znajdziesz w katalogu `dist/`.

## Automatyczne budowanie (GitHub Actions)

Workflow `.github/workflows/build.yml` buduje plik `.exe` na serwerze
`windows-latest` i przesyla go jako artefakt (`actions/upload-artifact@v3`).
Uruchamia sie: raz w tygodniu (harmonogram), po pushu na `master` oraz
recznie (`workflow_dispatch`).

## Struktura gałęzi (Git)

| Galaz   | Zawartosc                                                    |
|---------|-------------------------------------------------------------|
| Task0   | skrypt `installResources.ps1`, `requirements.txt`           |
| Task1   | parsowanie argumentow wywolania                             |
| Task2   | wczytywanie z `.json` + weryfikacja skladni                 |
| Task3   | zapis do `.json`                                            |
| Task4   | wczytywanie z `.yml/.yaml` + weryfikacja skladni            |
| Task5   | zapis do `.yml/.yaml`                                        |
| Task6   | wczytywanie z `.xml` + weryfikacja skladni                  |
| Task7   | zapis do `.xml`                                             |
| Task8   | wersja z interfejsem graficznym (PyQt5)                     |
| Task9   | GUI: wczytywanie/zapis asynchronicznie (wielowatkowo)       |
