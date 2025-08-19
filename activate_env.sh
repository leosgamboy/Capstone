#!/bin/bash

# Activate the local conda environment
echo "Activating local conda environment with Python 3.12..."
export PATH="/Users/leosgambato/Documents/GitHub/Capstone/.conda/bin:$PATH"
export CONDA_PREFIX="/Users/leosgambato/Documents/GitHub/Capstone/.conda"

echo "Environment activated!"
echo "Python location: $(which python)"
echo "Python version: $(python --version)"
echo ""
echo "Available packages:"
echo "- matplotlib: $(python -c 'import matplotlib; print(matplotlib.__version__)' 2>/dev/null || echo 'Not installed')"
echo "- seaborn: $(python -c 'import seaborn; print(seaborn.__version__)' 2>/dev/null || echo 'Not installed')"
echo "- pandas: $(python -c 'import pandas; print(pandas.__version__)' 2>/dev/null || echo 'Not installed')"
echo "- numpy: $(python -c 'import numpy; print(numpy.__version__)' 2>/dev/null || echo 'Not installed')"
echo "- jupyter: $(python -c 'import notebook; print(notebook.__version__)' 2>/dev/null || echo 'Not installed')"
echo ""
echo "To deactivate, run: conda deactivate"
echo "To run Jupyter with this environment: jupyter notebook"
