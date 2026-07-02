import re
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from sympy import sympify, to_dnf, simplify_logic
from sympy.logic.boolalg import truth_table

# =============================================================================
# LÓGICA DE BACKEND (Tu código original intacto)
# =============================================================================
def transformar_a_sympy_booleano(expresion):
    s = expresion.upper().replace(" ", "").replace(".", "&").replace("*", "&").replace("+", "|")
    while "'" in s:
        idx = s.index("'")
        if idx > 0 and s[idx-1] == ")":
            balance = 1
            j = idx - 2
            while j >= 0 and balance > 0:
                if s[j] == ")": balance += 1
                elif s[j] == "(": balance -= 1
                j -= 1
            pos_apertura = j + 1
            s = s[:pos_apertura] + "~" + s[pos_apertura:idx] + s[idx+1:]
        elif idx > 0 and s[idx-1].isalnum():
            pos_variable = idx - 1
            s = s[:pos_variable] + "~" + s[pos_variable] + s[idx+1:]
        else:
            s = s[:idx] + s[idx+1:]
    return s

def transformar_a_usuario_booleano(expresion_sympy):
    txt = str(expresion_sympy)
    txt = re.sub(r"~([A-Z0-9])", r"\1'", txt)
    while "~(" in txt:
        txt = re.sub(r"~\(([^()]+)\)", r"(\1)'", txt)
    txt = txt.replace(" & ", ".").replace("&", ".").replace(" | ", "+").replace("|", "+")
    return txt.replace("True", "1").replace("False", "0")

def transformar_a_sympy_logica(expresion):
    s = expresion.lower().replace(" ", "")
    s = s.replace("<->", "==").replace("<=>", "==").replace("↔", "==")
    s = s.replace("->", ">>").replace("=>", ">>").replace("→", ">>")
    s = s.replace(".", "&").replace("*", "&").replace("+", "|")
    while "'" in s:
        idx = s.index("'")
        if idx > 0 and s[idx-1] == ")":
            balance = 1
            j = idx - 2
            while j >= 0 and balance > 0:
                if s[j] == ")": balance += 1
                elif s[j] == "(": balance -= 1
                j -= 1
            pos_apertura = j + 1
            s = s[:pos_apertura] + "~" + s[pos_apertura:idx] + s[idx+1:]
        elif idx > 0 and s[idx-1].isalnum():
            pos_variable = idx - 1
            s = s[:pos_variable] + "~" + s[pos_variable] + s[idx+1:]
        else:
            s = s[:idx] + s[idx+1:]
    return s

# =============================================================================
# VISTAS / PANTALLAS (KIVY)
# =============================================================================

class MenuPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text="BOOLEAN MASTER 2.0", font_size='32sp', bold=True, size_hint_y=0.3))
        
        btn_bool = Button(text="Álgebra Booleana", size_hint_y=0.15, font_size='18sp')
        btn_bool.bind(on_press=self.ir_a_booleana)
        layout.add_widget(btn_bool)
        
        btn_tablas = Button(text="Tablas de Verdad", size_hint_y=0.15, font_size='18sp')
        btn_tablas.bind(on_press=self.ir_a_tablas)
        layout.add_widget(btn_tablas)
        
        btn_salir = Button(text="Salir", size_hint_y=0.15, font_size='18sp', background_color=(1, 0, 0, 1))
        btn_salir.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(btn_salir)
        
        self.add_widget(layout)

    def ir_a_booleana(self, instance):
        self.manager.current = 'booleana'

    def ir_a_tablas(self, instance):
        self.manager.current = 'tablas'


class PantallaBooleana(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="SIMPLIFICADOR BOOLEANO", font_size='20sp', bold=True, size_hint_y=0.08))
        layout.add_widget(Label(text="Ejemplo: (A+B)'+(A.B')'", font_size='14sp', size_hint_y=0.05))
        
        self.entrada = TextInput(text="(A+B)'+(A.B')'", multiline=False, size_hint_y=0.08, font_size='16sp')
        layout.add_widget(self.entrada)
        
        box_botones = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        btn_resolver = Button(text="RESOLVER", bold=True)
        btn_resolver.bind(on_press=self.resolver)
        btn_volver = Button(text="VOLVER", background_color=(0.4, 0.4, 0.4, 1))
        btn_volver.bind(on_press=self.volver)
        box_botones.add_widget(btn_resolver)
        box_botones.add_widget(btn_volver)
        layout.add_widget(box_botones)
        
        scroll = ScrollView(size_hint_y=0.69)
        self.salida = Label(text="", size_hint_y=None, halign='left', valign='top', font_size='14sp')
        self.salida.bind(texture_size=self.salida.setter('size'))
        scroll.add_widget(self.salida)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

    def volver(self, instance):
        self.manager.current = 'menu'

    def resolver(self, instance):
        f = self.entrada.text.upper().replace("Y=", "").replace("F=", "").replace(" ", "")
        texto_resultado = f"EJERCICIO DE ENTRADA:\nY = {f}\n\n"
        
        try:
            f_sympy_texto = transformar_a_sympy_booleano(f)
            expr = sympify(f_sympy_texto)
            texto_resultado += "DESGLOSE ANALÍTICO PASO A PASO:\n\n"
            
            expr_expandida = to_dnf(expr, simplify=False)
            txt_expandida = transformar_a_usuario_booleano(expr_expandida)
            
            if txt_expandida != f:
                texto_resultado += f"• Paso 1: De Morgan / Distribución:\n  => {txt_expandida}\n\n"
                actual = expr_expandida
            else:
                actual = expr
                
            expr_reducida = to_dnf(actual, simplify=True)
            txt_reducida = transformar_a_usuario_booleano(expr_reducida)
            
            if txt_reducida != txt_expandida:
                texto_resultado += f"• Paso 2: Reduciendo idénticos y complementos:\n  => {txt_reducida}\n\n"
                actual = expr_reducida

            expr_final = simplify_logic(actual, form='dnf')
            resultado_final = transformar_a_usuario_booleano(expr_final)
            
            if resultado_final != txt_reducida:
                texto_resultado += f"• Paso 3: Factorización y absorción:\n  => {resultado_final}\n\n"
            elif resultado_final == f:
                texto_resultado += "• El ejercicio ya está minimizado.\n\n"
                
            texto_resultado += "---------------------------------------\n"
            texto_resultado += f"MINIMIZACIÓN FINAL MÁXIMA:\nY = {resultado_final}"
        except Exception as e:
            texto_resultado = f"ERROR DE SINTAXIS: Verifica paréntesis.\nDetalle: {str(e)}"
            
        self.salida.text = texto_resultado


class PantallaTablas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="GENERADOR DE TABLAS DE VERDAD", font_size='18sp', bold=True, size_hint_y=0.08))
        
        self.entrada = TextInput(text="(p -> q) . (q -> r)", multiline=False, size_hint_y=0.08, font_size='16sp')
        layout.add_widget(self.entrada)
        
        box_botones = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        btn_resolver = Button(text="CONSTRUIR TABLA", bold=True)
        btn_resolver.bind(on_press=self.resolver)
        btn_volver = Button(text="VOLVER", background_color=(0.4, 0.4, 0.4, 1))
        btn_volver.bind(on_press=self.volver)
        box_botones.add_widget(btn_resolver)
        box_botones.add_widget(btn_volver)
        layout.add_widget(box_botones)
        
        scroll = ScrollView(size_hint_y=0.74)
        self.salida = Label(text="", size_hint_y=None, halign='left', valign='top', font_name='Roboto', font_size='13sp')
        self.salida.bind(texture_size=self.salida.setter('size'))
        scroll.add_widget(self.salida)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

    def volver(self, instance):
        self.manager.current = 'menu'

    def resolver(self, instance):
        f = self.entrada.text.replace(" ", "")
        texto_resultado = f"PROPOSICIÓN EVALUADA:\nF = {self.entrada.text}\n\n"
        
        try:
            variables_encontradas = sorted(list(set(re.findall(r'[p-zP-Z]', f.lower()))))
            if not variables_encontradas:
                self.salida.text = "ERROR: No se detectaron variables (p, q, r, s)."
                return
                
            f_sympy_texto = transformar_a_sympy_logica(f)
            expr = sympify(f_sympy_texto)
            
            encabezado = " | ".join([v.upper() for v in variables_encontradas]) + " || RESULTADO"
            texto_resultado += encabezado + "\n"
            texto_resultado += "=" * len(encabezado) + "\n"
            
            resultados_finales = []
            variables_sympy = [sympify(v) for v in variables_encontradas]
            tabla = truth_table(expr, variables_sympy)
            
            for combinacion in tabla:
                valores_entrada = combinacion[:-1]
                resultado_fila = combinacion[-1]
                
                str_entradas = " | ".join([" V " if v else " F " for v in valores_entrada])
                str_resultado = "   V" if resultado_fila else "   F"
                
                resultados_finales.append(resultado_fila)
                texto_resultado += f" {str_entradas} || {str_resultado}\n"
                
            texto_resultado += "=" * len(encabezado) + "\n\n"
            
            if all(resultados_finales):
                clasificacion = "TAUTOLOGÍA (Todas [V])"
            elif not any(resultados_finales):
                clasificacion = "CONTRADICCIÓN (Todas [F])"
            else:
                clasificacion = "CONTINGENCIA (Mezcla V/F)"
                
            texto_resultado += f"PROPIEDAD:\n=> {clasificacion}\n"
        except Exception as e:
            texto_resultado = f"ERROR DE SINTAXIS: Verifica conectores.\nDetalle: {str(e)}"
            
        self.salida.text = texto_resultado


class BooleanMasterApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name='menu'))
        sm.add_widget(PantallaBooleana(name='booleana'))
        sm.add_widget(PantallaTablas(name='tablas'))
        return sm

if __name__ == '__main__':
    BooleanMasterApp().run()