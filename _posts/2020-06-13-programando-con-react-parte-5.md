---
layout: post
title: "Programando con React - parte 5"
date: 2020-06-13 23:16:51 
slug: programando-con-react-parte-5
lang: es
permalink: /es/programando-con-react-parte-5/
tags:
  - redux
  - react
  - flux
  - funciones reductoras
original_status: published
---

# Integrando Redux

## Motivación

Integrar los conceptos que revisamos en el capítulo anterior, tanto a nivel conceptual como en el código.

## Objetivo

Configurar el Estado de nuestra aplicación con el repositorio proveído por redux, si tenemos tiempo también vamos a ir paso a paso,

## Actualizaciones

Como siempre ocurre que nos actualizan las especificaciones, no puede ser diferente con este curso, resulta que las especificaciones de TodoMVC, son un poco más completas, y me faltó definir algunas características. Lo tomamos con buena onda cómo lo haríamos, en la vida real?, y procedemos a actualizar las especificaciones

La definición del estado general de la aplicación a lo que teníamos originalmente planeado. Agregamos la propiedad `marcador: Estados` en `EstadoLista`, esto se debe a que una de las funcionalidades de la aplicación es marcar todas las tareas a la vez, y funciona de la siguiente manera.

  * Marcar todas las tareas: pasa todas las tareas a estado finalizado, si es que alguna no está finalizada, si todas están en el mismo estado, entonces revertir el estado en todas, vamos a agregar una nueva propiedad al estado para poder hacer seguimiento correcto de cómo ir modificando lo estados ante este evento.
  * Eliminar una tarea: cada ítem de la lista de tareas puede ser eliminado haciendo clic en una `x` convenientemente posicionada en la misma línea del ítem en cuestión.
  * Eliminar todas las tareas finalizadas: Tendremos un botón que elimine todas las tareas que se encuentren finalizadas.



Comencemos con las actualizaciones a`src/types/Tarea.ts`
    
    
    //  vamos a utilizar nuestros Enums como banderas para el filtro
    export enum Estados {
      Pendiente = 1 << 0, // 001
      Hecho = 1 << 1, // 010
    }
    // Y el filtro puede tener cualquier combinación de estados
    export enum FiltroTarea {
      Ninguno = 0, 			// 000
      Pendiente = 1 << 0, 	// 001
      Hecho = 1 << 1, 		// 010
      Todos = ~(~0 << 2), 	// 111
    }
    // si tuvieramos más estados solo nos preocupamos por mantener 
    // la secuencia, luego los combinamos con los operadores a nivel de bit | y &
    
    export interface Tarea {
      estado: Estados;
      descripcion: string; // cambio de String a string por compatibiliad de tipos
      id: string; // cambio de number a string para utilizar uuids
    }
    
    export type ListaTarea = Tarea[];
    
    export interface EstadoLista {
      lista: ListaTarea;
      filtro: FiltroTarea;
      // 
      marcador: Estados;
    }
    

Las actualizaciones están comentadas en `src/state/Tarea.ts`.
    
    
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
      id: string, // cambia a string
      descripcion: string,
      estado = Estados.Pendiente
    ): Tarea => ({
      id,
      descripcion,
      estado,
    });
    
    // exportamos esta función
    export const invertirEstado = (estado: Estados): Estados => {
      switch (estado) {
        case Estados.Pendiente:
          return Estados.Hecho;
        case Estados.Hecho:
          return Estados.Pendiente;
        default:
              // El compilador requiere que todos los casos posibles estén cubiertos
              // para cumplir con la firma de la función que indica que es sólamente Estado
          throw new Error("Estado no es ninguno de los estados esperados");
      }
    };
    
    const cambiarDescripcion = (tarea: Tarea, descripcion: string): Tarea =>
      merge(tarea, { descripcion });
    
    const mismoId = (t1: Tarea) => (t2: Tarea) => t1.id === t2.id;
    
    const actualizarLista = (lista: ListaTarea, tarea: Tarea) => {
      const indice = findIndex(lista, mismoId(tarea));
      // nos faltaba el return
      return flatten([take(lista, indice), [tarea], drop(lista, indice + 1)]);
    };
    
    export const agregarTarea = (
      lista: ListaTarea,
      id: string, // recibimos un uuid para cada tarea
      descripcion: string
    ): ListaTarea => concat(lista, [nuevaTarea(id, descripcion)]); // aquí habiamos dejado lista.length
    
    export const actualizarDescripcion = (
      lista: ListaTarea,
      tarea: Tarea,
      descripcion: string
    ) => actualizarLista(lista, cambiarDescripcion(tarea, descripcion));
    
    export const cambiarEstado = (tarea: Tarea): Tarea =>
      merge(tarea, { estado: invertirEstado(tarea.estado) });
    
    export const actualizarEstado = (lista: ListaTarea, tarea: Tarea) =>
      actualizarLista(lista, cambiarEstado(tarea));
    
    // Ahora debemos marcar todas las tareas de una sola vez
    export const marcarTodas = (lista: ListaTarea, estado: Estados) =>
      lista.map((tarea) => merge(tarea, { estado }));
    
    // Cada vez que cambiamos el estado de una tarea, debemos comprobar el marcador
    export const comprobarEstados = (lista: ListaTarea, marcador: Estados) =>
      lista.every((tarea) => tarea.estado === Estados.Pendiente)
        ? Estados.Pendiente
        : lista.every((tarea) => tarea.estado === Estados.Hecho)
        ? Estados.Hecho
        : marcador;
    
    // agregamos la funcion para eliminar tareas finalizadas
    export const eliminarFinalizadas = (lista: ListaTarea) =>
      reject(lista, (tarea) => tarea.estado === Estados.Hecho);
    // y otra función para eliminar una tarea dada
    export const eliminarTarea = (lista: ListaTarea, tarea: Tarea) =>
      reject(lista, mismoId(tarea));
    
    export const moverTarea = (lista: ListaTarea, tarea: Tarea, indice: number) => {
      const [pre, post] = splitAt(lista, indice);
      return flatten([
        reject(pre, mismoId(tarea)),
        [tarea],
        reject(post, mismoId(tarea)),
      ]);
    };
    

Con estos cambios podemos seguir a revisar paso a paso las funciones reductoras, que veremos a continuación.

## Funciones Reductoras

Las funciones reductoras es donde gran parte de la magia en `redux` ocurre. El repositorio de `redux`, es un repositorio configurado principalmente para hacer solamente dos cosas.

  * Actualizar el estado con funciones puras.
  * Notificar a sus suscriptores cuando el estado cambió. (En nuestro caso particular, la aplicación `React.js` es el subscriptor)



El estado de la aplicación es toda la información relevante que deben presentar las vistas. Al abstraer el estado de la aplicación en un repositorio central comenzamos verdaderamente a separar las responsabilidades de nuestros componentes. En este caso las funciones de vista o componentes de `React.js`, presentan la información, y el repositorio `redux` sólo se encarga de almacenar el árbol de objetos que representa el estado.

Comenzamos configurando la función reductora principal, en `src/redux/reducers/index.ts`
    
    
    import { combineReducers } from "redux";
    
    import tarea from "./tarea";
    const rootReducer = combineReducers({
      tarea,
    });
    
    export type RootState = ReturnType<typeof rootReducer>;
    export default rootReducer;
    

Y luego `src/redux/reducers/tarea.ts`, comenzamos importando las `Acciones`, los `IdsAcciones`, algunos tipos importantes, y la función `merge`
    
    
    import { Acciones } from "../actions";
    import { IdsAcciones } from "../actionTypes";
    import { EstadoLista, Estados } from "../../types/Tarea";
    import { merge } from "remeda";
    
    // definimos que init es de tipo estado lista para
    // que pueda ser inferido el tipo del primer argumento de la función reductora
    // y para que el compilador nos avise cuando no cumplimos con la interfaz
    const init: EstadoLista = {
      filtro: Estados.Hecho | Estados.Pendiente,
      lista: [],
      marcador: Estados.Pendiente,
    };
    // Aquí es donde vamos a ir reaccionando a los eventos
    export default (estado = init, accion: Acciones.Tareas): EstadoLista => {
      switch (accion.type) {
        default:
          return estado;
      }
    };
    

Esa es la estructura principal de una función reductora. Siempre debemos tener el estado inicial definido, con todas las propiedades que irá teniendo en el transcurso de la aplicación.

La función reductora funciona de la siguiente manera, cada vez que la vista emite una acción, se llama a todas las funciones reductoras que deben retornar una nueva copia del estado, lo que nosotros haremos será sencillo, y es aquí donde comenzaremos a ver las ventajas de nuestra forma de trabajar.

Lo único que hacemos es actualizar el estado con el nuevo valor de acuerdo al tipo de la acción, en el caso de agregar tarea, reemplazamos la vieja lista, con una nueva que tiene anexada la nueva tarea.

Como ya hicimos la mayor parte del trabajo al diseñar nuestra aplicación (al escribir el estado, las acciones, y sus efectos en el estado), lo único que tenemos que hacer, llamar a la función correspondiente, con los valores necesarios y actualizar el estado.

Agreguemos el primer caso.
    
    
    export default (estado = init, accion: Acciones.Tareas): EstadoLista => {
      switch (accion.type) {
        case IdsAcciones.TAREAS_AGREGAR:
          return merge(estado, { 
            lista: agregarTarea(estado.lista, uuid(), accion.contenido.descripcion),
          });
        default:
          return estado;
      }
    };
    

Lo único que hicimos fue agregar el caso en el `switch` y llamar una función, ya que no existe mucho secreto aquí, les dejo el resto.
    
    
    export default (estado = init, accion: Acciones.Tareas): EstadoLista => {
      switch (accion.type) {
        case IdsAcciones.TAREAS_AGREGAR:
          return merge(estado, {
            lista: agregarTarea(estado.lista, uuid(), accion.contenido.descripcion),
          });
        case IdsAcciones.TAREAS_FILTRAR:
          return merge(estado, { filtro: accion.contenido.filtro });
        case IdsAcciones.TAREAS_MARCAR_TODAS:
          return merge(estado, {
            marcador: accion.contenido.estado,
            lista: marcarTodas(estado.lista, accion.contenido.estado),
          });
        case IdsAcciones.TAREA_CAMBIAR_ESTADO: {
          // usamos un bloque para limitar el alcance de nuestras variables
          const lista = actualizarEstado(estado.lista, accion.contenido.tarea);
          return merge(estado, {
            lista,
            marcador: comprobarEstados(lista, estado.marcador),
          });
        }
        case IdsAcciones.TAREA_EDITAR:
          return merge(estado, {
            lista: actualizarDescripcion(
              estado.lista,
              accion.contenido.tarea,
              accion.contenido.descripcion
            ),
          });
        case IdsAcciones.TAREAS_ELIMINAR_FINALIZADAS: {
          // usamos un bloque para limitar el alcance de nuestras variables
    	  // si eliminamos una tarea, debemos comprobar que no sea la última
          // y reiniciar el marcador     
          const lista = eliminarFinalizadas(estado.lista);
          return merge(estado, {
            lista,
            marcador: lista.length === 0 ? Estados.Pendiente : estado.marcador,
          });
        }
        case IdsAcciones.TAREA_ELIMINAR:
          const lista = eliminarTarea(estado.lista, accion.contenido.tarea);
          return merge(estado, {
            lista,
            marcador: lista.length === 0 ? Estados.Pendiente : estado.marcador,
          });
        case IdsAcciones.TAREA_MOVER:
          return merge(estado, {
            lista: moverTarea(
              estado.lista,
              accion.contenido.tarea,
              accion.contenido.posicion
            ),
          });
        default:
          return estado;
      }
    };
    

Y con esto finalizamos nuestras funciones reductoras, y ya terminó la parte difícil, ahora solo nos toca hacer las vistas y conectar todo.
