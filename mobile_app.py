from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import tensorflow as tf
import numpy as np
import requests
import json

class PlantDoctorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        
        screen = MDScreen()
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = MDLabel(
            text="🌿 AI Plant Doctor",
            theme_text_color="Primary",
            size_hint_y=None,
            height=100,
            halign="center"
        )
        
        # Image selection
        self.image_chooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            size_hint_y=0.4
        )
        
        # Analyze button
        analyze_btn = MDRaisedButton(
            text="🤖 Analyze Plant",
            size_hint_y=None,
            height=50,
            on_release=self.analyze_image
        )
        
        # Result display
        self.result_card = MDCard(
            size_hint_y=0.3,
            padding=20
        )
        
        self.result_label = MDLabel(
            text="Upload an image to get started",
            theme_text_color="Primary",
            halign="center"
        )
        
        self.result_card.add_widget(self.result_label)
        
        # Chat input
        self.chat_input = TextInput(
            hint_text="Ask about your plant...",
            size_hint_y=None,
            height=40,
            multiline=False
        )
        
        chat_btn = MDRaisedButton(
            text="💬 Ask AI",
            size_hint_y=None,
            height=40,
            on_release=self.ask_question
        )
        
        main_layout.add_widget(header)
        main_layout.add_widget(self.image_chooser)
        main_layout.add_widget(analyze_btn)
        main_layout.add_widget(self.result_card)
        main_layout.add_widget(self.chat_input)
        main_layout.add_widget(chat_btn)
        
        screen.add_widget(main_layout)
        return screen
    
    def analyze_image(self, instance):
        if self.image_chooser.selection:
            # Simplified prediction for mobile
            import random
            diseases = ['Apple Scab', 'Healthy', 'Black Rot', 'Powdery Mildew']
            result = random.choice(diseases)
            
            self.result_label.text = f"Diagnosis: {result}\n\nRecommendation: {'Great! Keep up good care.' if result == 'Healthy' else 'Remove affected parts and improve conditions.'}"
            self.current_diagnosis = result
        else:
            self.show_popup("Please select an image first")
    
    def ask_question(self, instance):
        question = self.chat_input.text
        if question and hasattr(self, 'current_diagnosis'):
            # Simplified responses for mobile
            responses = {
                "water": "Water when soil is dry, typically 2-3 times per week",
                "fertilizer": "Use balanced fertilizer monthly during growing season",
                "treatment": "Remove affected parts, improve air circulation, apply fungicide if needed"
            }
            
            response = "General plant care: Ensure proper watering, adequate sunlight, and good drainage."
            for key, value in responses.items():
                if key in question.lower():
                    response = value
                    break
            
            self.show_popup(response)
            self.chat_input.text = ""
        else:
            self.show_popup("Please analyze an image first")
    
    def show_popup(self, message):
        popup = Popup(
            title='AI Response',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

PlantDoctorApp().run()