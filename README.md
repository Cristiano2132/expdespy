**expdespy** é um pacote Python para análise estatística de delineamentos experimentais.

## 📦 Funcionalidades

- Delineamento Inteiramente Casualizado (DIC)
- Delineamento em Blocos Casualizados (DBC)
- Plots Subdivididas
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
## Exemplo de uso

Veja os exemplos completos no [notebook de demonstração](https://github.com/Cristiano2132/expdespy/blob/main/examples/expdespy_example.ipynb)

```python
from expdespy import DIC
import pandas as pd

# Exemplo com dados simulados
dados = pd.DataFrame({
    'trat': ['A', 'B', 'C', 'D'] * 5,
    'resp': [20, 22, 25, 21, 19, 23, 24, 22, 20, 21, 25, 26, 27, 24, 23, 19, 20, 21, 22, 24]
})

modelo = DIC(tratamentos=dados['trat'], resposta=dados['resp'], qualitativo=True)
modelo.anova()
modelo.teste_posthoc(metodo='tukey', alfa=0.05)
modelo.plot()
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
## O pacote se encontra atualmente no [TestPyPI ](https://test.pypi.org/project/expdespy/)


## 📄 Licença

MIT
