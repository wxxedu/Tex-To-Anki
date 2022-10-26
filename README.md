# Tex To Anki 

This package converts [latex](https://www.latex-project.org/) files to 
[Anki](https://apps.ankiweb.net/) flashcards. 

## Format 

```tex 
\card{
% front content
}{
% back content
}
```

## Setup

### Anki Setup 

Double click on the `Tex-To-Anki.ankiaddon` file to install the plugin. 

### Latex Setup

Copy the `format.sty` into your tex directory, and import it. Or,
alternatively, copy the following command into your tex directory:

```tex 
\newenvironment{ankicard}{}{}
\newenvironment{ankiquestion}{}{}
\newenvironment{ankianswer}{}{}
\newenvironment{ankioption}{}{}
\newenvironment{ankicorrect}{}{}
```

## Usage 

If you want to create a card, in the latex file, wrap the front and back of
your card in the following format: 

```tex
\begin{ankicard} 
\begin{ankiquestion} 
% write your question here
\end{ankiquestion}
\begin{ankianswer} 
% write your answer here 
\end{ankianswer}
\end{ankicard}
```

