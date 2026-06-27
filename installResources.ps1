# installResources.ps1
# Skrypt instalujacy komponenty Pythona potrzebne do zbudowania i uruchomienia projektu.
# Przy KAZDEJ nowej instalacji przez pip dopisuj tutaj te sama komende.
# Skrypt jest uruchamiany lokalnie oraz w GitHub Actions (etap konfiguracji srodowiska).

Write-Host "== Aktualizacja pip ==" -ForegroundColor Cyan
python -m pip install --upgrade pip

Write-Host "== Instalacja zaleznosci projektu ==" -ForegroundColor Cyan
python -m pip install pyyaml          # obsluga formatu YAML (.yml / .yaml)
python -m pip install pyqt5           # interfejs graficzny (Task8 / Task9)
python -m pip install pyinstaller     # generowanie pliku .exe

Write-Host "== Gotowe ==" -ForegroundColor Green
