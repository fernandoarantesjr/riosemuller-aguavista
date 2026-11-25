# Rios & Muller — AguaVista

Peça de vendas para celular ("PDF animado") da **Rios & Muller**, usada para
apresentar casas e lotes no condomínio **AguaVista**, em San Juan del Paraná,
Itapúa, Paraguai. É mandada por link de WhatsApp para clientes interessados.

Não é o site do condomínio: a marca, a voz e o contato são da Rios & Muller.
O AguaVista é o produto.

## Como é feito

Um arquivo só, `index.html`, com o CSS e o JavaScript embutidos. Sem build,
sem dependência, sem framework — abre direto no navegador. A página é
publicada como Artifact e precisa funcionar sob uma CSP que não aceita
imagem, iframe nem fonte de fora, por isso tudo vai junto no repositório.

Bilíngue por atributo: o português está no DOM e o espanhol vive em `data-es`.
A função `setLang()` troca os dois.

## Pastas

| pasta | o que é |
|---|---|
| `img/` | o que a página publica: capas, galerias, pôsteres |
| `video/` | abertura com o vídeo do corretor e o filme do aeroporto |
| `_webp/` | acervo de trabalho, otimizado — a origem das fotos de `img/` |
| `_originais/` | arquivos como vieram, antes de qualquer conversão |

## Ver localmente

```
python3 serve.py
```

Abre em `http://127.0.0.1:8765`. O `serve.py` embrulha o `index.html` no
mesmo esqueleto que o Artifact injeta (charset, viewport e reset), para o
preview local se parecer com o publicado. Sem isso a página renderiza larga
e com acento quebrado.

Vale olhar no celular, ou com o navegador em 375×812: o recuo do vídeo de
abertura e o parallax não aparecem no desktop.
