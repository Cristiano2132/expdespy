# expdespy


**expdespy** is a Python package for statistical analysis of experimental designs in Python.

It provides a high-level interface for conducting ANOVA, verifying assumptions, performing post-hoc tests, and creating publication-ready visualizations for agricultural, biological, and industrial experiments.

---

## 🚀 Features

- ✅ Completely Randomized Design (DIC)
- ✅ Randomized Block Design (DBC)
- 🧪 ANOVA with Type II Sum of Squares
- 🔍 Assumption checks: Shapiro-Wilk and Levene tests
- 🔎 Post-hoc tests with Compact Letter Display:
  - Tukey HSD
  - T-test (pairwise, without correction)
- 📊 Visualizations with significance letters (CLD)
- 🔧 Modular architecture for easy extension

---

## 📦 Installation

```bash
git clone https://github.com/Cristiano2132/expdespy.git
cd expdespy
pip install .
```

---

🧪 Quick Example

```python
import pandas as pd
from expdespy.models import DIC
from expdespy.posthoc.tukey import TukeyHSD

# Load your experimental dataset (must be a pandas DataFrame)
df = pd.DataFrame({
    "fertilizer": ["A", "A", "B", "B", "C", "C", "D", "D"],
    "yield": [21, 22, 26, 27, 29, 30, 35, 36]
})

# Fit a DIC model
model = DIC(data=df, response="yield", treatment="fertilizer")

# Perform ANOVA
anova_table = model.anova()
print(anova_table)

# Post-hoc with Tukey HSD
tukey = TukeyHSD(data=df, values_column="yield", trats_column="fertilizer")
cld = tukey.run_compact_letters_display()
print(cld)
```

---

🤝 Contributing

We welcome contributions!

- Fork the repository
- Create your feature branch: git checkout -b feature/your-feature
- Commit your changes: git commit -m "Add your feature"
- Push to the branch: git push origin feature/your-feature
- Open a pull request 🚀


⚠️ **Important**:
Please write tests for any new features and make sure the test suite passes before submitting a pull request.

pytest tests/


---

📝 License

This project is licensed under the MIT License.

---

📫 Contact

Maintained by Cristiano Oliveira – contributions and feedback are very welcome!

---

📌 Versioning

This project follows Semantic Versioning:

MAJOR.MINOR.PATCH

- **MAJOR**: incompatible API changes
- **MINOR**: new features, but backwards compatible
- **PATCH**: backwards compatible bug fixes

Examples:

- **1.0.0**: first stable release
- **1.1.0**: added new functionality without breaking existing APIs
- **1.1.1**: fixed a bug
