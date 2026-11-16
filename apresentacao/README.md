# Guia Canadá — apresentação TABD

Apresentação interativa em português do projeto de Data Warehouse de Eliezir Moreira e Raphael Phillipe, IFAL, TABD 2026.2.

## Apresentar

- `#abertura` → `#perguntas` → `#metodo` → `#consulta-1` a `#consulta-10` → `#conclusoes`.
- **← / →** navegam. Nas consultas, o primeiro avanço revela a resposta.
- **↑ / ↓** percorrem a lista de perguntas. Na metodologia, avance pelas quatro etapas.
- **N** abre as notas do slide; **F** alterna tela cheia onde disponível.
- O seletor na barra inferior permite ir diretamente a qualquer uma das 14 telas.
- O botão de janela do apresentador abre um roteiro separado da projeção. As janelas se sincronizam no mesmo navegador.
- O roteiro também está disponível em `roteiro-apresentador.md` no site publicado.

As rotas de revisão das variantes continuam disponíveis como `#abertura-a`, `#perguntas-a` e `#metodo-a` (também b/c), além das seções do explorador em `#inicio`, `#explorar`, `#comparar` e `#fontes`.

## Executar e verificar

Requer Node 22 ou superior.

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 5186
npm run check
npm test
npm run build
```

O build exporta o roteiro de fala e gera `dist/`. As fontes, a foto da abertura, o mapa, as bandeiras e Recharts estão incluídos localmente. Valores indisponíveis continuam como **Sem dado**. Charts incluem tabelas acessíveis de apoio.

## Fontes e conteúdo

- Statistics Canada, Censo 2021: comunidade, chegada e indicador de moradia conforme o conjunto aprovado.
- Job Bank, NOC 21232: publicação 2025 com referência salarial 2023–2024.
- `src/data.ts` preserva perguntas, respostas, unidades e períodos aprovados.
- `src/presenter-notes.ts` contém os roteiros e as ressalvas metodológicas; veja também `PRESENTER_GUIDE.md`.
- `MAP_ASSETS.md` e `THIRD_PARTY_NOTICES.txt` registram atribuições.

## GitHub Pages

A branch dedicada é `apresentacao`, com fonte em `/apresentacao` e build em `/docs`. Para servir essa versão, a configuração do GitHub Pages deve apontar para `apresentacao /docs`:

https://raphaelphillipe07.github.io/canada-developer-immigration-dw/

O conteúdo anterior foi preservado em `entrega-1.html`. A aplicação usa caminhos relativos para funcionar sob o prefixo do repositório.

`apresentacao/` na branch de publicação guarda a fonte React. A pasta local `.presentation-checkout` é apenas o checkout auxiliar para publicação e não deve ser incorporada à fonte.

