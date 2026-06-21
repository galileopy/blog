---
layout: post
title: "Programando con React - Parte 2"
date: 2020-05-28 22:56:44 
slug: programando-con-react-parte-2
lang: es
permalink: /es/programando-con-react-parte-2/
tags:
  - react
  - remeda
  - programacion funcional
excerpt: "Funciones puras, transparencia referencial y determinismo, por qué son importantes? Y cómo nos facilitan la vida, una guía práctica."
original_status: published
---

# Funciones Puras y Remeda

## Motivación

En esta ocasión quiero hacer hincapié en dos aspectos fundamentales de la programación funcional, que son específicamente, la pureza de las funciones y la transparencia referencial (que es una de las consecuencias de la utilización de funciones puras), y más que nada, cómo podemos obtener los beneficios de estos principios en JavaScript, ya que por defecto el lenguaje no cuenta con restricciones o mecanismos para asegurar el cumplimiento de estos principios.

Si bien estamos trabajando en TypeScript, aquellos que deseen seguir el tutorial utilizando JavaScript, simplemente deben reemplazar Remeda por Ramda, que es la base de inspiración de Remeda, pero con la característica que respeta JavaScript idiomático.

## Objetivo

Preparar las funciones de transformación de los estados para nuestra aplicación de _Lista de Tareas_ , utilizando la librería Remeda para facilitar el cumplimiento de los principios de pureza de las funciones y transparencia referencial.

## Funciones puras

Una función pura no modifica el valor del argumento, más bien retorna un nuevo valor, esto nos permite compartir valores y resultados en nuestro código con mucha libertad y sin tener que andar pensando en condiciones de carrera, y todos los problemas relacionados a la concurrencia con valores mutables.

Es importante recordar que una aplicación web es altamente concurrente, podemos estar procesando eventos de usuario, estar suscritos a APIs, y realizamos un sin fin de llamadas remotas en todo momento.

Se dice que una función es pura, si es que

  * Llamada con el mismo argumento retorna el mismo valor, es decir es determinista,
  * No tiene efectos secundarios observables.



### Determinismo

Es importante destacar, que cuando decimos que el valor de la función es determinista, nos restringe inmediatamente a no utilizar valores globales.

Supongamos que tenemos una función para calcular el valor de una circunferencia definida de la siguiente manera.
    
    
    const circunferencia = (radio: number) => 2 * radio * Math.PI
    

Esta función, aunque podría ser considerada pura en TypeScript, porque la propiedad `Math.PI` es declarada como `readonly`, no lo sería en JavaScript, porque accede a la variable global `Math.PI` que puede ser modificada.

Para implementar `circunferencia` como función pura en JavaScript podemos utilizar algunos trucos. Uno de ellos es definir PI dentro de la función.
    
    
    const circunferencia = (radio) => {
        const PI = 3.1416
        return 2 * radio * PI
    }
    

El otro es recibir el argumento pi en la firma de la función
    
    
    const circunferenciaParametrizada = (pi, radio) => 2 * radio * pi
    
    

Sin embargo esto se vuelve tedioso si es que llamamos mucho a la función `circunferenciaParametrizada`, entonces podemos recurrir al uso de cerraduras para pasar el valor de PI una sola vez.
    
    
    const generarFuncionCircunferencia = pi => radio => 2 * radio * pi
    const circunferencia = generarFuncionCircunferencia(3.1416)
    // la constante circunferencia es una función, que es el valor retornado por 
    // generarFuncionCircunferencia, luego de haber 'capturado' el valor de pi.
    

Y con esto vemos una segunda técnica, la captura de argumentos en funciones anidadas, herramienta que nos será muy útil más adelante para entender la aplicación parcial de funciones, que nos permitirá utilizar el estilo _Programación de Punto Libre_.

### Sin efectos secundarios observables

Ejemplos de efectos secundarios son la modificación de un parámetro, o de un objeto global.

Un ejemplo sencillo que podemos utilizar es la siguiente función
    
    
    const objeto = { x: 12 };
    const incrementarX = (obj) => {
    	obj.x = obj.x + 1
        return obj
    }
    incrementarX(objeto) // { x: 13 }
    objeto // { x: 13 }
    

Esta función no es pura, ya que el valor de `objecto.x` se verá afectado luego de llamar a la función `incrementarX`.

Para implementarla de forma pura deberíamos retornar un nuevo objeto con
    
    
    const objeto = { x: 12 };
    const incrementarX = (obj) => {
        return { x: obj.x + 1};
    }
    incrementarX(objeto) // { x: 13 }
    objeto // { x: 12 }
    

Aunque este es un caso trivial, tenemos la desventaja que en casos más complejos nos pondríamos a generar un nuevo objeto con todas las propiedades que no utilizamos dentro de esta función.

Y es ahí donde Remeda nos ayuda, ya que para un caso más complejo podríamos utilizar la función `merge`
    
    
    import { merge } from "remeda";
    const objeto2 =  { x:1, y: 2, z: 3 };
    const incrementarX = (obj) => merge(obj, { x: obj.x + 1 });
    incrementarX(objeto2) // { x: 2, y: 2, z: 3  }
    objeto2 // { x: 1, y: 2, z: 3 }
    

Caso que no se daría si somos perezosos y terminamos modificando el parámetro recibido como en el siguiente caso.
    
    
    const objeto2 =  { x:1, y: 2, z: 3 };
    const incrementarX = (obj) => {
        obj.x = obj.x + 1;
        return obj
    };
    incrementarX(objeto2) // { x: 2, y: 2, z: 3  }
    objeto2 // { x: 2, y: 2, z: 3 } -- Mal! Modificamos el valor del parámetro 
    

Cuando utilizamos librerías que cumplen con este principio, conseguimos cumplir con el segundo principio de nuestro interés.

## Transparencia Referencial

Se dice que una función es transparente en sus referencias cuando cualquier llamada a función puede ser cambiada por el valor de la expresión a la que evalúa sin alterar el comportamiento del programa. Esto nos facilita increíblemente el trabajo de modificar nuestro código.

Es decir, garantiza que nuestro código sea independiente del contexto, esto significa que nuestras funciones pueden ser ejecutadas en cualquier contexto y siempre retornará el mismo resultado. Esto nos facilita intercambiar una función pura por otra con una implementación diferente.

Para dejarlo más claro, elimina el problema de que cambiamos algo en nuestro código y falla en otra, no relacionada.

## [Remeda](<https://remedajs.com/>)
    
    
    npm install --save remeda
    

Remeda es una librería utilitaria, escrita en TypeScript, ejecutable desde JavaScript, que se rige por los principios de pureza de las funciones y transparencia referencial, (esto también se aplica con Ramda), lo que nos ayuda a mantener un estilo de programación estable en todo nuestro proyecto.

Además de proveer con un conjunto importante de funciones puras, Remeda tiene una segunda particularidad, sus funciones vienen con un soporte limitado para aplicación parcial, característica que nos será útil para escribir programas más descriptivos en el futuro, utilizando un estilo de programación que se llama _De Punto Libre_.

Y con esto, finalizamos la segunda parte de nuestra serie, la próxima ya tendremos algo que programar y continuar con nuestra aplicación de _Lista de Quehaceres_.

En particular definiremos los eventos, y los estados a los que cambiará en cada evento, respetando los principios que hemos visto hasta ahora.
