from pyts.approximation import SymbolicFourierApproximation
from pyts.datasets import load_gunpoint

X, _, _, _ = load_gunpoint(return_X_y=True)
transformer = SymbolicFourierApproximation(n_coefs=4)
X_new = transformer.fit_transform(X)