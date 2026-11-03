"""Huấn luyện năm mô hình theo notebook 02, lưu vào saved_models/."""
import json
import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parent
    notebook = root / 'notebooks' / '02_Tien_Xu_Ly_Train_MNIST.ipynb'
    os.chdir(root)
    plt.show = lambda *args, **kwargs: plt.close('all')
    scope = {'__name__': '__main__'}
    for index, cell in enumerate(json.loads(notebook.read_text(encoding='utf-8'))['cells']):
        if cell['cell_type'] == 'code':
            exec(compile(''.join(cell['source']), f'{notebook.name}:cell_{index}', 'exec'), scope)


if __name__ == '__main__':
    main()
