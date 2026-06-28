import flet as ft

from compania   import CompaniaVista
from grabaciones import GrabacionVista
from formato    import FormatoVista
from interprete import InterpreteVista
from participa  import ParticipaVista


def menu_principal(page: ft.Page):
  


    vista_compania   = CompaniaVista()
    vista_grabacion  = GrabacionVista()
    vista_formato    = FormatoVista()
    vista_interprete = InterpreteVista()
    vista_participa  = ParticipaVista()


    def volver_menu():
        page.clean()
        menu_principal(page)

    def ir_compania(e):
        page.clean()
        vista_compania.mostrar_lista(page, volver_menu)

    def ir_grabacion(e):
        page.clean()
        vista_grabacion.mostrar_lista(page, volver_menu)

    def ir_formato(e):
        page.clean()
        vista_formato.mostrar_lista(page, volver_menu)

    def ir_interprete(e):
        page.clean()
        vista_interprete.mostrar_lista(page, volver_menu)

    def ir_participa(e):
        page.clean()
        vista_participa.mostrar_lista(page, volver_menu)

    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Text("Salir"), icon=ft.Icons.EXIT_TO_APP,
                             on_click=lambda e: page.window.close()),
        ],
        content=ft.Text("Archivo")
    )

    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Text("Compañía"),    icon=ft.Icons.BUSINESS,         on_click=ir_compania),
            ft.PopupMenuItem(content=ft.Text("Grabaciones"), icon=ft.Icons.MUSIC_NOTE,        on_click=ir_grabacion),
            ft.PopupMenuItem(content=ft.Text("Formato"),     icon=ft.Icons.ALBUM,             on_click=ir_formato),
            ft.PopupMenuItem(content=ft.Text("Intérprete"),  icon=ft.Icons.MIC,               on_click=ir_interprete),
            ft.PopupMenuItem(content=ft.Text("Participa"),   icon=ft.Icons.PEOPLE,            on_click=ir_participa),
        ],
        content=ft.Text("Herramientas")
    )


    # -------------------------------------------------------
    boton_compania   = ft.IconButton(icon=ft.Icons.BUSINESS,    tooltip="Compañía",    on_click=ir_compania)
    boton_grabacion  = ft.IconButton(icon=ft.Icons.MUSIC_NOTE,  tooltip="Grabaciones", on_click=ir_grabacion)
    boton_formato    = ft.IconButton(icon=ft.Icons.ALBUM,       tooltip="Formato",     on_click=ir_formato)
    boton_interprete = ft.IconButton(icon=ft.Icons.MIC,         tooltip="Intérprete",  on_click=ir_interprete)
    boton_participa  = ft.IconButton(icon=ft.Icons.PEOPLE,      tooltip="Participa",   on_click=ir_participa)


 

    page.clean()
    page.add(
        
        ft.Row(
            controls=[archivo_menu, herramientas_menu],
            spacing=10,
        ),
      
        ft.Row(
            controls=[boton_compania, boton_grabacion, boton_formato, boton_interprete, boton_participa]
        ),
        ft.Divider(),
   
    )
    page.update()


def main(page: ft.Page):
    page.title = "Discografía — Don Pepe Muelas"
    page.window.maximized = True
    menu_principal(page)


ft.app(target=main)
