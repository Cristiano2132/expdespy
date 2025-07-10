**expdespy** é um pacote Python para análise estatística de delineamentos experimentais.

## 📦 Funcionalidades

- Delineamento Inteiramente Casualizado (DIC)
- Delineamento em Blocos Casualizados (DBC)
- Parcelas Subdivididas
- ANOVA
- Verificações de pressupostos (normalidade, homogeneidade)
- Testes pós-hoc: Tukey, Duncan, Scott-Knott
- Visualizações com letras de significância

## 📥 Instalação

Você pode instalar o pacote localmente com:

```bash
pip install .
```

## 🚀 Exemplo de Uso

```python
from expdespy.models import DIC

# Exemplo de uso
dic = DIC(data=df, response="yield", treatment="fertilizer")
dic.anova()
dic.tukey()
dic.plot_means()
```

## 👨‍💻 Para Desenvolvedores

### 🧪 Executando os Testes com Docker

Este repositório já inclui o script `test.sh` para facilitar a execução dos testes automatizados com Docker. Para rodar:

```bash
bash test.sh
```

Esse script realiza:

1. A construção da imagem Docker (`expdespy-tests`)
2. A execução dos testes automatizados dentro do contêiner
3. A verificação da cobertura de testes (mínimo exigido: 90%)

Se algum teste falhar ou a cobertura for menor que 90%, o script será interrompido com erro.

### 🐳 Execução Manual com Docker (Opcional)

Se preferir rodar os testes manualmente:

```bash
# Construir a imagem Docker
docker build -t expdespy-tests .

# Executar os testes
docker run --rm expdespy-tests
```

Ou acessar o ambiente interativo:

```bash
docker run -it --rm -v $(pwd):/app expdespy-tests bash
```

Dentro do contêiner, execute:

```bash
pytest --cov=src
```

---

## 📄 Licença

MIT

---

Se quiser, posso adaptar isso também para incluir instruções sobre como contribuir ou configurar um ambiente local com `venv`. Deseja isso?
"""

path = "/mnt/data/README.md"
with open(path, "w", encoding="utf-8") as f:
    f.write(readme_content)

path