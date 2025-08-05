# System Info Reader

Um script Python que coleta informações do sistema (somente leitura) e pode integrar com a API do Claude para análise.

## 🚀 Funcionalidades

- **Coleta segura** de informações do sistema (Windows/Linux/macOS)
- **Informações de hardware** (CPU, RAM, disco)
- **Lista de programas instalados**
- **Processos em execução**
- **Integração com Claude API** para análise inteligente
- **Export para JSON**

## 📋 Pré-requisitos

```bash
pip install psutil requests
```

## 🔧 Como usar

1. **Execute o script:**
```bash
python system_info_reader.py
```

2. **Escolha uma opção:**
   - `1` - Salvar informações em arquivo JSON
   - `2` - Enviar para Claude (requer API key)
   - `3` - Mostrar resumo do sistema
   - `4` - Sair

## 🔐 Segurança

- ✅ **Somente leitura** - não modifica nenhuma configuração
- ✅ **Sem dados sensíveis** - não coleta senhas ou IPs específicos
- ✅ **Código aberto** - você pode revisar todo o código

## 🌐 Sistemas Suportados

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, CentOS, etc.)
- ✅ macOS

## 📊 Informações Coletadas

### Sistema
- Sistema operacional e versão
- Arquitetura (32/64 bits)
- Hostname
- Tempo de atividade

### Hardware
- Informações da CPU
- Memória RAM (total/disponível)
- Uso de disco por partição

### Software
- Programas instalados (via registry/package managers)
- Processos em execução (top 20)

### Rede
- Interfaces de rede (sem IPs específicos)

## 🤖 Integração com Claude

Para usar a integração com Claude:

1. Obtenha uma API key em: https://console.anthropic.com
2. Execute o script e escolha a opção `2`
3. Cole sua API key quando solicitado
4. Faça perguntas sobre seu sistema!

## 📄 Exemplo de Uso

```python
from system_info_reader import SystemInfoReader

reader = SystemInfoReader()
info = reader.collect_all_info()
reader.save_to_file("meu_sistema.json")
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ⚠️ Disclaimer

Este script coleta apenas informações básicas do sistema para fins de análise e otimização. Nenhuma informação sensível é coletada ou transmitida.

---

**Feito com ❤️ para análise de sistemas**
