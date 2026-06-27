#!/usr/bin/env python3
"""
Konwerter danych pomiedzy formatami JSON, YAML i XML.

Uzycie:
    program.exe pathFile1.x pathFile2.y
gdzie x oraz y to jeden z formatow: json, yml, yaml, xml.

Program rozpoznaje format na podstawie rozszerzenia pliku, wczytuje
dane z pliku zrodlowego, a nastepnie zapisuje je do nowego pliku
docelowego w wybranym formacie.
"""
import sys
import os
import json
import argparse

import xml.etree.ElementTree as ET
from xml.dom import minidom

try:
    import yaml
except ImportError:
    yaml = None


SUPPORTED = {"json", "yml", "yaml", "xml"}
ROOT_TAG = "root"

# Rejestry funkcji wczytujacych i zapisujacych - uzupelniane w kolejnych taskach.
READERS = {}
WRITERS = {}


# Task2: wczytywanie z pliku .json i weryfikacja poprawnosci skladni
def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError("Niepoprawna skladnia JSON w pliku '%s': %s" % (path, e))


READERS["json"] = read_json

# Task3: zapis danych z obiektu do pliku w formacie .json
def write_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


WRITERS["json"] = write_json






def detect_format(path):
    """Rozpoznaje format pliku na podstawie rozszerzenia."""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext not in SUPPORTED:
        raise ValueError(
            "Nieobslugiwany format pliku: '%s'. Dozwolone: json, yml, yaml, xml." % path
        )
    return ext


def convert(source, destination):
    """Wczytuje dane z pliku zrodlowego i zapisuje je w formacie docelowym."""
    if not os.path.isfile(source):
        raise FileNotFoundError("Plik zrodlowy nie istnieje: '%s'" % source)

    src_fmt = detect_format(source)
    dst_fmt = detect_format(destination)

    if src_fmt not in READERS:
        raise RuntimeError("Odczyt formatu '%s' nie jest jeszcze obslugiwany." % src_fmt)
    if dst_fmt not in WRITERS:
        raise RuntimeError("Zapis formatu '%s' nie jest jeszcze obslugiwany." % dst_fmt)

    data = READERS[src_fmt](source)
    WRITERS[dst_fmt](data, destination)
    return src_fmt, dst_fmt


def parse_args(argv=None):
    """Task1: parsowanie argumentow wywolania programu."""
    parser = argparse.ArgumentParser(
        description="Konwerter danych JSON <-> YAML <-> XML."
    )
    parser.add_argument("source", help="plik zrodlowy (.json, .yml, .yaml, .xml)")
    parser.add_argument("destination", help="plik docelowy (.json, .yml, .yaml, .xml)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        src_fmt, dst_fmt = convert(args.source, args.destination)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print("Blad: %s" % e, file=sys.stderr)
        return 1
    except Exception as e:  # zabezpieczenie przed nieoczekiwanymi bledami
        print("Nieoczekiwany blad: %s" % e, file=sys.stderr)
        return 2
    print("OK: '%s' (%s) -> '%s' (%s)" % (args.source, src_fmt, args.destination, dst_fmt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
