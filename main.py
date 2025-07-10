import pandas as pd
import numpy as np
from itertools import product
from expdespy.models import FatorialDIC

# Simulando fatores com 2 níveis cada e 3 repetições
levels = [0, 1]
replicates = 3

combinations = list(product(levels, levels, levels))
data = []
np.random.seed(42)

for a, b, c in combinations:
    for _ in range(replicates):
        # Cria uma resposta com efeito aditivo e alguma interação
        y = (
            10 * a + 5 * b + 3 * c + 
            4 * a * b - 2 * b * c + 
            np.random.normal(0, 2)
        )
        data.append([a, b, c, y])

df = pd.DataFrame(data, columns=["A", "B", "C", "Y"])


model = FatorialDIC(data=df, response="Y", factors=["A", "B", "C"])
result = model.unfold_interactions(alpha=0.05, posthoc="tukey", print_results=False, max_interaction=3)
model.display_unfolded_interactions(result)