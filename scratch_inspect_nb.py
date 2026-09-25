import nbformat

with open('ab_testing_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

for i, cell in enumerate(nb.cells):
    print(f"Cell {i} ({cell.cell_type}):")
    print(cell.source[:100] + "...")
    print("-" * 40)
