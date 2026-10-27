import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ==============================================================================
# Configurações do Servidor Ollama Local (Windows)
# ==============================================================================
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "nomic-embed-text"
TEXTO_EXEMPLO = (
    "A inteligência artificial generativa e os vetores de embeddings "
    "transformam textos em representações numéricas de alta dimensão."
)


def verificar_status_ollama(host: str) -> str:
    """
    Verifica se o serviço do Ollama está rodando localmente no Windows
    consultando a rota raiz (GET http://localhost:11434).
    """
    with urlopen(host, timeout=5) as response:
        return response.read().decode("utf-8").strip()


def gerar_embeddings_local(host: str, modelo: str, texto: str) -> list[float]:
    """
    Envia uma requisição HTTP POST diretamente para a API local do Ollama (/api/embed)
    usando apenas a biblioteca padrão do Python (sem pacotes externos).
    """
    url = f"{host}/api/embed"
    payload = json.dumps({"model": modelo, "input": texto}).encode("utf-8")
    requisicao = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(requisicao, timeout=30) as response:
        dados = json.loads(response.read().decode("utf-8"))

        # Suporte ao formato /api/embed ("embeddings") ou /api/embeddings ("embedding")
        if "embeddings" in dados and len(dados["embeddings"]) > 0:
            return dados["embeddings"][0]
        if "embedding" in dados:
            return dados["embedding"]

        raise ValueError(f"Formato inesperado na resposta do Ollama: {dados}")


def exibir_resumo_vetor(texto: str, modelo: str, vetor: list[float]) -> None:
    """Exibe no console o tamanho do vetor e uma amostra dos valores gerados."""
    norma_l2 = sum(x * x for x in vetor) ** 0.5
    valor_min = min(vetor)
    valor_max = max(vetor)

    print("=" * 70)
    print("GERAÇÃO DE EMBEDDINGS COM OLLAMA LOCAL (WINDOWS)")
    print("=" * 70)
    print(f"Endpoint Local   : {OLLAMA_HOST}/api/embed")
    print(f"Modelo utilizado : {modelo}")
    print(f"Texto de entrada : \"{texto}\"")
    print("-" * 70)
    print(f"Tamanho do vetor (dimensões) : {len(vetor)}")
    print(f"Norma L2 do vetor            : {norma_l2:.4f}")
    print(f"Intervalo de valores         : [{valor_min:.6f}, {valor_max:.6f}]")
    print("-" * 70)
    print("Primeiros 10 valores do vetor de embeddings:")
    for indice, valor in enumerate(vetor[:10]):
        print(f"  [{indice:02d}] {valor:+.6f}")
    print("-" * 70)
    print(f"Amostra resumida (5 primeiros): {[round(v, 5) for v in vetor[:5]]}")
    print("=" * 70)


def main() -> None:
    print(f"Verificando serviço do Ollama em {OLLAMA_HOST}...")

    try:
        status = verificar_status_ollama(OLLAMA_HOST)
        print(f"Status do servidor local: '{status}'\n")

        vetor = gerar_embeddings_local(OLLAMA_HOST, MODEL_NAME, TEXTO_EXEMPLO)
        exibir_resumo_vetor(TEXTO_EXEMPLO, MODEL_NAME, vetor)

    except HTTPError as erro_http:
        detalhe = erro_http.read().decode("utf-8", errors="ignore")
        print(f"\n[ERRO HTTP {erro_http.code}] O Ollama retornou um erro: {detalhe}", file=sys.stderr)
        print(f"Certifique-se de que você baixou o modelo no Prompt de Comando / PowerShell:", file=sys.stderr)
        print(f"  ollama pull {MODEL_NAME}", file=sys.stderr)
        sys.exit(1)
    except (URLError, ConnectionError) as erro_conexao:
        print("\n[ERRO DE CONEXÃO] Não foi possível conectar ao Ollama local na porta 11434.", file=sys.stderr)
        print("No Windows, verifique se o aplicativo do Ollama está aberto na bandeja do sistema", file=sys.stderr)
        print("ou execute no PowerShell / Prompt de Comando:", file=sys.stderr)
        print("  ollama serve", file=sys.stderr)
        print(f"Detalhes técnicos: {erro_conexao}", file=sys.stderr)
        sys.exit(1)
    except Exception as erro:
        print(f"\n[ERRO] Falha inesperada: {erro}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()