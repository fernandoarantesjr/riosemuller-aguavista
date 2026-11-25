"""Servidor estático para pré-visualizar o site localmente.

Duas correções em cima do `python3 -m http.server`, que não serve aqui:

1. O __main__ dele chama os.getcwd() ao montar o argparse e quebra neste
   ambiente. Aqui a pasta é fixa e getcwd nunca é tocado.
2. Ele é single-thread: ao transmitir os dois vídeos, as imagens ficam na
   fila e parecem quebradas. Por isso ThreadingHTTPServer.

E o index.html é servido embrulhado no esqueleto que o Artifact injeta
(doctype, charset, viewport e o reset) — sem isso o preview renderiza a
1020 px, com acento quebrado, e não se parece com o publicado.
"""
import functools
import http.server
import io
import os

DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8765

TOPO = (
    '<!doctype html>\n<html lang="pt-BR">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<style>\n'
    ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);'
    'padding-bottom:env(safe-area-inset-bottom,0px)}\n'
    'body{margin:0;font:14px system-ui,-apple-system,sans-serif}\n'
    'img{max-width:100%}\n'
    '[hidden]{display:none!important}\n'
    '</style>\n</head>\n<body>\n'
)
RODAPE = "\n</body>\n</html>\n"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        if self.path.split("?")[0] in ("/", "/index.html"):
            corpo = io.open(os.path.join(DIR, "index.html"),
                            encoding="utf-8", newline="").read()
            dados = (TOPO + corpo + RODAPE).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            self.end_headers()
            return io.BytesIO(dados)
        return super().send_head()


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=DIR)
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print("servindo %s em http://127.0.0.1:%d" % (DIR, PORT), flush=True)
        httpd.serve_forever()
