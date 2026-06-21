---
layout: post
title: "Programando con React - Parte 1"
date: 2020-05-28 16:44:02 
slug: programando-con-react-parte-1
lang: es
permalink: /es/programando-con-react-parte-1/
tags:
  - react
  - redux,
  - programacion funcional
  - pfr
  - flux
excerpt: "Una guía sencilla de cómo empezar un proyecto React con algunas de las mejores tecnologías incorporadas a javascript desde el mundo funcional."
original_status: published
---

## Motivación

Articular de manera explícita los principios fundamentales que me ayudaron a programar mejor, con mayor confianza, alta productividad y menos estrés, espero que articular mi propio proceso de desarrollo me ayude a aferrarme a esos principio de una manera más disciplinada.

## Objetivo

Presentar una serie de artículos, en forma de tutorial, con los principios esenciales que me ayudan diariamente a trabajar de forma armoniosa con React, utilizando fundamentos de programación funcional y adoptando un estilo de programación que va de la mano con la arquitectura Flux, y que aprovecha al máximo Redux con Redux-Observables.

Para ello vamos a cubrir la utilización de algunas herramientas y librerías, además de algunos principios prácticos que deben ser autoimpuestos por el programador.

Para hacer este proceso entretenido, dividiré este trabajo en partes iguales de teoría y práctica, como producto colateral de la presentación, vamos a construir una aplicación de Lista de Quehaceres, (El típico ejemplo del ToDo List), y para que este proceso sea entretenido para mí, voy a utilizar algunas herramientas a las que no estoy acostumbrado, una de ellas es TypeScript y Remeda. Apuntando a evolucionar de mi zona de confort con JavaScript y Ramda.

## Requisitos

Es importante que el lector tenga familiaridad con la consola de comandos de linux, tenga instalado node y npm.

Para comenzar a detallar los aspectos importantes, primero debemos cubrir lo trivial, en este caso, la configuración inicial de las herramientas que vamos a manejar.

Puedes seguir el tutorial desde cero e implementar todo tu mismo, y tienes la opción de seguir los ejemplos desde el repositorio git.

`git clone git@github.com:galileopy/programando_con_react.git`

Cada parte tendrá una etiqueta en git en el formato `tema-x.y` donde X e Y son los números de los capítulos que vamos haciendo.

### Configuración - React con Typescript
    
    
    npx create-react-app programando_con_react --template typescript
    cd programando_con_react
    npm start
    

> Si anteriormente instalaste `create-react-app` utilizando `npm install -g create-react-app`, se recomienda desinstalar el paquete con `npm uninstall -g create-react-app`, para asegurarte que `npx` siempre utilice la última versión.  
> Recomendación del sitio de [React](</programando-con-gali-parte-1/\[https://create-react-app.dev/docs/adding-typescript/>)

## Temas

  1. [React](</programando-con-react-parte-1/>)
  2. [Funciones puras y remeda](</programando-con-react-parte-2/>)
  3. [Transformaciones y Datos Estructurados](</programando-con-react-parte-3/>)
  4. [Arquitectura Flux](</programando-con-react-parte-4/>)
  5. [Integrando Redux](</programando-con-react-parte-4/>)
  6. [Representando las vistas](</programando-con-react-parte-6/>)
  7. Promesas y eventos asíncronos
  8. RxJS y Redux Observables, programación reactiva, incorporando EventStreams (Flujogramas de Eventos)
  9. Funciones totales y Tipos de Datos Algebraicos con Folktale (Functores y Mónadas)
  10. Evolucionando con GhostStories
  11. Tipos de datos según TypeScript



## [React](<https://es.reactjs.org/>)

Extrayendo directamente del sitio de React.js

React es una librería Javascript para construir interfaces de usuario,

#### Declarativo

React te ayuda a crear interfaces de usuario interactivas de forma sencilla. Diseña vistas simples para cada estado en tu aplicación, y React se encargará de actualizar y renderizar de manera eficiente los componentes correctos cuando los datos cambien.

Las vistas declarativas hacen que tu código sea más predecible, por lo tanto, fácil de depurar.

#### Basado en componentes

Crea componentes encapsulados que manejen su propio estado, y conviértelos en interfaces de usuario complejas.

Ya que la lógica de los componentes está escrita en JavaScript y no en plantillas, puedes pasar datos de forma sencilla a través de tu aplicación y mantener el estado fuera del DOM.

Si aún no conoces React, te recomiendo que realices el [tutorial](<https://es.reactjs.org/tutorial/tutorial.html>) antes de seguir, o si prefieres puedes leer la [guía paso a paso](<https://es.reactjs.org/docs/hello-world.html>)

Aunque conocer React es ventajoso para seguir esta guía, no es necesario, ya que nos concentramos exclusivamente en un subconjunto de React, y no nos preocupamos por un montón de sus características. En todo caso, a medida que vamos implementando nuestra aplicación, me ocuparé de dejar links relevantes a la documentación cuando sea necesario.

#### Por qué React?

React nos ofrece la presentación de nuestra interfaz de usuario en un formato similar a HTML llamado JSX, que nos permite construir declarativamente nuestros componentes.

Esto nos facilita la separación de nuestra presentación y la lógica de nuestra aplicación, y nosotros llevaremos eso a un nivel superior con las técnicas que iremos viendo en este tutorial.

Uno de los principio a los que nos vamos a adherir fielmente es

> La presentación debe estar totalmente aislada de la lógica en la medida de lo posible.

Esto nos ayuda a simplificar nuestros componentes, utilizar las mejores partes de React, y a utilizar librerías especializadas para cada parte de la construcción de nuestra aplicación.

Para aquellos más perspicaces, habrán notado que React es una _librería_ , no es un _framework_ , esto quiere decir que se especializa solamente en un conjunto limitado de cosas.

Idealmente sólo debería enfocarse en la presentación, pero como la programación de aplicaciones web es aún algo muy nuevo, las librerías que se enfocan solamente en un problema, del dominio total de problemas, todavía están en un estado muy naciente.

Debido a ello elegimos React, al ser una librería madura que resuelve:

  * La fácil elaboración de componentes de manera declarativa
  * La presentación eficiente de dichos componentes utilizando un concepto llamado _Virtual DOM_
  * Y React tiene un hermano mellizo llamado _React Native_ que nos permite aprender solamente una herramienta y escribir para varias plataformas, Web y Mobile



#### Cómo utilizamos React?

Nosotros descartamos un montón de agregados de React, y nos enfocaremos en utilizar JSX, para definir Componentes Puros, React Hooks para enlazar los componentes con nuestro mecanismo de procesamiento de eventos, que estará conectado a React-Redux y React-Observables.

Es decir la mayoría de nuestros componentes serán

  * Sencillos: No contendrán mucha lógica, a menos que sean componentes de Lógica, que los escribiremos por separado
  * Especializados: Utilizaremos componentes que se concentren únicamente en una cosa, con ello separaremos nuestros componentes en Componentes Lógicos y Componentes de Presentación
  * Reutilizables: Como cada componente es especializado, nos quedarán un montón de componentes reutilizables, y al final del curso incluso tendrás la facultad de escribir Componentes que utilizarás en todos tus proyectos, ya que abstraen procesos que hacemos en cada aplicación.
