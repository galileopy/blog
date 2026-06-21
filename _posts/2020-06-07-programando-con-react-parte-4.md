---
layout: post
title: "Programando con React - Parte 4"
date: 2020-06-07 17:33:00 
slug: programando-con-react-parte-4
lang: es
permalink: /es/programando-con-react-parte-4/
tags:
  - redux
  - react
  - programacion funcional
excerpt: "Definiendo los eventos, los datos y sus transformaciones para trabajar con Redux."
original_status: published
---

# La arquitectura Flux

Programar es fácil, lo difícil es razonar sobre nuestros programas, entonces el truco para programar tranquilos es utilizar métodos que nos faciliten el razonamiento sobre nuestros programas. Por suerte, no somos los únicos que estamos tratando de encontrar formas de ser más efectivos.

Los genios en Facebook también se dieron cuenta que no importa que tan brillantes sean sus programadores, su productividad se reduce estrepitosamente cuando la carga cognitiva, a la hora de diseñar nuevas funcionalidades o buscar errores, es muy alta.

Y con eso en mente diseñaron (o encontraron? no está claro, ya que Flux tiene mucha similaridad con MVU del mundo Elm ), una arquitectura que simplifica todo al poner como fundamento el principio de la comunicación unidireccional.

**Comunicación unidireccional:** Cada componente de un sistema debe enviar mensajes solamente en una dirección y recibir mensajes solamente de otra dirección. Es decir, nuestra vista solo recibe datos del controlador, y el controlador solo recibe datos del repositorio, y el repositorio solo recibe datos de la vista.

Podemos entender mejor la idea si nos fijamos en el siguiente gráfico.

![](/content/images/2020/06/flux.svg-2.png)

## Redux y la Arquitectura Flux

Hasta ahora hemos cubierto intensivamente los principios fundamentales que nos van a ayudar a utilizar de forma ordenada y efectiva la arquitectura Flux en nuestro proyecto.

Luego modelamos la capa de datos de nuestra aplicación a la que llamamos Estado, el estado es similar al Modelo en la arquitectura MVC.

> Flux propone una arquitectura en la que el flujo de datos es unidireccional. Los datos viajan desde la vista por medio de acciones y llegan a un Store [repositorio] desde el cual se actualizará la vista de nuevo.
> 
> Carlos Azuarte - [Cómo funciona Flux?](<https://carlosazaustre.es/como-funciona-flux>)

### Los principios detrás de Redux

  * **Única fuente de verdad** , el estado global de tu aplicación es almacenado en un árbol de objetos dentro un único repositorio de datos.
  * **El Estado es de sólo lectura** , la única forma de modificar el estado es emitiendo un objeto _acción_ que describe las modificaciones que aplicar al estado, (lo que estábamos llamando evento)
  * **Los cambios son hechos con funciones puras** , para especificar cómo se ve afectado el estado por una acción escribimos funciones que se llaman "reductores", reciben una copia del estado actual de la aplicación y la acción ocurrida para retornar el nuevo estado, sin modificar el anterior, respetando el principio de pureza de las funciones.



Si desarrollamos el hábito de escribir funciones puras, lo único que nos queda es, constantemente hacernos y responder una sola pregunta

  * Al ocurrir un evento `X`, cómo se modifica el estado de la aplicación?



Para eso debemos bajar a tierra los conceptos de

  * Estado
  * Acción



Pero como trabajamos con código, en vez de bajar a tierra, escribiremos un poco de código. Lo primero que vamos a hacer es configurar nuestro proyecto con las dependencias necesarias.
    
    
    npm install --save redux react-redux
    npm install --save-dev @types/redux  @types/react-redux
    

Luego comenzamos configurando nuestro repositorio y pasar la representación de nuestro estado, para eso vamos a crear la siguiente estructura de archivos.

Vamos a comenzar por la parte más sencilla, las acciones y sus identificadores, creamos entonces el siguiente fichero, `src/redux/actionTypes.ts`, aquí listamos en un `enum` los tipos de acciones posibles de nuestra aplicación.
    
    
    // ACTION TYPES
    export enum IdsAcciones {
      TAREAS_AGREGAR = "TAREAS/AGREGAR",
      TAREAS_FILTRAR = "TAREAS/FILTRAR",
      TAREAS_MARCAR_TODAS = "TAREAS/MARCAR_TODAS",
      TAREAS_ELIMINAR_FINALIZADAS = "TAREAS/ELIMINAR_FINALIZADAS",
      TAREA_CAMBIAR_ESTADO = "TAREA/CAMBIAR_ESTADO",
      TAREA_EDITAR = "TAREA/EDITAR",
      TAREA_ELIMINAR = "TAREA/ELIMINAR",
      TAREA_MOVER = "TAREA/MOVER",
      __WARN_DEFAULT = "NO_UTILIZAR/ESTO_ES_SOLO_POR_INTEROP",
    }
    

Particularmente a mí me gusta tener todos los tipos de acciones, así como las acciones, en un solo lugar, ya que no importa qué tan grande sea nuestra aplicación, las acciones tienen identificadores únicos, por lo que tenerlas todas en un solo lugar nos permite ver fácilmente si estamos duplicando identificadores.

Ahora es cuestión de definir nuestras acciones, como dijimos anteriormente, las acciones se procesan al ocurrir eventos, y deben contener la información necesaria para el cambio de estado.

Es por eso que las acciones tienen dos propiedades muy características, una de ellas es que tienen un identificador o "tipo", y la otra es que llevan la información del evento, en React uno es libre de elegir como definir su objeto acción, sin embargo a mí me gusta mantener un esquema sencillo y manejar siempre la misma estructura, un objeto con dos propiedades,

  * _Type_ , indica el tipo de acción, esto lo dejamos en inglés porque más adelante utilizaremos una librería para manejo de lógicas asíncronas complejas, y cuentan con que la acción debe tener la propiedad `type`
  * Contenido, es la información generada por el evento.



Ahora podemos empezar a crear nuestras acciones, y unas funciones especiales que se llaman funciones creadoras,

Primero definimos una interfaz para nuestras acciones, a manera de contar con un estándar para todos los tipos de acciones.

Creamos un archivo `src/redux/actions.ts`
    
    
    import { IdsAcciones } from "./actionTypes";
    import { FiltroTarea, Tarea, Estados } from "../types/Tarea";
    
    export declare namespace Acciones {
      export interface AgregarTarea {
        type: typeof IdsAcciones.TAREAS_AGREGAR;
        contenido: { descripcion: string };
      }
      export interface MarcarTareas {
        type: typeof IdsAcciones.TAREAS_MARCAR_TODAS;
        contenido: { estado: Estados };
      }
      export interface FiltrarTareas {
        type: typeof IdsAcciones.TAREAS_FILTRAR;
        contenido: {
          filtro: FiltroTarea;
        };
      }
      export interface CambiarEstado {
        type: typeof IdsAcciones.TAREA_CAMBIAR_ESTADO;
        contenido: {
          tarea: Tarea;
        };
      }
      export interface EditarTarea {
        type: typeof IdsAcciones.TAREA_EDITAR;
        contenido: {
          tarea: Tarea;
          descripcion: string;
        };
      }
      export interface MoverTarea {
        type: typeof IdsAcciones.TAREA_MOVER;
        contenido: {
          tarea: Tarea;
          posicion: number;
        };
      }
      export interface EliminarTarea {
        type: typeof IdsAcciones.TAREA_ELIMINAR;
        contenido: {
          tarea: Tarea;
        };
      }
      export interface EliminarFinalizadas {
        type: typeof IdsAcciones.TAREAS_ELIMINAR_FINALIZADAS;
        contenido: null;
      }
    
      export type Tareas =
        | MoverTarea
        | EditarTarea
        | CambiarEstado
        | FiltrarTareas
        | MarcarTareas
        | AgregarTarea
        | EliminarFinalizadas
        | EliminarTarea;
    }

Si desean un artículo que hable exclusivamente de TypeScript y su sistema de tipo de datos, pueden dejarme unos comentarios. Asumo que muchos tienen alguna experiencia trabajando con TypeScript o Java, y que las definiciones aunque de tipos serán fáciles de seguir.

Continuamos escribiendo los creadores de acciones, los creadores de acciones son solamente funciones que recibirán los datos necesarios para las acciones y retornan un objeto que cumpla con nuestra interfaz para las acciones.

Nuestro archivo `src/redux/actions.ts` quedaría así
    
    
    import { IdsAcciones } from "./actionTypes";
    import { FiltroTarea } from "../types/Tarea";
    
    // export declare namespace Acciones { ....
    // ... definicion de las acciones
    
    const agregarTarea = (datos: {
      descripcion: string;
    }): Acciones.AgregarTarea => ({
      type: IdsAcciones.TAREAS_AGREGAR,
      contenido: datos,
    });
    const finalizarTareas = (): Acciones.FinalizarTareas => ({
      type: IdsAcciones.TAREAS_FINALIZAR,
      contenido: null,
    });
    const filtrarTareas = (datos: {
      filtro: FiltroTarea;
    }): Acciones.FiltrarTareas => ({
      type: IdsAcciones.TAREAS_FILTRAR,
      contenido: datos,
    });
    const cambiarEstado = (datos: { tarea: Tarea }): Acciones.CambiarEstado => ({
      type: IdsAcciones.TAREA_CAMBIAR_ESTADO,
      contenido: datos,
    });
    const editarTarea = (datos: {
      tarea: Tarea;
      descripcion: string;
    }): Acciones.EditarTarea => ({
      type: IdsAcciones.TAREA_EDITAR,
      contenido: datos,
    });
    const moverTarea = (datos: {
      tarea: Tarea;
      posicion: number;
    }): Acciones.MoverTarea => ({
      type: IdsAcciones.TAREA_MOVER,
      contenido: datos,
    });
    
    const eliminarFinalizadas = (): Acciones.EliminarFinalizadas => ({
      type: IdsAcciones.TAREAS_ELIMINAR_FINALIZADAS,
      contenido: null,
    });
    
    const eliminarTarea = (datos: { tarea: Tarea }): Acciones.EliminarTarea => ({
      type: IdsAcciones.TAREA_ELIMINAR,
      contenido: datos,
    });
    
    export const Creadores = {
      agregarTarea,
      finalizarTareas,
      filtrarTareas,
      cambiarEstado,
      editarTarea,
      moverTarea,
      eliminarTarea,
      eliminarFinalizadas,
    };
    

Y con eso terminamos esta parte, la próxima nos dedicamos a explicar las funciones reductoras, y vemos si nos llegamos a preparar nuestras vistas y a discutir un poco sobre los componentes en React.
