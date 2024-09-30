```markdown
# Documentação: ProgWeb - Revisão Tópico 3 - YouTube

## Visão Geral
Este documento documenta a transcrição do vídeo "ProgWeb - Revisão Tópico 3", disponível no YouTube. O foco principal deste tópico é a linguagem de marcação, com ênfase em HTML, sua estrutura, semântica e importância no desenvolvimento web.

## Conteúdo da Transcrição

### Introdução à Linguagem de Marcação
- **Linguagem de Marcação**: Uma linguagem que combina texto com informações adicionais, utilizando tags para delimitar componentes em um documento, permitindo a estruturação e apresentação dos dados de forma lógica e compreensível.
- **Exemplos**: SGML (Standard Generalized Markup Language), HTML (HyperText Markup Language), XML (eXtensible Markup Language).

### HTML
- **Definição**: HTML (HyperText Markup Language) é uma linguagem de marcação utilizada para criar documentos que apresentam links para outros documentos. É fundamental para a construção da estrutura de páginas web.
- **Estilização**: HTML não deve ser utilizado para estilização; a estilização deve ser feita com CSS (Cascading Style Sheets), permitindo a separação entre conteúdo e apresentação.

### Separação de Conteúdo e Apresentação
- **Conteúdo (HTML)**: Define a estrutura e o conteúdo do documento, atuando como a espinha dorsal da página.
- **Apresentação (CSS)**: Responsável por definir o layout e o estilo, permitindo designers interferirem na aparência sem modificar o conteúdo.

### História do HTML
- **Introdução**: HTML foi introduzido em 1991 como uma forma simples de estruturar documentos web.
- **Expansão**: Entre 1993 e 1997, o HTML foi expandido com o surgimento de novas funcionalidades e suporte a multimedia.
- **Versões**: HTML 4.01 ainda é amplamente utilizado, mas novos projetos devem adotar HTML5, que introduz novas características essenciais para a web moderna.

### Server-Side vs Client-Side
- **Server-Side**: Inclui linguagens de programação como PHP (Hypertext Preprocessor), ASP (Active Server Pages) e Java, que rodam no servidor e geram HTML dinâmico.
- **Client-Side**: Refere-se ao código que é executado no navegador do usuário, como HTML, CSS e JavaScript. Neste contexto, os navegadores interpretam e apresentam o conteúdo ao usuário.
- **Funcionamento**: O servidor responde a requisições do cliente, retornando documentos HTML devidamente formatados.

### Estrutura do HTML
- **Elementos HTML**: Cada elemento é delimitado por uma tag de abertura (por exemplo, `<p>`) e uma tag de fechamento (por exemplo, `</p>`). É importante a compreensão da estrutura do HTML e sua função, que é mais relevante do que saber todos os detalhes práticos.

### Elementos em Desuso
- **Tags Antigas**: Tags de estilização como `<b>` (bold) e `<i>` (italic) foram substituídas por elementos semânticos mais apropriados, como `<strong>` (importante) e `<em>` (ênfase).

### Definição de Tipo de Documento (DTD)
- **HTML 4.01**: A especificação fornece três tipos de DTD: strict (estrito), transitional (transicional) e frameset (para uso com frames).
- **HTML5**: Introduz apenas um DTD simples: `<!DOCTYPE html>`, simplificando a declaração do tipo de documento.

### Importância da Semântica no HTML
- **Uso de Elementos Corretos**: Usar elementos semânticos, como listas (`<ul>`, `<ol>`), cabeçalhos (`<h1>` - `<h6>`) e rodapés (`<footer>`), é crucial para atribuir significado ao conteúdo.
- **Acessibilidade**: O HTML semântico melhora a acessibilidade e a compreensão da estrutura da página tanto para usuários quanto para máquinas, facilitando a navegação e leitura.
- **SEO (Otimização para Motores de Busca)**: O uso adequado da semântica beneficia a otimização para motores de busca, ajudando a classificar melhor o site em resultados de busca.

### Design Sem Tabelas
- **Uso de Tabelas**: Tabelas devem ser utilizadas unicamente para conteúdo tabular, não para layout visual, que deve ser gerido por CSS.
- **Alternativas**: Utilize `<div>` e outros elementos semânticos para efetuar layouts responsivos e mais facilmente ajustáveis.

### Elementos Semânticos Introduzidos no HTML5
- **Novos Elementos**: A versão HTML5 introduziu elementos como `<header>`, `<nav>`, `<article>`, `<section>`, `<footer>`, cada um com funções específicas que melhoram a estrutura e a acessibilidade.

### Elementos Semânticos vs Elementos de Layout
- **Elementos Semânticos**: Elementos como `<figure>`, `<figcaption>`, `<audio>` e `<video>` trazem significado ao conteúdo, melhorando a relação entre dados e apresentação.
- **Elementos de Layout**: Elementos como `<div>` e `<span>` são utilizados predominantemente para estilização e não possuem significado semântico intrínseco.

### Outros Elementos Semânticos
- **Exemplos**: Elementos como `<meter>` e `<progress>` são importantes para indicar progresso em tarefas e fornecer feedback visual semântico e acessível de maneira eficaz.

### Melhores Práticas em HTML Semântico
- **Organização do Código**: Utilizar HTML semântico facilita a leitura, manutenibilidade do código e colaboração entre desenvolvedores.
- **Estrutura da Página**: Implementar corretamente tags de estrutura como `<header>`, `<nav>`, `<main>`, `<aside>`, e `<footer>` para fornecer uma estrutura clara e lógica.
- **Validação**: Validar o código com ferramentas como W3C para garantir conformidade, acessibilidade, e evitar problemas de interpretação em diferentes navegadores.

## Conclusão
A compreensão da linguagem de marcação, especialmente HTML, e sua semântica é fundamental para construir documentos web bem estruturados e significativos. A adoção da separação entre conteúdo e apresentação, a abordagem semântica, e a utilização adequada de tags são essenciais para criar páginas web que sejam não apenas funcionalmente corretas, mas também acessíveis e otimizadas para SEO. Desenvolvedores familiarizados com estas práticas estarão mais bem preparados para se destacar tanto em avaliações técnicas quanto no mercado de trabalho.

---

## Referências
1. W3C. (2021). *HTML5 – A vocabulary and associated APIs for HTML and XHTML*. Disponível em: [https://www.w3.org/TR/html51/](https://www.w3.org/TR/html51/)
2. Mozilla Developer Network. (2023). *HTML: HyperText Markup Language*. Disponível em: [https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
3. WHATWG. (2023). *HTML Living Standard*. Disponível em: [https://html.spec.whatwg.org/multipage/](https://html.spec.whatwg.org/multipage/)
4. A Importância do HTML Semântico: Melhores Práticas - DIO. Disponível em: [https://www.dio.me/articles/a-importancia-do-html-semantico-melhores-praticas](https://www.dio.me/articles/a-importancia-do-html-semantico-melhores-praticas)
5. Semântica HTML: O que é e por que é importante | Blog da TreinaWeb. Disponível em: [https://www.treinaweb.com.br/blog/semantica-html-o-que-e-e-por-que-e-importante](https://www.treinaweb.com.br/blog/semantica-html-o-que-e-e-por-que-e-importante)
6. HTML Semântico: Por que é Importante e Boas Práticas. Disponível em: [https://skillstecnologicas.com/html-semantico/](https://skillstecnologicas.com/html-semantico/)
7. HTML Semântico: Conheça os elementos semânticos da HTML5. Disponível em: [https://www.devmedia.com.br/html-semantico-conheca-os-elementos-semanticos-da-html5/38065](https://www.devmedia.com.br/html-semantico-conheca-os-elementos-semanticos-da-html5/38065)
8. HTML: Boas práticas em acessibilidade - MDN Web Docs. Disponível em: [https://developer.mozilla.org/pt-BR/docs/Learn/Accessibility/HTML](https://developer.mozilla.org/pt-BR/docs/Learn/Accessibility/HTML)
```