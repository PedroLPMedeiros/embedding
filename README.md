Geração de Vetores de Embeddings com Ollama Local no Windows (Python Nativo)

Este repositório apresenta um script em Python que se conecta diretamente ao servidor local do Ollama no Windows (http://localhost:11434/api/embed) para gerar e inspecionar vetores de embeddings a partir de um texto simples.

Pré-requisitos do Ambiente

Para reproduzir este projeto localmente no Windows, você precisará apenas de:

Sistema Operacional: Windows 10 ou Windows 11.
Ollama para Windows: instalado e em execução localmente na porta padrão (11434).
Python: versão 3.9 ou superior instalada no Windows (utiliza apenas bibliotecas nativas: urllib, json e sys).
Modelo Aberto de Embeddings: nomic-embed-text (gera vetores de 768 dimensões).

Passo 1: Instalação e Execução do Ollama no WindowsBaixe e instale o Ollama para Windows:Acesse a página oficial ollama.com/download/windows, baixe o instalador OllamaSetup.exe e conclua a instalação.Verifique se o serviço do Ollama está ativo:Após instalar, o ícone do Ollama ficará ativo na bandeja do sistema (próximo ao relógio do Windows).Abra o PowerShell ou Prompt de Comando (CMD) e execute os comandos abaixo para confirmar a versão e verificar se o serviço responde localmente:ollama --version
curl http://localhost:11434

(A saída esperada do comando curl é: Ollama is running — caso o serviço esteja fechado, basta rodar ollama serve no terminal).Baixe o modelo de embeddings nomic-embed-text:No PowerShell ou CMD, execute:ollama pull nomic-embed-text
Confirme que o modelo foi baixado listando os modelos locais:ollama list
Passo 2: Como Executar o Script Python no WindowsComo o script gerar_embeddings.py se comunica diretamente com a API HTTP local do Ollama (http://localhost:11434/api/embed) usando a biblioteca padrão do Python (urllib.request), não é necessário instalar nenhuma dependência externa com pip.Clone este repositório no seu computador:git clone https://github.com/SEU-USUARIO/ollama-embeddings-python.git

cd ollama-embeddings-python

Execute o script diretamente pelo PowerShell ou CMD:python gerar_embeddings.py
Saída Esperada no ConsoleVerificando serviço do Ollama em http://localhost:11434...
Status do servidor local: 'Ollama is running'

======================================================================
GERAÇÃO DE EMBEDDINGS COM OLLAMA LOCAL (WINDOWS)
======================================================================
Endpoint Local   : http://localhost:11434/api/embed
Modelo utilizado : nomic-embed-text
Texto de entrada : "A inteligência artificial generativa e os vetores de embeddings transformam textos em representações numéricas de alta dimensão."
----------------------------------------------------------------------
Tamanho do vetor (dimensões) : 768
Norma L2 do vetor            : 1.0000
Intervalo de valores         : [-0.142857, 0.168421]
----------------------------------------------------------------------
Primeiros 10 valores do vetor de embeddings:
  [00] +0.018421
  [01] +0.042105
  [02] -0.061234
  [03] -0.019876
  [04] +0.035112
  [05] -0.008421
  [06] +0.027654
  [07] +0.014982
  [08] -0.031098
  [09] +0.005432
----------------------------------------------------------------------
Amostra resumida (5 primeiros): [0.01842, 0.04211, -0.06123, -0.01988, 0.03511]
======================================================================
Estrutura do RepositórioArquivoDescriçãogerar_embeddings.pyScript em Python nativo que verifica o status do Ollama local (http://localhost:11434), requisita os embeddings na rota /api/embed e imprime a dimensão e os valores iniciais do vetor.README.mdGuia passo a passo para instalar o Ollama no Windows, baixar o modelo nomic-embed-text e reproduzir o teste.