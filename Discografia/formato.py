import flet as ft
from conectar import Conectar
from clases import Formato

conectando = Conectar()
cursor = conectando.cursor()


class FormatoVista:

    def mostrar_lista(self, page: ft.Page, volver_menu):
        lista = ft.ListView(expand=True, spacing=8, padding=10)

        def cargar_lista():
            lista.controls.clear()
            try:
                cursor.execute("SELECT id_formato, tipo, conservacion, titulo FROM formato")
                resultados = cursor.fetchall()

                if not resultados:
                    lista.controls.append(ft.Text("No hay formatos registrados.", size=16))
                else:
                    for fila in resultados:
                        id_f, tipo, conservacion, titulo = fila
                        lista.controls.append(
                            ft.Row(controls=[
                                ft.Text(f"[{id_f}] {tipo} | Estado: {conservacion} | Grabación: {titulo}", size=15, expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Modificar",
                                    on_click=lambda e, id=id_f: self.mostrar_buscador_modificar(page, volver_menu, id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, id=id_f: self.eliminar_formato(page, id, cargar_lista)
                                ),
                            ])
                        )
            except Exception as ex:
                lista.controls.append(ft.Text(f"Error: {ex}", color="red"))
            page.update()

        cargar_lista()

        boton_alta  = ft.ElevatedButton("Nuevo Formato", on_click=lambda e: self.mostrar_formulario_alta(page, volver_menu, cargar_lista))
        boton_volver = ft.ElevatedButton("<-- Volver al Menú", on_click=lambda e: volver_menu())

        page.clean()
        page.add(
            ft.Text("Gestión de Formatos", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[boton_alta, boton_volver]),
            ft.Divider(),
            lista
        )
        page.update()

    def mostrar_formulario_alta(self, page: ft.Page, volver_menu, cargar_lista):
        formu_tipo        = ft.TextField(label="Tipo (CD, cinta, vinilo, ...)")
        formu_conservacion = ft.TextField(label="Estado de Conservación (bueno, malo, regular)")
        formu_titulo      = ft.TextField(label="Título de la Grabación asociada")

        def registrar(e):
            fmt = Formato()
            fmt.tipo         = formu_tipo.value.strip()
            fmt.conservacion = formu_conservacion.value.strip()
            fmt.titulo       = formu_titulo.value.strip()

            if not fmt.tipo or not fmt.titulo:
                page.snack_bar = ft.SnackBar(ft.Text("Tipo y Título son obligatorios."), open=True)
                page.update()
                return

            try:
                cursor.execute(
                    "INSERT INTO formato(tipo, conservacion, titulo) VALUES (%s, %s, %s)",
                    (fmt.tipo, fmt.conservacion, fmt.titulo)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text(f"Formato '{fmt.tipo}' registrado."), open=True)
                page.update()
                self.mostrar_lista(page, volver_menu)
            except Exception as ex:
                conectando.rollback()
                page.snack_bar = ft.SnackBar(ft.Text(f" Error: {ex}"), open=True)
                page.update()

        boton_registrar = ft.ElevatedButton("Registrar", on_click=registrar)
        boton_volver    = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Alta de Formato", size=20, weight=ft.FontWeight.BOLD),
            formu_tipo,
            formu_conservacion,
            formu_titulo,
            ft.Row(controls=[boton_registrar, boton_volver])
        )
        page.update()


    def eliminar_formato(self, page, id_formato, cargar_lista):
        try:
            cursor.execute("DELETE FROM formato WHERE id_formato = %s", (id_formato,))
            conectando.commit()
            page.snack_bar = ft.SnackBar(ft.Text(f" Formato ID {id_formato} eliminado."), open=True)
            page.update()
            cargar_lista()
        except Exception as ex:
            conectando.rollback()
            page.snack_bar = ft.SnackBar(ft.Text(f" Error al eliminar: {ex}"), open=True)
            page.update()


    def mostrar_buscador_modificar(self, page: ft.Page, volver_menu, id_preseleccionado=None):
        campo_id = ft.TextField(
            label="ID del Formato a modificar",
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(id_preseleccionado) if id_preseleccionado else ""
        )

        if id_preseleccionado:
            try:
                cursor.execute(
                    "SELECT id_formato, tipo, conservacion, titulo FROM formato WHERE id_formato = %s",
                    (id_preseleccionado,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    fmt = Formato()
                    fmt.id_formato   = resultado[0]
                    fmt.tipo         = resultado[1]
                    fmt.conservacion = resultado[2]
                    fmt.titulo       = resultado[3]
                    self.mostrar_formulario_modificar(page, fmt, volver_menu)
                    return
            except Exception:
                pass

        def buscar(e):
            id_val = campo_id.value.strip()
            if not id_val:
                page.snack_bar = ft.SnackBar(ft.Text("Ingrese un ID."), open=True)
                page.update()
                return
            try:
                cursor.execute(
                    "SELECT id_formato, tipo, conservacion, titulo FROM formato WHERE id_formato = %s",
                    (id_val,)
                )
                resultado = cursor.fetchone()
                if resultado:
                    fmt = Formato()
                    fmt.id_formato   = resultado[0]
                    fmt.tipo         = resultado[1]
                    fmt.conservacion = resultado[2]
                    fmt.titulo       = resultado[3]
                    self.mostrar_formulario_modificar(page, fmt, volver_menu)
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"No encontrado ID: {id_val}"), open=True)
                    page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar)
        boton_volver = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Formato — Buscar por ID", size=20, weight=ft.FontWeight.BOLD),
            campo_id,
            ft.Row(controls=[boton_buscar, boton_volver])
        )
        page.update()

    def mostrar_formulario_modificar(self, page, fmt, volver_menu):
        formu_id          = ft.TextField(label="ID", value=str(fmt.id_formato), read_only=True)
        formu_tipo        = ft.TextField(label="Tipo", value=fmt.tipo)
        formu_conservacion = ft.TextField(label="Conservación", value=fmt.conservacion)
        formu_titulo      = ft.TextField(label="Título Grabación", value=fmt.titulo)

        def guardar(e):
            try:
                cursor.execute(
                    "UPDATE formato SET tipo=%s, conservacion=%s, titulo=%s WHERE id_formato=%s",
                    (formu_tipo.value, formu_conservacion.value, formu_titulo.value, fmt.id_formato)
                )
                conectando.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Formato modificado correctamente."), open=True)
                page.update()
                self.mostrar_lista(page, volver_menu)
            except Exception as ex:
                conectando.rollback()
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
                page.update()

        boton_guardar = ft.ElevatedButton("Guardar Cambios", on_click=guardar)
        boton_volver  = ft.ElevatedButton("<-- Volver", on_click=lambda e: self.mostrar_lista(page, volver_menu))

        page.clean()
        page.add(
            ft.Text("Modificar Formato", size=20, weight=ft.FontWeight.BOLD),
            formu_id,
            formu_tipo,
            formu_conservacion,
            formu_titulo,
            ft.Row(controls=[boton_guardar, boton_volver])
        )
        page.update()