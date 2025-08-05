# System Info Reader

Coletor de Informações do Sistema (versão multiplataforma)  
Este aplicativo coleta informações detalhadas do seu sistema para análise ou envio para a API Claude.

---

## Como Usar

### **Opção recomendada: Download do Executável**

Você não precisa instalar Python nem nenhuma dependência!

1. **Baixe o arquivo [`system_info_reader.exe`](https://github.com/Leotech47/system_info_reader/releases) na seção de Releases do GitHub.**
2. Dê um duplo clique em `system_info_reader.exe`.
3. Siga as instruções no terminal:
    - Salvar informações em arquivo JSON
    - Enviar para a API Claude (requer API Key)
    - Mostrar resumo do sistema

<details>
<summary>Como funciona?</summary>

O aplicativo coleta dados como:
- Sistema operacional, arquitetura, hostname
- Informações de hardware (CPU, RAM, discos)
- Programas instalados (Windows, Linux, macOS)
- Interfaces de rede (sem dados sensíveis)
- Processos em execução (nomes e uso de CPU)

Você pode salvar um relatório (arquivo JSON), visualizar um resumo ou enviar para a API Claude para análise.
</details>

---

### **Opção alternativa: Rodar o script Python**

Se preferir rodar o script manualmente ou em outro sistema operacional:

#### 1. Clone o repositório:
```sh
git clone https://github.com/Leotech47/system_info_reader.git
cd system_info_reader
```

#### 2. Instale as dependências:
```sh
pip install -r requirements.txt
```

#### 3. Execute:
```sh
python system_info_reader.py
```

---

## Recursos

- Funciona em Windows, Linux e macOS.
- Não requer permissões administrativas.
- Não coleta nem envia dados sensíveis sem sua permissão.
- Compatível com envio para a API Claude (Anthropic).

---

## Gerando o executável (avançado)

O executável `.exe` é gerado automaticamente pelo GitHub Actions a cada nova release.  
Se quiser gerar manualmente:

1. Instale Python 3.11+ e as dependências.
2. Instale o PyInstaller:
   ```sh
   pip install pyinstaller
   ```
3. Gere o executável:
   ```sh
   pyinstaller --onefile system_info_reader.py
   ```
4. O arquivo estará em `dist/system_info_reader.exe`.

---

## Licença

MIT License

---

**Dúvidas ou sugestões?**  
Abra uma [issue](https://github.com/Leotech47/system_info_reader/issues) no GitHub!
