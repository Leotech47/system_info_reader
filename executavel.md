Eu não consigo gerar ou fazer upload direto de arquivos executáveis (.exe) aqui, mas posso te orientar com exatidão sobre como gerar o executável e publicar no seu GitHub. Você fará isso em poucos comandos no seu Windows.

Veja o passo a passo detalhado:

---

## Como gerar o executável do seu script Python

### 1. Instale Python e dependências

- Baixe o Python em https://python.org e instale (marque "Add Python to PATH").
- Abra o Prompt de Comando (cmd) na pasta do seu projeto.
- Execute:
  ```sh
  pip install psutil requests pyinstaller
  ```

### 2. Gere o executável

No Prompt de Comando, execute:
```sh
pyinstaller --onefile system_info_reader.py
```
- Isso criará o executável em dist/system_info_reader.exe

### 3. Teste o executável

- Vá para a pasta dist:
  ```sh
  cd dist
  ```
- Rode o programa:
  ```sh
  system_info_reader.exe
  ```
- Ele deve funcionar igual ao script Python, sem precisar de Python instalado.

### 4. Publique no GitHub

- Faça upload do arquivo dist/system_info_reader.exe na seção de Releases do seu repositório:
  1. No GitHub, acesse seu repositório.
  2. Vá em "Releases" > "Draft a new release".
  3. Faça upload do .exe em "Attach binaries by dropping them here or selecting them".
  4. Publique a release.

---

## DICA: README para Usuários

Adicione ao seu README:

````markdown name=README.md
## Download e Uso

Baixe o arquivo `system_info_reader.exe` na seção [Releases](https://github.com/Leotech47/system_info_reader/releases).

Dê um duplo clique no arquivo para rodar o coletor de informações do sistema.

_Não é necessário instalar Python ou nenhum outro programa!_
````

---

