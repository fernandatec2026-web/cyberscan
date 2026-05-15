import os
from openai import OpenAI

def generate_ai_summary(secrets_results, deps_results):
    """Utiliza IA para gerar uma análise executiva e dicas de remediação."""
    # Verifica se a chave da API está configurada no ambiente
    if not os.environ.get("OPENAI_API_KEY"):
        return "Análise de IA indisponível: Configure a variável de ambiente OPENAI_API_KEY."

    try:
        client = OpenAI()
        
        # Prepara os dados encontrados para enviar como contexto simplificado para a IA
        contexto = {
            "segredos_vazados": [item["type"] for files in secrets_results.values() for item in files],
            "dependencias_vulneraveis": [f"{item['package']} ({item['cve']})" for item in deps_results]
        }
        
        prompt = f"""
        Como um especialista sênior em Application Security (AppSec), faça um resumo executivo curto e direto em português (máximo 4 linhas) sobre os seguintes riscos encontrados em um scan de código:
        {contexto}
        
        Diga qual o impacto principal e a ação imediata que o desenvolvedor deve tomar.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.2
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Falha ao gerar resumo via IA: {str(e)}"
