import os

def generate_html_report(secrets_results, deps_results, ai_summary):
    """Gera um painel executivo consolidado em HTML contendo análise de IA."""
    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", "security_report.html")
    
    secrets_rows = ""
    for filepath, findings in secrets_results.items():
        for item in findings:
            secrets_rows += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #ddd; font-family: monospace;">{filepath}</td>
                <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;"><span style="background: #ffcccc; color: #cc0000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">CRÍTICO</span></td>
                <td style="padding: 12px; border-bottom: 1px solid #ddd;">Vazamento de {item['type']}</td>
                <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{item['line']}</td>
            </tr>
            """

    deps_rows = ""
    for item in deps_results:
        deps_rows += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; font-family: monospace;">{item['package']} (v{item['version']})</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;"><span style="background: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{item['severity']}</span></td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;"><strong>{item['cve']}</strong> - {item['description']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{item['line']}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>CyberScan AI - Dashboard de Segurança</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px;">
        <div style="max-width: 1100px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50; margin: 0;">CyberScan AI</h1>
            <p style="color: #7f8c8d;">Painel Consolidado de Riscos de Código e Cadeia de Suprimentos (SAST & SCA)</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            
            <!-- Caixa de Inteligência Artificial -->
            <div style="background: #efe6f7; border-left: 4px solid #8e44ad; padding: 18px; margin-bottom: 30px; border-radius: 4px;">
                <strong style="color: #8e44ad; font-size: 16px;">🤖 Resumo Executivo CyberScan AI:</strong>
                <p style="margin: 8px 0 0 0; color: #2c3e50; line-height: 1.5; font-style: italic;">{ai_summary}</p>
            </div>

            <h2 style="color: #c0392b;">1. Segredos e Credenciais Expostas</h2>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 40px;">
                <thead>
                    <tr style="background-color: #2c3e50; color: white; text-align: left;">
                        <th style="padding: 12px;">Arquivo</th>
                        <th style="padding: 12px; text-align: center;">Severidade</th>
                        <th style="padding: 12px;">Descrição</th>
                        <th style="padding: 12px; text-align: center;">Linha</th>
                    </tr>
                </thead>
                <tbody>
                    {secrets_rows if secrets_rows else '<tr><td colspan="4" style="padding: 20px; text-align: center; color: green;">Nenhum segredo exposto.</td></tr>'}
                </tbody>
            </table>

            <h2 style="color: #d35400;">2. Vulnerabilidades em Dependências (SCA)</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #2c3e50; color: white; text-align: left;">
                        <th style="padding: 12px;">Componente</th>
                        <th style="padding: 12px; text-align: center;">Severidade</th>
                        <th style="padding: 12px;">Análise Técnica</th>
                        <th style="padding: 12px; text-align: center;">Linha</th>
                    </tr>
                </thead>
                <tbody>
                    {deps_rows if deps_rows else '<tr><td colspan="4" style="padding: 20px; text-align: center; color: green;">Todas as bibliotecas estão seguras e atualizadas.</td></tr>'}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[+] Painel executivo atualizado com IA em: {report_path}")
