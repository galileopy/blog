---
layout: post
title: "Programando con React - Parte 3"
date: 2020-05-29 19:41:16 
slug: programando-con-react-parte-3
lang: es
permalink: /es/programando-con-react-parte-3/
tags:
  - react
  - remeda
  - programacion funcional
excerpt: "Trabajando con datos estructurados, conceptos de programación funcional, determinismo y transparencia referencial. "
original_status: published
---

# Transformaciones y Datos Estructurados

Ya tenemos lo necesario para comenzar a hacer algo más divertido que solo leer, al fin vamos a codear un poco. Pero no nos olvidemos de nuestra estructura de trabajo.

## Motivación

Comenzar con una API, no con una aplicación, una de las cosas que más facilitan la vida a la hora de programar aplicaciones complejas, es comenzar por el diseño.

Sin embargo, no es necesario sacar una herramienta de UML, (a menos que estés haciendo algo realmente grande para un cliente exigente). Pero para la práctica, podemos enfocarnos en nuestras estructuras de datos y las transformaciones para la presentación.

Es bueno definir todas las transformaciones de datos que vamos a utilizar, hoy nos vamos concentrar en las transformaciones de estado con los eventos correspondientes, y luego veremos cómo transformar el estado en vistas. Utilizando siempre los mismos principios.

  * Pureza en las funciones
  * Transparencia referencial
  * Trabajar con Datos Estructurados



## Objetivo

Definir las estructura del estado de nuestra aplicación, los eventos que disparan las modificaciones a ese estado, y dejar todo listo para incorporar Redux a nuestra aplicación.

## Datos Estructurados

Trabajar con datos estructurados es la principal razón por la que estamos experimentando con TypeScript. Sabemos que vamos a hacer una lista de tareas, entonces empecemos definiendo el modelo de datos.

De buenas a primeras, vamos a describir nuestra aplicación para poder extraer los eventos, el estado principal de nuestra aplicación y los eventos que van a afectar ese estado.

  * Agregar una nueva tarea: ingresa la descripción de la tarea en un campo de texto, y al presionar la tecla Enter, se debe agregar una nueva tarea al final de la lista de tareas, con el campo descripción reflejando la entrada de usuario, un nuevo id de tarea, y con el estado en pendiente por defecto.
  * Cambiar el estado de una tarea: En la lista de tareas se va a presentar una casilla de selección que nos permite cambiar el estado de la tarea de pendiente a hecho y viceversa.
  * Editar tarea: En la lista de tareas, si el usuario hace doble clic sobre una tarea debemos permitirle editar la descripción de la tarea seleccionada.
  * Filtrar la lista: Vamos a ofrecer un control con tres filtros. 
    * Todas las tareas
    * Tareas finalizadas
    * Tareas pendientes
  * Marcar como finalizadas todas las tareas.
  * Mover tarea (Extra): , vamos a ver si llegamos a re-ordenar la tarea utilizando _drag-and-drop_



Antes que nada vamos a abrir nuestro editor en la carpeta de proyecto y crearemos una nueva carpeta `types` con un archivo llamado `src/types/Tarea.ts`
    
    
    export enum Estados {
      Pendiente,
      Hecho,
    }
    
    export interface Tarea {
      estado: Estados;
      descripcion: string;
      id: number;
    }
    
    export type ListaTarea = Tarea[];
    export type FiltroTareas = Estados;
    
    export interface EstadoLista {
        lista: ListaTareas;
        filtro: FiltroTareas;
    }
    
    

Y con eso tenemos definido el modelo de datos de nuestra aplicación, y el estado de nuestra aplicación debe cumplir con la interfaz `EstadoLista`

Ahora nos toca definir la lista de eventos posibles, estos afectan el estado de nuestra aplicación, y lo actualizan, reflejando las interacciones que el usuario tiene con la misma.

De la descripción podemos extraer los siguientes eventos, con sus efectos sobre el estado.

`agregarTarea` es un evento que inserta a `listaTareas` una nueva tarea, el contenido o valor del evento es la descripción de la tarea, sin embargo para insertarla a la lista nosotros debemos generar un objeto `Tarea` con los campos `id, estado`, para eso podemos comenzar con una función que transforma una descripción a una tarea.

Cómo vamos a trabajar con el estado?, y cómo reacciona a cada evento?, podemos crear un archivo llamado `src/state/Tarea.ts`, y comenzamos
    
    
    import { Tarea, Estados } from "../types/Tarea"
    const descripcionATarea = (descripcion: string) : Tarea => ({
        descripcion,
        estado: Estados.Pendiente
        id: // de donde obtenemos el id?
    })
    

Casi lo logramos, pero aún no sabemos de donde vamos a obtener el `id`, no podemos tomarlo de una variable global, porque estaríamos perdiendo la transparencia referencial, como vimos, en la unidad anterior cuando hablábamos de transparencia referencial, es preferible recibir todos los datos como parámetros de la función.
    
    
    import { Tarea, Estados } from "../types/Tarea"
    
    const descripcionATarea = (id: number, descripcion: string) : Tarea => ({
        id,
        descripcion,
        estado: Estados.Pendiente
    })
    

Ahora, lo que nos pasa es que debemos obtener el `id` antes de insertar una tarea, por qué no definimos que el `id` será, el próximo indice disponible en la lista de tareas?

Nuestro archivo `src/state/Tarea.ts` quedará así.
    
    
    import { Tarea, Estados, ListaTarea } from "../types/Tarea";
    import { concat } from "remeda";
    
    const descripcionATarea = (id: number, descripcion: string): Tarea => ({
      id,
      descripcion,
      estado: Estados.Pendiente,
    });
    
    const agregarTarea = (lista: ListaTarea, descripcion: string): ListaTarea =>
      concat(lista, [descripcionATarea(lista.length, descripcion)]);
    // utilizamos la funcion concat de Remeda porque nos garantiza transparencia referencial
    

Y con eso tenemos ya definido como vamos a reaccionar al evento `AGREGAR_TAREA`, podemos aplicar el mismo tipo de proceso para los demás eventos con su correspondiente alteración en el estado.

Para el evento `CAMBIAR_ESTADO` nos basta con recibir el estado de la tarea en cuestión e invertir el estado, es decir, si está en `Pendiente` pasamos a `Hecho` y viceversa.
    
    
    const invertirEstado = (estado: Estados): Estados => {
      switch (estado) {
        case Estados.Pendiente:
          return Estados.Hecho;
        case Estados.Hecho:
          return Estados.Pendiente;
      }
    };
    

Utilizando esta función, podemos crear otra que recibe una tarea y retorna una nueva, actualizando el estado
    
    
    import { concat, merge } from "remeda";
    // ...
    const cambiarEstado = (tarea: Tarea): Tarea =>
      merge(tarea, { estado: invertirEstado(tarea.estado) });
    // merge es como Object.assign(obj1, obj2) implementado como una funcion pura
    

Utilizando una idea similar para cambiar la descripción de una tarea,
    
    
    import { concat, merge } from "remeda";
    // ...
    const cambiarDescripcion = (tarea: Tarea, descripcion: string): Tarea =>
      merge(tarea, { descripcion });
    

Volvemos a utilizar la función `merge` de `remeda`. Ahora nos queda actualizar la lista de tareas con la nueva tarea; para eso primero debemos tener un mecanismo que, dada una tarea y una lista, reemplace la tarea en el índice correspondiente, esto lo podemos lograr con tres funciones auxiliares de `remeda`

[drop](<https://remedajs.com/docs#drop>): toma una lista y un índice, y descarta todos los elementos del arreglo hasta el índice excluyente.

[take](<https://remedajs.com/docs#take>): toma una lista y un índice, y descarta todos los elementos del arreglo desde el índice inclusive.

[flatten](<https://remedajs.com/docs#flatten>): toma un arreglo de arreglos y "aplana" el arreglo en un solo arreglo con los elementos de los sub-arreglos.
    
    
    import { drop, take} from "remeda";
    
    drop([1, 2, 3, 4, 5], 3) // => [3, 4, 5]
    take([1, 2, 3, 4, 5], 2) // => [1, 2]
    flatten([[1, 2], [3], [4, 5]]) // => [1, 2, 3, 4, 5]
    

Si recordamos que el `id` de una tarea corresponde al índice que ocupa en la lista, podemos implementar la función `actualizarLista` de la siguiente manera:
    
    
    import { concat, merge, take, drop, flatten } from "remeda";
    // ...
    const actualizarLista = (lista: ListaTarea, tarea: Tarea) =>
      flatten([
          take(lista, tarea.id), // retorna un arreglo hasta la tarea, excluyente
          [tarea], // es un arreglo con un sólo elemento, inserta la tarea
          drop(lista, tarea.id + 1)] // retorna el resto del arreglo, después de la tarea
      );
    

Y finalmente combinamos las funciones de manera que podamos llamar solamente a una función en cada evento.
    
    
    const actualizarDescripcion = (
      lista: ListaTarea,
      tarea: Tarea,
      descripcion: string
    ) => actualizarLista(lista, cambiarDescripcion(tarea, descripcion));
    
    const actualizarEstado = (lista: ListaTarea, tarea: Tarea) =>
      actualizarLista(lista, cambiarEstado(tarea));
    

Nos falta el evento `MOVER_TAREA`, para esto volveremos a utilizar a las funciones `drop, take, flatten`, con la diferencia que además de quitar el elemento de su lugar y asignarle un nuevo lugar, debemos también, recordar que el índice de todas las tareas será afectado. Y que el `id` ya no puede representar al índice de la tarea, y nos va a tocar hacer unos cuantos cambios interesantes. Que espero que nos ayuden a ver las ventajas de nuestra forma de trabajar.

Antes que nada, revisamos cómo está nuestro archivo `src/state/Tarea.ts`
    
    
    import { Tarea, Estados, ListaTarea } from "../types/Tarea";
    import { concat, merge, take, drop, flatten } from "remeda";
    
    const descripcionATarea = (id: number, descripcion: string): Tarea => ({
      id,
      descripcion,
      estado: Estados.Pendiente,
    });
    
    const invertirEstado = (estado: Estados): Estados => {
      switch (estado) {
        case Estados.Pendiente:
          return Estados.Hecho;
        case Estados.Hecho:
          return Estados.Pendiente;
      }
    };
    
    const cambiarEstado = (tarea: Tarea): Tarea =>
      merge(tarea, { estado: invertirEstado(tarea.estado) });
    
    const cambiarDescripcion = (tarea: Tarea, descripcion: string): Tarea =>
      merge(tarea, { descripcion });
    
    const agregarTarea = (lista: ListaTarea, descripcion: string): ListaTarea =>
      concat(lista, [descripciónATarea(lista.length, descripcion)]);
    
    const actualizarLista = (lista: ListaTarea, tarea: Tarea) =>
      flatten([take(lista, tarea.id), [tarea], drop(lista, tarea.id + 1)]);
    
    const actualizarDescripcion = (
      lista: ListaTarea,
      tarea: Tarea,
      descripcion: string
    ) => actualizarLista(lista, cambiarDescripcion(tarea, descripcion));
    
    const actualizarEstado = (lista: ListaTarea, tarea: Tarea) =>
      actualizarLista(lista, cambiarEstado(tarea));
    

Al revisar nos damos cuenta que en las funciones `actualizarLista` y `agregarTarea` hacemos uso de la idea de que el índice es el `id` de la tarea. Si nos comprometemos que el `id` será único en la lista siempre podemos hacer los siguientes cambios.
    
    
    import { concat, merge, take, drop, flatten, findIndex } from "remeda";
    
    // ...
    
    const agregarTarea = (
      lista: ListaTarea,
      id: number,
      descripcion: string
    ): ListaTarea => concat(lista, [descripcionATarea(lista.length, descripcion)]);
    
    const actualizarLista = (lista: ListaTarea, tarea: Tarea) => {
      const indice = findIndex(lista, (t) => t.id === tarea.id);
      flatten([take(lista, indice), [tarea], drop(lista, indice + 1)]);
    };
    

Utilizando la función `findIndex` de `remeda`, y recibiendo el `id` como parámetro en `agregarTarea`.

Y antes de empezar con el último paso, me gustaría modificar la función `descripcionATarea` ya que originalmente construía una `Tarea` desde una descripción, pero ahora es lo que se llama una función de construcción, ojo, no es lo mismo que el constructor de un objeto, pero cumple con un propósito similar, al tomar unos parámetros y retornar un objeto con los valores recibidos y otros valores por defecto, para que `descripcionATarea` sea una función de construcción, debe recibir todas las propiedades como argumento de la función, y quedaría así.
    
    
    import { concat, merge, take, drop, flatten, findIndex } from "remeda";
    
    // ..
    
    const nuevaTarea = (
      id: number,
      descripcion: string,
      estado = Estados.Pendiente
    ): Tarea => ({
      id,
      descripcion,
      estado,
    });
    
    /// agregar tarea también la tenemos que modficar
    const agregarTarea = (
      lista: ListaTarea,
      id: number,
      descripcion: string
    ): ListaTarea => concat(lista, [nuevaTarea(lista.length, descripcion)]);
    

Ahora simplemente nos toca mover la tarea, dividimos la lista en dos partes de acuerdo al nuevo indice con la función `splitAt` de `remeda`, eliminamos la tarea de ambas listas resultantes con la función `reject` de `remeda` y concatenamos las listas incorporando la tarea en el medio.
    
    
    import { concat, merge, take, drop, flatten, findIndex, splitAt } from "remeda";
    
    // ..
    
    const moverTarea = (lista: ListaTarea, tarea: Tarea, indice: number) => {
      // partimos el arreglo en dos, en el lugar donde insertaremos la tarea
      const [pre, post] = splitAt(lista, indice);
      return flatten([
        reject(pre, (t) => t.id === tarea.id),// retorna un arreglo sin la tarea
        [tarea], // el arreglo con la tarea en su nueva posición
        reject(post, (t) => t.id === tarea.id),// retorna un arreglo sin la tarea
      ]);
    };
    

Y como punto extra, vemos que la función anónima `(t) => t.id === tarea.id` , ya la hemos escrito tres veces, una buena practica es si algo lo escribiste tres veces, lo debes abstraer.
    
    
    const mismoId = (t1: Tarea) => (t2: Tarea) => t1.id === t2.id;
    

Esta función retorna una función, que es un predicado. Toma la primera tarea y retorna una función que espera una segunda tarea para comparar, esto ya nos va dando una idea de cómo se el estilo de punto libre, cuando utilizamos en la función siguiente.
    
    
    import { concat, merge, take, drop, flatten, findIndex, splitAt, reject } from "remeda";
    
    // ...
    
    const moverTarea = (lista: ListaTarea, tarea: Tarea, indice: number) => {
      const [pre, post] = splitAt(lista, indice);
      return flatten([
          // pasamos solo la primera tarea, y nos queda una funcion que recibirá una a una cada
          // tarea del arreglo y comparará el id de la primera con el resto
          reject(pre, mismoId(tarea)), 
          [tarea],
          reject(post, mismoId(tarea)),
      ]);
    };
    

Y nuestro archivo `src/state/Tarea.ts` quedará así.
    
    
    import { Tarea, Estados, ListaTarea } from "../types/Tarea";
    import {
      concat,
      merge,
      take,
      drop,
      flatten,
      findIndex,
      splitAt,
      reject,
    } from "remeda";
    
    const nuevaTarea = (
      id: number,
      descripcion: string,
      estado = Estados.Pendiente
    ): Tarea => ({
      id,
      descripcion,
      estado,
    });
    
    const invertirEstado = (estado: Estados): Estados => {
      switch (estado) {
        case Estados.Pendiente:
          return Estados.Hecho;
        case Estados.Hecho:
          return Estados.Pendiente;
      }
    };
    
    const cambiarEstado = (tarea: Tarea): Tarea =>
      merge(tarea, { estado: invertirEstado(tarea.estado) });
    
    const cambiarDescripcion = (tarea: Tarea, descripcion: string): Tarea =>
      merge(tarea, { descripcion });
    
    const mismoId = (t1: Tarea) => (t2: Tarea) => t1.id === t2.id;
    
    const agregarTarea = (
      lista: ListaTarea,
      id: number,
      descripcion: string
    ): ListaTarea => concat(lista, [nuevaTarea(lista.length, descripcion)]);
    
    const actualizarLista = (lista: ListaTarea, tarea: Tarea) => {
      const indice = findIndex(lista, mismoId(tarea));
      return flatten([take(lista, indice), [tarea], drop(lista, indice + 1)]);
    };
    
    const actualizarDescripcion = (
      lista: ListaTarea,
      tarea: Tarea,
      descripcion: string
    ) => actualizarLista(lista, cambiarDescripcion(tarea, descripcion));
    
    const actualizarEstado = (lista: ListaTarea, tarea: Tarea) =>
      actualizarLista(lista, cambiarEstado(tarea));
    
    const moverTarea = (lista: ListaTarea, tarea: Tarea, indice: number) => {
      const [pre, post] = splitAt(lista, indice);
      return flatten([
        reject(pre, mismoId(tarea)),
        [tarea],
        reject(post, mismoId(tarea)),
      ]);
    };
    

Y con esto finalizamos el modelado del estado de nuestra aplicación, como podrán probar, cada una de estas funciones cumple con los principios que queremos adoptar.

Para la próxima presentación, veremos cómo manejar el estado de nuestra aplicación con `redux` y cómo representar el estado en un `reducer`.
