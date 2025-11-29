# Benchmark

> LETHOOR Lina & CARON Sebastian

## Installation

Si `UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown` alors :
```bash
pip install PyQt5
```

## Générer le PDF

```bash
pandoc ./pandoc/metadata.yaml rapport.md -o rapport.pdf --pdf-engine=xelatex
```