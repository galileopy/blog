---
layout: post
title: "Programando con React - Parte 6"
date: 2020-06-20 16:16:38 
slug: programando-con-react-parte-6
lang: es
permalink: /es/programando-con-react-parte-6/
tags:
  - react
  - redux
original_status: published
---

# Representando las vistas

En el último capítulo vimos cómo procesar las acciones y alterar el estado, si bien no todas nuestras funciones son puras, una gran mayoría lo son, la excepción a la regla fue la utilidad UUID para generar los Id de las tareas. Pudimos haber implementado un contador, y generar identificadores de forma secuencial, pero la idea es ser prácticos y no puristas.

## Motivación

Necesitamos ver el resultado de nuestro trabajo de forma visual, al fin y al cabo estamos haciendo un tutorial de front-end con React.

## Objetivo

Conectar nuestro repositorio `redux` con la aplicación `React.js`

## Configurando el repositorio

El la última parte nos faltó, instalar la dependencia `uuid`, comencemos por ahí
    
    
    npm install --save uuid
    npm install --save-dev @types/uuid 
    

Luego continuamos editando el archivo `src/redux/store.ts`
    
    
    import { createStore } from "redux"; // importamos la función createStore de redux
    import reducers from "./reducers"; // nuestra función reductora
    
    // declaramos que puede existir una variable en el objeto global window
    declare global {
      interface Window {
        __REDUX_DEVTOOLS_EXTENSION__: any;
      }
    }
    // Esto lo envolvemos en una función para evitar que se ejecute antes de cargar la aplicación
    const configureStore = () => {
      const store = createStore(
        reducers,
        // le pasamos al repositorio si es que existe, la función de configuración para redux-dev-tools
        window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
      );
      return store;
    };
    
    export default configureStore;
    

Redux Dev Tools una extensión de navegador que nos permite ver todas las acciones emitidas por nuestra aplicación, y cómo afecta el estado.  
Al configurar nuestro repositorio aprovechamos para inyectar un poco de código que nos permite conectar el repositorio con la herramienta `redux-dev-tools`  
[Extensión para Chrome](<https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en>)  
[Extensión para Firefox](<https://addons.mozilla.org/en-US/firefox/addon/reduxdevtools/>)

Luego configuramos nuestra aplicación, y le pasamos el repositorio configurado, en `src/index.tsx`
    
    
    import React from "react";
    import ReactDOM from "react-dom";
    // 1: Importamos Provider de react-redux
    import { Provider } from "react-redux";
    
    import App from "./App";
    // 2: Importamos nuestro repositorio redux
    import createStore from "./redux/store";
    import * as serviceWorker from "./serviceWorker";
    
    // 3: Inicializamos el repositorio
    const store = createStore();
    
    ReactDOM.render(
      <React.StrictMode>
        {/*Envolvemos App en el provider de react-redux y le pasamos el repositorio*/}
        <Provider store={store}>
          <App />
        </Provider>
      </React.StrictMode>,
      document.getElementById("root")
    );
    
    // If you want your app to work offline and load faster, you can change
    // unregister() to register() below. Note this comes with some pitfalls.
    // Learn more about service workers: https://bit.ly/CRA-PWA
    serviceWorker.unregister();
    
    

### *.TSX?

Aquí nos encontramos con una pequeña diferencia, hasta ahora estuvimos trabajando exclusivamente con archivos `*.ts` que es código fuente de `TypesScript`, pero este archivo es una mezcla de TypeScript y lo que parece ser HTML o alguna suerte de XML, el código `tsx ` es justamente eso, es una forma de trabajar con componentes como si fueran etiquetas de HTML, pero que en realidad están implementadas como funciones, ya veremos más adelante cómo funciona eso ya que escribiremos un montón de `tsx`.

No hay mucha diferencia con escribir código TypeScript común y corriente. Lo único que cambia es que cuando importamos React, también podemos referirnos a los componentes de `react` utilizando la notación `<Componente attributo={variable}> Componentes hijos </Componente>`. Para una información más detallada al respecto, podemos revisar la documentación de JSX, que es el hermano mayor de TSX.

[Presentando JSX](<https://es.reactjs.org/docs/introducing-jsx.html>)

## Agregando CSS

No nos vamos a complicar con el css, ya que eso viene de manos del diseñador, y por suerte en nuestro caso ya tenemos todas nuestras clases definidas en el plantilla de TodoMVC.

Simplemente importamos las hojas de estilo en el fichero que viene por defecto al crear nuestra aplicación, `public/index.html` y agregamos la siguiente línea dentro de la etiqueta `head`, aprovechamos para cambiar la el título de nuestra aplicación.
    
    
    <!--archivo: public/index.html -->
    <head>
        <!--... código existente -->
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/todomvc-app-css@2.3.0/index.css"
        />
        <!--... más código -->
        <title>Tareas</title>
    </head>
    

## Al fin React!

Ya tenemos todo listo para comenzar a hacer nuestras vistas. Lo primero que tenemos que hacer es crear un archivo donde vamos a escribir nuestro primer componente.

Comencemos con la estructura de `App.tsx`
    
    
    import React from "react";
    import Tareas from "./pages/Tarea";
    export default () => {
      return (
        <div>
          <Tareas />
          <footer className="info">
            <p>Doble Click para editar una Tarea</p>
            <p>
              Template by <a href="http://sindresorhus.com">Sindre Sorhus</a>
            </p>
            <p>
              Creado por <a href="https://galileopy.com">Galileo Sánchez</a>
            </p>
            <p>
              Part of <a href="http://todomvc.com">TodoMVC</a>
            </p>
          </footer>
        </div>
      );
    };
    

Luego definamos `src/pages/Tarea/index.tsx`
    
    
    mkdir -p src/pages/Tarea
    touch src/pages/Tarea/index.tsx
    
    
    
    import React from "react";
    
    import TareaHeader from "./TareaHeader";
    import TareaList from "./TareaList";
    import TareaFooter from "./TareaFooter";
    
    export default () => (
      <section className="todoapp">
        <TareaHeader />
        <TareaList />
        <TareaFooter />
      </section>
    );
    

Y con eso ya vamos estructurando nuestro programa, una breve descripción de lo que hará cada componente parece útil en este momento.

  * `TareaHeader`: Tendrá el campo de texto y el botón de agregar tarea.
  * `TareaList`: Mostrará los elementos de la lista de tareas
  * `TareaFooter`: Tendrá algunos controles para filtrar las tareas y eliminar tares finalizadas.



Comenzamos por `src/pages/Tarea/TareaHeader.tsx`
    
    
    // useState es un `hook` de react, nos permite manejar un estado interno en los componentes sin tener que propagar eventos 
    // al repositorio principal, muy útil para manejar información temporal y datos que no necesitan propagarse a toda la 
    // aplicación, podemos verlo cómo si fuera un constructor para un pequeño repositorio local
    import React, { useState } from "react";
    import { connect, ConnectedProps } from "react-redux";
    
    // Necesitamos emitir el evento `agregarTarea`
    import { Creadores } from "../../redux/actions";
    
    const ENTER_KEY = 13;
    // 1: esto se utiliza para conectar con Redux. Vamos a hablar de  ello a más profundidad.
    const mapDispatch = {
      // nuestro componente recibirá una propiedad `agregar` que nos permitira emitir el evento
      agregar: Creadores.agregarTarea,
    };
    
    // connect genera un Componente de Alto Nivel que está conectado al repositorio
    const connector = connect(null, mapDispatch);
    
    // Utilizamos este helper para poder especificar que tipo de datos que vamos a recibir
    type Props = ConnectedProps<typeof connector>;
    
    /// nuestro componente básico
    const TareaHeader = (props: Props) => {
      // el evento
      const { agregar } = props;
      // un repositorio para guardar la descripción mientras se edita
      const [descripcion, setDescripcion] = useState("");
      // a medida que va cambiando nuestro input vamos actualizando la variable descripción
      const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setDescripcion(e.target.value);
      };
      // cuando nuestro input recibe un enter, emitimos el evento agregar y reinicializamos la descripción local
      const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.keyCode === ENTER_KEY) {
          agregar({ descripcion });
          setDescripcion("");
        }
      };
      return (
        <header className="header">
          <h1>tareas</h1>
          <input
            className="new-todo"
            value={descripcion} // variable local
            placeholder="Qué tienes que hacer?"
            onChange={onChange} // actualizar la variable local
            onKeyDown={onKeyDown} // emitir el evento global agregar({ descripción }) y reinicializar la descripción
          />
        </header>
      );
    };
    // exportamos el componenente conectado ya al repositorio redux
    export default connector(TareaHeader);
    

## mapDispatch y mapState

Redux nos provee una función especial que nos provee dos mecanismos para conectar nuestros componentes al repositorio principal de redux. Esta función se llama `connect` toma como argumento dos funciones sencillas, una la primera suele llamarse `mapState` y la segunda `mapDispatch`.

  * `mapState`: es una función que recibe el estado actual y debe retornar un objeto con propiedades del estado que queremos tener disponibles en nuestro componente, en nuestro ejemplo anterior no tuvimos necesidad de usar esta función y por lo tanto pasamos `null` a `connect`.
  * `mapDispatch`: puede ser una función o un objeto, la forma más sencilla es utilizar un objeto cuyas propiedades sean funciones que retornen una acción a ser procesada por nuestras funciones reductoras y afecten el estado, en nuestro caso le pasamos la función que crea la acción `agregarTarea`



Continuemos con lo aprendido y vayamos al componente más completo de los tres.
    
    
    // archivo: src/pages/Tarea/TareaItem.tsx
    import React, { useState } from "react";
    import { Tarea, Estados } from "../../types/Tarea";
    import { Creadores } from "../../redux/actions";
    import { ConnectedProps, connect } from "react-redux";
    
    const ENTER_KEY = 13;
    
    const mapDispatch = {
      // cuando cambiamos el checkbox
      cambiarEstado: Creadores.cambiarEstado,
      // cuando nos ponemos a editar
      actualizarDescripcion: Creadores.editarTarea,
      // cuando hacemos click en la x
      eliminarTarea: Creadores.eliminarTarea,
    };
    
    const connector = connect(null, mapDispatch);
    // recibiremos la tarea desde la lista, no del estado
    type LocalProps = {
      tarea: Tarea;
    };
    // definimos el tipo del argumento del componente
    type Props = LocalProps & ConnectedProps<typeof connector>;
    
    const TareaItem = (props: Props) => {
      // la tarea y los manejadores de eventos los recibimos como argumento
      const { tarea, cambiarEstado, actualizarDescripcion, eliminarTarea } = props;
      // cuando hacemos doble click debemos mostrar el input
      const [editando, setEditando] = useState(false);
      // función auxiliar para ser llamada en doble click
      const activarEditar = () => setEditando(true);
      // cuando se termina la edición volvemos a ocultar el input
      const onEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.keyCode === ENTER_KEY) {
          setEditando(false);
        }
      };
      // función auxiliar a ser llamada al hacer click en el checkbox
      const onCambiarEstado = () => cambiarEstado({ tarea });
      // a medida que ingresamos valores en el input ya vamos editando la tarea
      const onEdicion = (e: React.ChangeEvent<HTMLInputElement>) =>
        actualizarDescripcion({ tarea, descripcion: e.target.value });
      // si la tarea está finalizada cambiamos la clase del label
      const hecho = tarea.estado === Estados.Hecho;
      // si la tearea está siendo editada cambiamos la clase
      // a editing, si está finalizada a "completed", y si no, no lleva ninguna clase
      const itemClass = editando ? "editing" : hecho ? "completed" : "";
    
      return (
        <li className={itemClass}>
          <div className="view">
            <input
              className="toggle"
              type="checkbox"
              checked={hecho} // valor del checkbox
              onChange={onCambiarEstado} // conectamos el evento
            />
            <label onDoubleClick={activarEditar}>{tarea.descripcion}</label>
            <button
              className="destroy"
              onClick={() => eliminarTarea({ tarea })}
            ></button>
          </div>
          <input
            className="edit"
            value={tarea.descripcion} // el valor del input es el valor actual de la tarea
            onChange={onEdicion} // a medida que ingresamos datos, vamos actualizando la tarea
            onKeyUp={onEnter} // si es enter cambiamos el estado local "editando"
          />
        </li>
      );
    };
    
    // exportamos el componente conectado al estado de redux
    export default connector(TareaItem);
    
    

Ahora podemos continuar directamente al componente Lista, que se encargará de llamar al componente Ítem con una tarea a la vez.
    
    
    // archivo: src/pages/Tarea/TareaList.tsx
    import React from "react";
    import { connect, ConnectedProps } from "react-redux";
    
    import TareaItem from "./TareaItem";
    
    import { Creadores } from "../../redux/actions";
    import { RootState } from "../../redux/reducers";
    import { Estados } from "../../types/Tarea";
    import { invertirEstado } from "../../state/Tarea";
    
    const mapState = (state: RootState) => ({
      lista: state.tarea.lista, // la lista del estado
      filtro: state.tarea.filtro, // el filtro actual
      marcador: state.tarea.marcador, // el estado del marcador global
    });
    
    const mapDispatch = {
      marcarTodas: Creadores.marcarTodas, // para marcar todas las tareas
    };
    
    const connector = connect(mapState, mapDispatch); 
    
    // el tipo de nuestro argumento
    type Props = ConnectedProps<typeof connector>;
    // debe recibir la lista de tareas y todos los handlers
    
    const TareaList = (props: Props) => {
      // nuestras funciones de eventos y nuestros datos todos fueron conectado con `connector`
      const { filtro, lista, marcador, marcarTodas } = props;
      // cuando la lista está vacía no mostramos nada
      if (lista.length === 0) return null;
      // el estado del check de marcar todas
      const marcadas = marcador === Estados.Hecho;
      return (
        <section className="main">
          <input
            id="toggle-all"
            className="toggle-all"
            type="checkbox"
            checked={marcadas} // si el marcador está en hecho, está marcada, de lo contrario no
            onChange={() => marcarTodas({ estado: invertirEstado(marcador) })} // marcar todas invierte el estado del marcador global y modifica todas las tareas con el mismo
          />
          <label htmlFor="toggle-all">Finalizar todas</label>
          <ul className="todo-list">
            {lista // filtramos las tareas de acuerdo al filtro
              .filter((tarea) => tarea.estado & filtro)
              .map((tarea) => ( // por cada tarea generamos un item
                <TareaItem key={tarea.id.toString()} tarea={tarea} />
              ))}
          </ul>
        </section>
      );
    };
    // exportamos el componente conectado
    export default connector(TareaList);
    
    

Y ahora solo nos falta el pié de página, les dejó así como está, interpretar lo que hace ya queda como ejercicio del lector.
    
    
    import React from "react";
    import { ListaTarea, Estados, FiltroTarea } from "../../types/Tarea";
    import { connect, ConnectedProps } from "react-redux";
    import { Creadores } from "../../redux/actions";
    import { RootState } from "../../redux/reducers";
    
    const mapState = (state: RootState) => ({
      lista: state.tarea.lista,
      filtro: state.tarea.filtro,
    });
    
    const mapDispatch = {
      filtrar: Creadores.filtrarTareas,
      eliminarFinalizadas: Creadores.eliminarFinalizadas,
    };
    
    const connector = connect(mapState, mapDispatch);
    
    // debe recibir el cambio de filtros
    // necesitamos una que elmine las terminadas
    type Props = ConnectedProps<typeof connector>;
    
    const TareasFooter = (props: Props) => {
      const { lista, filtrar, eliminarFinalizadas } = props;
      if (lista.length === 0) return null;
      const pendientes = lista.filter((tarea) => tarea.estado === Estados.Pendiente)
        .length;
      const completas = lista.filter((tarea) => tarea.estado === Estados.Hecho)
        .length;
    
      const filtrarTodas = () => filtrar({ filtro: FiltroTarea.Todos });
      const filtrarHechas = () => filtrar({ filtro: FiltroTarea.Hecho });
      const filtrarPendientes = () => filtrar({ filtro: FiltroTarea.Pendiente });
    
      return (
        <footer className="footer">
          <span className="todo-count">
            <strong>{pendientes}</strong> tareas pendientes
          </span>
          <ul className="filters">
            <li>
              <button className="selected" onClick={filtrarTodas}>
                Todas
              </button>
            </li>
            <li>
              <button onClick={filtrarPendientes}>Pendientes</button>
            </li>
            <li>
              <button onClick={filtrarHechas}>Terminadas</button>
            </li>
          </ul>
          {completas > 0 ? (
            <button
              onClick={() => eliminarFinalizadas()}
              className="clear-completed"
            >
              Eliminar terminadas
            </button>
          ) : null}
        </footer>
      );
    };
    
    export default connector(TareasFooter);
    
    

Éxitos! Y para la próxima entrega vamos a modificar nuestra aplicación para incorporar enrutamiento dinámico de vistas y obtener los filtros de las rutas y no de los estados.

Si llegaron hasta este punto, puede probar su aplicación ejecutando
    
    
    npm start
    

Y yendo a `localhost:3000` desde cualquier navegador.
