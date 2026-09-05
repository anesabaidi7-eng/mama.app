from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.clock import Clock
from datetime import datetime
import random

import arabic_reshaper
from bidi.algorithm import get_display

from kivy.core.text import LabelBase, DEFAULT_FONT
try:
    LabelBase.register(name='ArabicFont', fn_regular='arialbd.ttf')
    DEFAULT_FONT[0] = 'ArabicFont'
except Exception as e:
    print(f"خطأ في تحميل الخط: {e}")

def ar(text):
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except:
        return text

azkar_list = [
    "«رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ»",
    "«اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت»",
    "«سبحان الله وبحمده، عدد خلقه، ورضا نفسه، وزنة عرشه، ومداد كلماته»",
    "«اللهم إني أسألك العافية في الدنيا والآخرة»",
    "«يا حي يا قيوم برحمتك أستغيث، اصلح لي شأني كله ولا تكلني إلى نفسي طرفة عين»"
]

recipes_list = [
    "شوربة عدس دافئة ومفيدة:\nالمقادير: عدس، بصل، ثوم، جزر، كمون، ملح، زيت زيتون.",
    "كيكة الشاي البسيطة:\nالمقادير: 3 بيضات، كوب سكر، كوب حليب، نصف كوب زيت، 2 كوب دقيق، فانيليا وبكنج بودر.",
    "سلطة خضار طازجة:\nالمقادير: طماطم، خيار، خس، ليمون، زيت زيتون ورشة نعناع."
]

class CardButton(Button):
    def __init__(self, **kwargs):
        super(CardButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.base_color = [0.45, 0.15, 0.25, 1]
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.05, 0.1, 0.9)
            RoundedRectangle(pos=(self.x + 2, self.y - 3), size=self.size, radius=[14])
            
            Color(*self.base_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[14])
            
            Color(0.8, 0.4, 0.5, 0.5)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 14), width=1.5)

    def shift_style(self, *args):
        shades = [
            [0.42, 0.13, 0.23, 1],
            [0.48, 0.18, 0.30, 1],
            [0.52, 0.20, 0.33, 1],
            [0.39, 0.11, 0.20, 1],
            [0.45, 0.16, 0.27, 1]
        ]
        self.base_color = random.choice(shades)
        self.update_canvas()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.15, 0.10, 0.12, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        layout = BoxLayout(orientation='vertical', padding=20, spacing=16, size_hint=(None, None), width=450, height=450)
        
        title = Label(
            text=ar("تطبيق أمي الحبيبة"), 
            font_size=28, 
            color=(1.0, 0.85, 0.9, 1), 
            size_hint_y=None, height=55,
            font_name='ArabicFont',
            halign='center'
        )
        layout.add_widget(title)
        
        buttons_data = [
            ("مفكرة ومواعيد الأدوية", 'medicines'),
            ("مساعد الطبخ الذكي", 'cooking'),
            ("قائمة طلبات البيت", 'shopping'),
            ("مسجل الخلطات السرية", 'recipes'),
            ("حصن المسلم والأدعية", 'azkar')
        ]

        self.anim_buttons = []
        for text, screen_name in buttons_data:
            btn = CardButton(
                text=ar(text), 
                font_size=18, 
                font_name='ArabicFont', 
                color=(1, 1, 1, 1),
                size_hint_y=None, height=52
            )
            btn.bind(on_press=lambda x, s=screen_name: setattr(self.manager, 'current', s))
            layout.add_widget(btn)
            self.anim_buttons.append(btn)
        
        Clock.schedule_interval(self.animate_ui, 4.0)
        
        anchor.add_widget(layout)
        self.add_widget(anchor)

    def animate_ui(self, dt):
        for btn in self.anim_buttons:
            btn.shift_style()

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class MedicinesScreen(Screen):
    def __init__(self, **kwargs):
        super(MedicinesScreen, self).__init__(**kwargs)
        self.last_check_date = datetime.now().date()
        self.med_records = []

        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        layout.add_widget(Label(text=ar("مفكرة ومواعيد الأدوية - تتجدد تلقائياً"), font_size=15, font_name='ArabicFont', color=(0.9, 0.7, 0.8, 1), size_hint_y=None, height=40))
        
        self.med_input = TextInput(hint_text=ar("اكتب اسم الدواء ووقت تناوله..."), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50, multiline=False)
        layout.add_widget(self.med_input)
        
        btn_add = CardButton(text=ar("إضافة للمواعيد"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_add.base_color = [0.45, 0.15, 0.25, 1]
        btn_add.bind(on_press=self.add_med)
        layout.add_widget(btn_add)
        
        self.results_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)
        
        btn_back = CardButton(text=ar("العودة للرئيسية"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_back.base_color = [0.3, 0.18, 0.22, 1]
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)

        Clock.schedule_interval(self.check_daily_reset, 60)
        self.add_widget(layout)

    def add_med(self, instance):
        text = self.med_input.text.strip()
        if text:
            med_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
            lbl = Label(text=ar(text), font_size=16, font_name='ArabicFont', color=(1, 1, 1, 1))
            
            btn_taken = CardButton(text=ar("تم"), font_size=14, font_name='ArabicFont', size_hint_x=None, width=95, size_hint_y=None, height=40)
            btn_taken.base_color = [0.4, 0.2, 0.3, 1]
            btn_taken.bind(on_press=lambda x, l=lbl, t=text: self.mark_taken(l, t))
            
            med_box.add_widget(lbl)
            med_box.add_widget(btn_taken)
            self.results_layout.add_widget(med_box)
            
            self.med_records.append({'layout': med_box, 'label': lbl, 'text': text, 'taken': False})
            self.med_input.text = ""

    def mark_taken(self, lbl, text):
        lbl.text = ar("تم أخذ: " + text)
        for item in self.med_records:
            if item['text'] == text:
                item['taken'] = True

    def check_daily_reset(self, dt):
        current_date = datetime.now().date()
        if current_date > self.last_check_date:
            self.last_check_date = current_date
            for item in self.med_records:
                item['taken'] = False
                item['label'].text = ar(item['text'])


class CookingScreen(Screen):
    def __init__(self, **kwargs):
        super(CookingScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)
        layout.add_widget(Label(text=ar("مساعد الطبخ الذكي"), font_size=22, font_name='ArabicFont', color=(0.9, 0.7, 0.8, 1), size_hint_y=None, height=45))
        
        self.recipe_label = Label(text=ar("اضغطي على الزر أدناه لاقتراح وصفة سريعة"), font_size=18, font_name='ArabicFont', color=(0.95, 0.95, 0.95, 1), halign='center', valign='middle', text_size=(350, 200))
        layout.add_widget(self.recipe_label)
        
        btn_suggest = CardButton(text=ar("اقترحِ وصفة"), font_size=18, font_name='ArabicFont', size_hint_y=None, height=55)
        btn_suggest.base_color = [0.45, 0.15, 0.25, 1]
        btn_suggest.bind(on_press=lambda x: setattr(self.recipe_label, 'text', ar(random.choice(recipes_list))))
        layout.add_widget(btn_suggest)
        
        btn_back = CardButton(text=ar("العودة للرئيسية"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_back.base_color = [0.3, 0.18, 0.22, 1]
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        self.add_widget(layout)


class ShoppingScreen(Screen):
    def __init__(self, **kwargs):
        super(ShoppingScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        layout.add_widget(Label(text=ar("قائمة طلبات البيت"), font_size=22, font_name='ArabicFont', color=(0.9, 0.7, 0.8, 1), size_hint_y=None, height=45))
        
        self.text_input = TextInput(hint_text=ar("اكتب اسم الغرض..."), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50, multiline=False)
        layout.add_widget(self.text_input)
        
        btn_add = CardButton(text=ar("إضافة للقائمة"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_add.base_color = [0.45, 0.15, 0.25, 1]
        btn_add.bind(on_press=self.add_item)
        layout.add_widget(btn_add)
        
        self.results_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)
        
        btn_back = CardButton(text=ar("العودة للرئيسية"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_back.base_color = [0.3, 0.18, 0.22, 1]
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def add_item(self, instance):
        text = self.text_input.text.strip()
        if text:
            item_label = Label(text=ar("- " + text), font_size=18, font_name='ArabicFont', color=(1, 1, 1, 1), size_hint_y=None, height=40)
            self.results_layout.add_widget(item_label)
            self.text_input.text = ""


class RecipesScreen(Screen):
    def __init__(self, **kwargs):
        super(RecipesScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=12)
        layout.add_widget(Label(text=ar("مسجل الخلطات السرية"), font_size=20, font_name='ArabicFont', color=(0.9, 0.7, 0.8, 1), size_hint_y=None, height=45))
        
        self.recipe_name = TextInput(hint_text=ar("اسم الوصفة"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=45, multiline=False)
        self.recipe_details = TextInput(hint_text=ar("المقادير والخطوات..."), font_size=16, font_name='ArabicFont', size_hint_y=None, height=65)
        
        layout.add_widget(self.recipe_name)
        layout.add_widget(self.recipe_details)
        
        btn_save = CardButton(text=ar("حفظ الوصفة"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_save.base_color = [0.45, 0.15, 0.25, 1]
        btn_save.bind(on_press=self.save_recipe)
        layout.add_widget(btn_save)
        
        self.recipes_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.recipes_layout.bind(minimum_height=self.recipes_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.recipes_layout)
        layout.add_widget(scroll)
        
        btn_back = CardButton(text=ar("العودة للرئيسية"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_back.base_color = [0.3, 0.18, 0.22, 1]
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def save_recipe(self, instance):
        name = self.recipe_name.text.strip()
        details = self.recipe_details.text.strip()
        if name and details:
            recipe_text = f"{name}: {details}"
            lbl = Label(text=ar(recipe_text), font_size=16, font_name='ArabicFont', color=(1, 1, 1, 1), size_hint_y=None, height=70)
            self.recipes_layout.add_widget(lbl)
            self.recipe_name.text = ""
            self.recipe_details.text = ""


class AzkarScreen(Screen):
    def __init__(self, **kwargs):
        super(AzkarScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)
        layout.add_widget(Label(text=ar("حصن المسلم والأدعية"), font_size=22, font_name='ArabicFont', color=(0.9, 0.7, 0.8, 1), size_hint_y=None, height=45))
        
        self.zekr_label = Label(text=ar(azkar_list[0]), font_size=20, font_name='ArabicFont', color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(350, 200))
        layout.add_widget(self.zekr_label)
        
        btn_next = CardButton(text=ar("دعاء آخر"), font_size=18, font_name='ArabicFont', size_hint_y=None, height=55)
        btn_next.base_color = [0.45, 0.15, 0.25, 1]
        btn_next.bind(on_press=lambda x: setattr(self.zekr_label, 'text', ar(random.choice(azkar_list))))
        layout.add_widget(btn_next)
        
        btn_back = CardButton(text=ar("العودة للرئيسية"), font_size=16, font_name='ArabicFont', size_hint_y=None, height=50)
        btn_back.base_color = [0.3, 0.18, 0.22, 1]
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        self.add_widget(layout)


class MomsAppCombined(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MedicinesScreen(name='medicines'))
        sm.add_widget(CookingScreen(name='cooking'))
        sm.add_widget(ShoppingScreen(name='shopping'))
        sm.add_widget(RecipesScreen(name='recipes'))
        sm.add_widget(AzkarScreen(name='azkar'))
        return sm

if __name__ == '__main__':
    MomsAppCombined().run()